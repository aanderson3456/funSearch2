import sys
import os
import math
import copy
import json
import torch
import torch.nn.functional as F
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "big_nn"))
from resnet import SnakyNet
from env import SnakyEnv
from generate_html import make_html

# --- Precompute 13x13 board shapes ---
_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]
def _get_board_shapes(radius: int = 6):
    orientations = set()
    for rot in range(4):
        for ref in range(2):
            s = _BASE_SNAKY
            if ref:
                s = [(-p[0], p[1]) for p in s]
            for _ in range(rot):
                s = [(p[1], -p[0]) for p in s]
            mx = min(p[0] for p in s)
            my = min(p[1] for p in s)
            normalized = tuple(sorted((p[0] - mx, p[1] - my) for p in s))
            orientations.add(normalized)

    shapes = []
    for ori in orientations:
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                translated = tuple(sorted((x + dx, y + dy) for x, y in ori))
                if all(-radius <= x <= radius and -radius <= y <= radius for x, y in translated):
                    shapes.append(frozenset(translated))
    return list(set(shapes))

ALL_SHAPES_13X13 = _get_board_shapes(radius=6)

# --- Precompute Heuristic Planes for NNv2 ---
checkerboard = np.zeros((13, 13), dtype=np.float32)
centrality = np.zeros((13, 13), dtype=np.float32)
center = 6.0
max_dist = 13 / 1.414
for _y in range(13):
    for _x in range(13):
        checkerboard[_y, _x] = 1.0 if (_x + _y) % 2 == 0 else 0.0
        dist = np.sqrt((_x - center)**2 + (_y - center)**2)
        centrality[_y, _x] = max(0.0, 1.0 - (dist / max_dist))

# --- State Encoder supporting 3-channel (v1) and 5-channel (v2) models ---
def encode_state(env, in_channels, device):
    state = np.zeros((in_channels, env.size, env.size), dtype=np.float32)
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

    if in_channels == 5:
        state[3] = checkerboard
        state[4] = centrality

    return torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)

# --- MCTS Node & Search ---
class Node:
    def __init__(self, parent=None, prior_prob=1.0):
        self.parent = parent
        self.children = {} # action : Node
        self.visit_count = 0
        self.value_sum = 0.0
        self.prior_prob = prior_prob

    def is_expanded(self):
        return len(self.children) > 0

    def get_value(self):
        if self.visit_count == 0:
            return 0.0
        return self.value_sum / self.visit_count

class FlexibleMCTS:
    def __init__(self, model, in_channels, num_searches=100, c_puct=1.0, device="cpu"):
        self.model = model
        self.in_channels = in_channels
        self.num_searches = num_searches
        self.c_puct = c_puct
        self.device = device

    def search(self, initial_env):
        root = Node()
        state_tensor = encode_state(initial_env, self.in_channels, self.device)
        with torch.no_grad():
            policy_logits, _ = self.model(state_tensor)
            policy = F.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy()

        legal_moves = initial_env.get_legal_moves()
        valid_policy = np.zeros_like(policy)
        valid_policy[legal_moves] = policy[legal_moves]
        sum_p = np.sum(valid_policy)
        if sum_p > 0:
            valid_policy /= sum_p
        else:
            if len(legal_moves) > 0:
                valid_policy[legal_moves] = 1.0 / len(legal_moves)

        for action in legal_moves:
            root.children[action] = Node(parent=root, prior_prob=valid_policy[action])

        for _ in range(self.num_searches):
            node = root
            scratch_env = SnakyEnv(size=initial_env.size)
            scratch_env.maker_board = initial_env.maker_board
            scratch_env.breaker_board = initial_env.breaker_board
            scratch_env.current_player = initial_env.current_player
            scratch_env.done = initial_env.done
            scratch_env.winner = initial_env.winner

            # 1. Selection
            while node.is_expanded() and not scratch_env.done:
                best_ucb = -float('inf')
                best_action = None
                best_child = None

                for action, child in node.children.items():
                    q_val = child.get_value()
                    # Q is from Maker's perspective (+1 Maker, -1 Breaker)
                    if scratch_env.current_player == 1:
                        q = q_val
                    else:
                        q = -q_val

                    u = self.c_puct * child.prior_prob * math.sqrt(node.visit_count) / (1 + child.visit_count)
                    score = q + u
                    if score > best_ucb:
                        best_ucb = score
                        best_action = action
                        best_child = child

                if best_child is None:
                    break

                scratch_env.step(best_action)
                node = best_child

            # 2. Evaluation & Expansion
            if not scratch_env.done:
                s_tensor = encode_state(scratch_env, self.in_channels, self.device)
                with torch.no_grad():
                    p_logits, v = self.model(s_tensor)
                    p = F.softmax(p_logits, dim=1).squeeze(0).cpu().numpy()
                    value = v.item()

                l_moves = scratch_env.get_legal_moves()
                v_policy = np.zeros_like(p)
                v_policy[l_moves] = p[l_moves]
                s_val = np.sum(v_policy)
                if s_val > 0:
                    v_policy /= s_val
                elif len(l_moves) > 0:
                    v_policy[l_moves] = 1.0 / len(l_moves)

                for a in l_moves:
                    node.children[a] = Node(parent=node, prior_prob=v_policy[a])
            else:
                if scratch_env.winner == 1:
                    value = 1.0
                else:
                    value = -1.0

            # 3. Backpropagation
            curr = node
            while curr is not None:
                curr.visit_count += 1
                curr.value_sum += value
                curr = curr.parent

        # Compute visit distribution
        action_probs = np.zeros(initial_env.size * initial_env.size, dtype=np.float32)
        for action, child in root.children.items():
            action_probs[action] = child.visit_count
        sum_visits = np.sum(action_probs)
        if sum_visits > 0:
            action_probs /= sum_visits
        return action_probs

mcts_cache = {}

def get_agent_priority(candidate, maker_cells, breaker_cells, active_shapes, role, mcts_agent):
    state_key = (frozenset(maker_cells), frozenset(breaker_cells), role, mcts_agent.in_channels, id(mcts_agent.model))
    if state_key not in mcts_cache:
        env = SnakyEnv(size=13)
        for x, y in maker_cells:
            env.maker_board |= (1 << ((y + 6) * 13 + (x + 6)))
        for x, y in breaker_cells:
            env.breaker_board |= (1 << ((y + 6) * 13 + (x + 6)))
        env.current_player = role
        mcts_cache[state_key] = mcts_agent.search(env)

    action_probs = mcts_cache[state_key]
    idx = (candidate[1] + 6) * 13 + (candidate[0] + 6)
    return float(action_probs[idx])

def play_match(maker_strat, breaker_strat, maker_name, breaker_name):
    m_cells, b_cells = [], []
    maker_won = False
    trace = []
    winning_shape = None

    print(f"\n--- Playing Match: Maker ({maker_name}) vs Breaker ({breaker_name}) ---")
    for turn in range(85):
        print(f"\rTurn {turn + 1}/85...", end="", flush=True)
        m_set, b_set = set(m_cells), set(b_cells)

        # Check Maker win
        for s in ALL_SHAPES_13X13:
            if s.issubset(m_set):
                maker_won = True
                winning_shape = list(s)
                break
        if maker_won:
            break

        active = [s for s in ALL_SHAPES_13X13 if not (s & b_set)]
        if not active:
            break

        candidates = set()
        for s in active:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates.add(p)
        if not candidates:
            break

        # Maker turn
        best_m_move = max(candidates, key=lambda c: maker_strat(c, m_cells, b_cells, active))
        m_cells.append(best_m_move)
        m_set.add(best_m_move)
        trace.append({"turn": turn + 1, "player": "maker", "move": [best_m_move[0], best_m_move[1]]})

        # Check Maker win again
        for s in ALL_SHAPES_13X13:
            if s.issubset(m_set):
                maker_won = True
                winning_shape = list(s)
                break
        if maker_won:
            break

        active = [s for s in ALL_SHAPES_13X13 if not (s & b_set)]
        if not active:
            break

        candidates = set()
        for s in active:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates.add(p)
        if not candidates:
            break

        # Breaker turn
        best_b_move = max(candidates, key=lambda c: breaker_strat(c, m_cells, b_cells, active))
        b_cells.append(best_b_move)
        trace.append({"turn": turn + 1, "player": "breaker", "move": [best_b_move[0], best_b_move[1]]})

    print(f"\nMatch finished! Result: {'Maker (' + maker_name + ') won!' if maker_won else 'Breaker (' + breaker_name + ') won!'} Total turns: {len(m_cells)}")
    return trace, winning_shape

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using compute device: {device}")

    v1_checkpoint = "snaky_large_model_it608.pt"
    v2_checkpoint = "snaky_large_model_it129.pt"

    print(f"Loading NNv1 (3-channel) from {v1_checkpoint}...")
    model_v1 = SnakyNet(in_channels=3, num_resBlocks=16, num_channels=256, board_size=13).to(device)
    model_v1.load_state_dict(torch.load(v1_checkpoint, map_location=device, weights_only=True))
    model_v1.eval()

    print(f"Loading NNv2 (5-channel) from {v2_checkpoint}...")
    model_v2 = SnakyNet(in_channels=5, num_resBlocks=16, num_channels=256, board_size=13).to(device)
    model_v2.load_state_dict(torch.load(v2_checkpoint, map_location=device, weights_only=True))
    model_v2.eval()

    agent_v1 = FlexibleMCTS(model_v1, in_channels=3, num_searches=100, device=device)
    agent_v2 = FlexibleMCTS(model_v2, in_channels=5, num_searches=100, device=device)

    # --- Match 1: NNv2 (Maker) vs NNv1 (Breaker) ---
    global mcts_cache
    mcts_cache = {}
    trace1, shape1 = play_match(
        lambda c, m, b, a: get_agent_priority(c, m, b, a, 1, agent_v2),
        lambda c, m, b, a: get_agent_priority(c, m, b, a, -1, agent_v1),
        maker_name="NNv2_it129",
        breaker_name="NNv1_it608"
    )
    with open("arena_v2_vs_v1_trace.json", "w") as f:
        json.dump({"trace": trace1, "winningShape": shape1}, f)
    make_html("arena_v2_vs_v1_trace.json", "arena_v2_vs_v1_replay.html", title="Snaky Match: Maker (NNv2 it129) vs Breaker (NNv1 it608)")
    print("Saved replay to arena_v2_vs_v1_replay.html")

    # --- Match 2: NNv1 (Maker) vs NNv2 (Breaker) ---
    mcts_cache = {}
    trace2, shape2 = play_match(
        lambda c, m, b, a: get_agent_priority(c, m, b, a, 1, agent_v1),
        lambda c, m, b, a: get_agent_priority(c, m, b, a, -1, agent_v2),
        maker_name="NNv1_it608",
        breaker_name="NNv2_it129"
    )
    with open("arena_v1_vs_v2_trace.json", "w") as f:
        json.dump({"trace": trace2, "winningShape": shape2}, f)
    make_html("arena_v1_vs_v2_trace.json", "arena_v1_vs_v2_replay.html", title="Snaky Match: Maker (NNv1 it608) vs Breaker (NNv2 it129)")
    print("Saved replay to arena_v1_vs_v2_replay.html")

    print("\nAll matches finished successfully!")

if __name__ == "__main__":
    main()
