import numpy as np
import time, math
import torch
import torch.nn as nn
import torch.nn.functional as F
from big_nn.env import SnakyEnv

# Mock model
class MockModel(nn.Module):
    def forward(self, x):
        batch = x.shape[0]
        return torch.randn(batch, 169).to(x.device), torch.randn(batch, 1).to(x.device)

class FastSnakyEnv:
    def __init__(self, size=13):
        self.size = size
        self.maker_board = 0
        self.breaker_board = 0
        self.current_player = 1 
        self.done = False
        self.winner = 0
        self.occupied_array = np.zeros(size * size, dtype=bool)
        self.maker_array = np.zeros(size * size, dtype=np.float32)
        self.breaker_array = np.zeros(size * size, dtype=np.float32)
        
        temp_env = SnakyEnv(size=size)
        self.win_masks = temp_env.win_masks

    def get_legal_moves(self):
        return np.where(~self.occupied_array)[0].tolist()
        
    def step(self, move):
        move = int(move)
        if self.done:
            return self.done, self.winner
            
        self.occupied_array[move] = True
        
        if self.current_player == 1:
            self.maker_board |= (1 << move)
            self.maker_array[move] = 1.0
            mb = self.maker_board
            for m in self.win_masks:
                if (mb & m) == m:
                    self.done = True
                    self.winner = 1
                    return self.done, self.winner
        else:
            self.breaker_board |= (1 << move)
            self.breaker_array[move] = 1.0
            
        if (self.maker_board | self.breaker_board) == ((1 << (self.size * self.size)) - 1):
            self.done = True
            self.winner = 0
            return self.done, self.winner
            
        self.current_player *= -1
        return self.done, self.winner
        
def clone_env(env):
    new_env = object.__new__(FastSnakyEnv)
    new_env.size = env.size
    new_env.maker_board = env.maker_board
    new_env.breaker_board = env.breaker_board
    new_env.current_player = env.current_player
    new_env.done = env.done
    new_env.winner = env.winner
    new_env.occupied_array = env.occupied_array.copy()
    new_env.maker_array = env.maker_array.copy()
    new_env.breaker_array = env.breaker_array.copy()
    new_env.win_masks = env.win_masks
    return new_env

class FastNode:
    def __init__(self, parent=None, action_idx_in_parent=None):
        self.parent = parent
        self.action_idx_in_parent = action_idx_in_parent
        self.is_expanded_flag = False
        self.total_visits = 0
        
    def is_expanded(self):
        return self.is_expanded_flag
        
    def expand(self, legal_moves, priors):
        self.is_expanded_flag = True
        self.legal_moves = np.array(legal_moves, dtype=np.int32)
        num_moves = len(legal_moves)
        
        self.visits = np.zeros(num_moves, dtype=np.float32)
        self.values = np.zeros(num_moves, dtype=np.float32)
        self.priors = priors[legal_moves]
        
        p_sum = np.sum(self.priors)
        if p_sum > 0:
            self.priors /= p_sum
        else:
            if num_moves > 0:
                self.priors = np.ones(num_moves, dtype=np.float32) / num_moves
                
        self.children = [None] * num_moves

def _encode_state_batch(envs, device):
    n = len(envs)
    size = envs[0].size
    states = np.empty((n, 3, size * size), dtype=np.float32)
    
    states[:, 0] = [e.maker_array for e in envs]
    states[:, 1] = [e.breaker_array for e in envs]
    cp = np.array([e.current_player for e in envs], dtype=np.float32)
    states[:, 2] = (cp == 1)[:, None]
    
    states = states.reshape(n, 3, size, size)
    return torch.tensor(states, dtype=torch.float32, device=device)

def batched_search(model, envs, num_searches, c_puct=1.0, add_noise=False, device='cpu'):
    roots = [FastNode() for _ in range(len(envs))]
    
    states_tensor = _encode_state_batch(envs, device)
    with torch.no_grad():
        policy_logits, _ = model(states_tensor)
        policies = F.softmax(policy_logits, dim=1).cpu().numpy()
        
    for i, env in enumerate(envs):
        legal_moves = env.get_legal_moves()
        roots[i].expand(legal_moves, policies[i])
        if add_noise and len(legal_moves) > 0:
            dirichlet_alpha = 0.3
            dirichlet_noise = np.random.dirichlet([dirichlet_alpha] * len(legal_moves))
            frac = 0.25
            roots[i].priors = (1 - frac) * roots[i].priors + frac * dirichlet_noise

    for _ in range(num_searches):
        search_envs = [clone_env(env) for env in envs]
        search_nodes = [root for root in roots]
        
        for i in range(len(envs)):
            node = search_nodes[i]
            env = search_envs[i]
            
            while node.is_expanded():
                if len(node.legal_moves) == 0:
                    break
                    
                q = np.divide(node.values, node.visits, out=np.zeros_like(node.values), where=node.visits!=0)
                if env.current_player == -1:
                    q = -q
                u = c_puct * node.priors * math.sqrt(node.total_visits) / (1.0 + node.visits)
                ucb = q + u
                best_idx = np.argmax(ucb)
                
                if node.children[best_idx] is None:
                    node.children[best_idx] = FastNode(parent=node, action_idx_in_parent=best_idx)
                    
                node = node.children[best_idx]
                best_action = node.parent.legal_moves[best_idx]
                env.step(best_action)
                
            search_nodes[i] = node
            
        states_to_eval = []
        eval_indices = []
        for i in range(len(envs)):
            if not search_envs[i].done:
                states_to_eval.append(search_envs[i])
                eval_indices.append(i)
            else:
                v = 1.0 if search_envs[i].winner == 1 else -1.0
                node = search_nodes[i]
                while node.parent is not None:
                    node.total_visits += 1
                    p = node.parent
                    idx = node.action_idx_in_parent
                    p.visits[idx] += 1
                    p.values[idx] += v
                    node = p
                node.total_visits += 1
                
        if states_to_eval:
            states_tensor = _encode_state_batch(states_to_eval, device)
            with torch.no_grad():
                policy_logits, values = model(states_tensor)
                policies = F.softmax(policy_logits, dim=1).cpu().numpy()
                values = values.cpu().numpy()
                
            for idx, i in enumerate(eval_indices):
                node = search_nodes[i]
                env = search_envs[i]
                policy = policies[idx]
                v = values[idx][0]
                
                legal_moves = env.get_legal_moves()
                node.expand(legal_moves, policy)
                
                while node.parent is not None:
                    node.total_visits += 1
                    p = node.parent
                    idx_in_p = node.action_idx_in_parent
                    p.visits[idx_in_p] += 1
                    p.values[idx_in_p] += v
                    node = p
                node.total_visits += 1
                
    action_probs_batch = []
    for i in range(len(envs)):
        action_probs = np.zeros(envs[i].size * envs[i].size)
        root = roots[i]
        for idx_in_p, move in enumerate(root.legal_moves):
            action_probs[move] = root.visits[idx_in_p] / num_searches
            
        s = np.sum(action_probs)
        if s > 0:
            action_probs /= s
        action_probs_batch.append(action_probs)
        
    return action_probs_batch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = MockModel().to(device)
envs = [FastSnakyEnv() for _ in range(100)]
t0 = time.time()
batched_search(model, envs, num_searches=100, device=device)
print("Batched search 1 move across 100 envs:", time.time() - t0)
