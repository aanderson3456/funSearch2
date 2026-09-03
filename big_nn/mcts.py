import math
import torch
import torch.nn.functional as F
import numpy as np
import copy
from env import SnakyEnv

class Node:
    def __init__(self, parent=None, prior_prob=1.0):
        self.parent = parent
        self.children = {} # action : Node
        self.visit_count = 0
        self.value_sum = 0
        self.prior_prob = prior_prob

    def is_expanded(self):
        return len(self.children) > 0

    def get_value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count
        
class MCTS:
    def __init__(self, model, num_searches=50, c_puct=1.0, device="cpu"):
        self.model = model
        self.num_searches = num_searches
        self.c_puct = c_puct
        self.device = device
        
    def _encode_state(self, env):
        # returns tensor of shape (1, 3, 8, 8)
        state = np.zeros((3, env.size, env.size), dtype=np.float32)
        for i in range(env.size * env.size):
            y, x = divmod(i, env.size)
            if env.maker_board & (1 << i):
                state[0, y, x] = 1.0
            if env.breaker_board & (1 << i):
                state[1, y, x] = 1.0
        
        if env.current_player == 1:
            state[2, :, :] = 1.0
        else:
            state[2, :, :] = 0.0
            
        return torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)

    def search(self, initial_env):
        root = Node()
        
        # Expand root
        state_tensor = self._encode_state(initial_env)
        with torch.no_grad():
            policy_logits, _ = self.model(state_tensor)
            policy = F.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy()
            
        legal_moves = initial_env.get_legal_moves()
        
        # Mask illegal moves
        valid_policy = np.zeros_like(policy)
        valid_policy[legal_moves] = policy[legal_moves]
        
        policy_sum = np.sum(valid_policy)
        if policy_sum > 0:
            valid_policy /= policy_sum
        else:
            # Fallback if network outputs extremely low values for all legal moves
            valid_policy[legal_moves] = 1.0 / len(legal_moves)
            
        for move in legal_moves:
            root.children[move] = Node(parent=root, prior_prob=valid_policy[move])

        # Add Dirichlet noise for exploration at root
        dirichlet_alpha = 0.3
        dirichlet_noise = np.random.dirichlet([dirichlet_alpha] * len(legal_moves))
        frac = 0.25
        for i, move in enumerate(legal_moves):
            root.children[move].prior_prob = (1 - frac) * root.children[move].prior_prob + frac * dirichlet_noise[i]

        for _ in range(self.num_searches):
            node = root
            env = copy.deepcopy(initial_env)
            
            # Selection
            while node.is_expanded():
                best_ucb = -float('inf')
                best_action = None
                best_child = None
                
                for action, child in node.children.items():
                    # PUCT formula
                    # UCB = Q + C * P * sqrt(N_parent) / (1 + N_child)
                    # Q is defined from current player's perspective. 
                    # If Maker's turn, Q = get_value() (Maker win prob). 
                    # Wait, if Q is always from Maker's perspective, we need to adapt it.
                    # Value from network is from Maker's perspective (+1 Maker win, -1 Breaker win).
                    # So if current player is Maker, we maximize Q. If Breaker, we MINIMIZE Q.
                    
                    q_val = child.get_value()
                    # If it's Breaker's turn in the simulation, Breaker wants to minimize the score, 
                    # so we negate q_val for Breaker.
                    # Wait, the node we are evaluating is a child. The turn that led to this child was taken by `env.current_player`.
                    # So the player making the choice at `node` is `env.current_player`.
                    
                    if env.current_player == 1:
                        q = q_val
                    else:
                        q = -q_val
                        
                    u = self.c_puct * child.prior_prob * math.sqrt(node.visit_count) / (1 + child.visit_count)
                    ucb = q + u
                    
                    if ucb > best_ucb:
                        best_ucb = ucb
                        best_action = action
                        best_child = child
                        
                node = best_child
                done, winner = env.step(best_action)
                
            # Expansion and Evaluation
            if not env.done:
                state_tensor = self._encode_state(env)
                with torch.no_grad():
                    policy_logits, value = self.model(state_tensor)
                    policy = F.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy()
                    v = value.item() # Maker's perspective
                    
                legal_moves = env.get_legal_moves()
                valid_policy = np.zeros_like(policy)
                valid_policy[legal_moves] = policy[legal_moves]
                
                policy_sum = np.sum(valid_policy)
                if policy_sum > 0:
                    valid_policy /= policy_sum
                else:
                    valid_policy[legal_moves] = 1.0 / len(legal_moves)
                    
                for move in legal_moves:
                    node.children[move] = Node(parent=node, prior_prob=valid_policy[move])
            else:
                # Terminal state
                v = float(winner) # 1 if Maker, -1 if Breaker (but Breaker win is never explicitly encoded in winner right now).
                # Wait, env.py sets winner=0 for draw, winner=1 for Maker. Breaker wins by drawing (board full).
                # Wait! Maker wins if they make the shape. Breaker wins if they BLOCK Maker until the board is full. 
                # So a "draw" in Snaky is actually a Breaker win!
                if winner == 1:
                    v = 1.0
                else:
                    v = -1.0 # Breaker win
                    
            # Backpropagation
            while node is not None:
                node.visit_count += 1
                node.value_sum += v
                node = node.parent
                
        # Return action probabilities
        action_probs = np.zeros(initial_env.size * initial_env.size)
        for action, child in root.children.items():
            action_probs[action] = child.visit_count / self.num_searches
            
        return action_probs
