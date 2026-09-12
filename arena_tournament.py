import sys
import os
import math
import json
import torch
import torch.nn.functional as F
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "big_nn"))
from resnet import SnakyNet
from env import SnakyEnv
from generate_html import make_html

# Precompute board shapes for 13x13 win checks
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

# Static Heuristic Planes
checkerboard = np.zeros((13, 13), dtype=np.float32)
centrality = np.zeros((13, 13), dtype=np.float32)
center = 6.0
max_dist = 13 / 1.414
for _y in range(13):
    for _x in range(13):
        checkerboard[_y, _x] = 1.0 if (_x + _y) % 2 == 0 else 0.0
        dist = np.sqrt((_x - center)**2 + (_y - center)**2)
        centrality[_y, _x] = max(0.0, 1.0 - (dist / max_dist))
HEURISTIC_STATIC_PLANES = np.stack([checkerboard, centrality])

# Threat Heuristic Tables
_temp_env = SnakyEnv(size=13)
_mask_cells = []
for m in _temp_env.win_masks:
    _mask_cells.append([i for i in range(169) if (m & (1 << i))])
WIN_MASK_CELLS = np.array(_mask_cells, dtype=np.int32)
WEIGHT_LOOKUP = np.array([0, 2, 10, 50, 250, 10000, 0], dtype=np.float32)

def compute_threat(maker_board, breaker_board):
    m_arr = np.array([(maker_board & (1 << i)) != 0 for i in range(169)], dtype=np.float32)
    b_arr = np.array([(breaker_board & (1 << i)) != 0 for i in range(169)], dtype=np.float32)
    mask_b_counts = b_arr[WIN_MASK_CELLS].sum(axis=1)
    active_idx = np.where(mask_b_counts == 0)[0]
    if len(active_idx) == 0:
        return np.zeros(169, dtype=np.float32), False
    active_cells = WIN_MASK_CELLS[active_idx]
    m_counts = m_arr[active_cells].sum(axis=1).astype(np.int32)
    is_crit = bool(np.any(m_counts == 5))
    weights = WEIGHT_LOOKUP[m_counts]
    empty_mask = (m_arr[active_cells] == 0)
    t_map = np.zeros(169, dtype=np.float32)
    np.add.at(t_map, active_cells[empty_mask], np.broadcast_to(weights[:, None], active_cells.shape)[empty_mask])
    return t_map, is_crit

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

    if in_channels >= 5:
        state[3] = HEURISTIC_STATIC_PLANES[0]
        state[4] = HEURISTIC_STATIC_PLANES[1]

    if in_channels == 6:
        t_map, _ = compute_threat(env.maker_board, env.breaker_board)
        mx = max(float(t_map.max()), 1e-5)
        state[5] = (t_map / mx).reshape(13, 13)

    return torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)

class Node:
    def __init__(self, parent=None, prior_prob=1.0):
        self.parent = parent
        self.children = {}
        self.visit_count = 0
        self.value_sum = 0.0
        self.prior_prob = prior_prob

    def is_expanded(self):
        return len(self.children) > 0

    def get_value(self):
        if self.visit_count == 0:
            return 0.0
        return self.value_sum / self.visit_count

class ArenaAgent:
    def __init__(self, name, model, in_channels, device, num_searches=100, use_threat_blend=False):
        self.name = name
        self.model = model
        self.in_channels = in_channels
        self.device = device
        self.num_searches = num_searches
        self.c_puct = 1.0
        self.use_threat_blend = use_threat_blend

    def search(self, initial_env):
        root = Node()
        state_tensor = encode_state(initial_env, self.in_channels, self.device)
        with torch.no_grad():
            policy_logits, _ = self.model(state_tensor)
            policy = F.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy()

        legal_moves = initial_env.get_legal_moves()
        if self.use_threat_blend and initial_env.current_player == -1 and len(legal_moves) > 0:
            t_map, is_crit = compute_threat(initial_env.maker_board, initial_env.breaker_board)
            t_legal = t_map[legal_moves]
            t_sum = np.sum(t_legal)
            if is_crit:
                crit_mask = (t_legal >= 9000)
                if np.any(crit_mask):
                    p_threat = np.zeros_like(t_legal)
                    p_threat[crit_mask] = 1.0 / np.sum(crit_mask)
                    policy[legal_moves] = 0.05 * policy[legal_moves] + 0.95 * p_threat
            elif t_sum > 0:
                p_threat = t_legal / t_sum
                policy[legal_moves] = 0.65 * policy[legal_moves] + 0.35 * p_threat

        valid_policy = np.zeros_like(policy)
        valid_policy[legal_moves] = policy[legal_moves]
        sum_p = np.sum(valid_policy)
        if sum_p > 0:
            valid_policy /= sum_p
        elif len(legal_moves) > 0:
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
                    q = q_val if scratch_env.current_player == 1 else -q_val
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
                value = 1.0 if scratch_env.winner == 1 else -1.0

            # 3. Backpropagation
            curr = node
            while curr is not None:
                curr.visit_count += 1
                curr.value_sum += value
                curr = curr.parent

        action_probs = np.zeros(initial_env.size * initial_env.size, dtype=np.float32)
        for action, child in root.children.items():
            action_probs[action] = child.visit_count
        sum_visits = np.sum(action_probs)
        if sum_visits > 0:
            action_probs /= sum_visits
        return action_probs

mcts_cache = {}

def get_agent_priority(candidate, maker_cells, breaker_cells, active_shapes, role, agent):
    state_key = (frozenset(maker_cells), frozenset(breaker_cells), role, agent.name)
    if state_key not in mcts_cache:
        env = SnakyEnv(size=13)
        for x, y in maker_cells:
            env.maker_board |= (1 << ((y + 6) * 13 + (x + 6)))
        for x, y in breaker_cells:
            env.breaker_board |= (1 << ((y + 6) * 13 + (x + 6)))
        env.current_player = role
        mcts_cache[state_key] = agent.search(env)

    action_probs = mcts_cache[state_key]
    idx = (candidate[1] + 6) * 13 + (candidate[0] + 6)
    return float(action_probs[idx])

def play_match(maker_agent, breaker_agent):
    global mcts_cache
    mcts_cache = {}

    m_cells, b_cells = [], []
    maker_won = False
    trace = []
    winning_shape = None

    print(f"\n=======================================================")
    print(f"MATCH: Maker ({maker_agent.name}) vs Breaker ({breaker_agent.name})")
    print(f"=======================================================")

    for turn in range(85):
        print(f"\rTurn {turn + 1}/85...", end="", flush=True)
        m_set, b_set = set(m_cells), set(b_cells)

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

        candidates_list = sorted(candidates, key=lambda c: (abs(c[0]) + abs(c[1]), c[1], c[0]))

        # Maker turn
        best_m_move = max(candidates_list, key=lambda c: get_agent_priority(c, m_cells, b_cells, active, 1, maker_agent))
        m_cells.append(best_m_move)
        m_set.add(best_m_move)
        trace.append({"turn": turn + 1, "player": "maker", "move": [best_m_move[0], best_m_move[1]]})

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

        candidates_list = sorted(candidates, key=lambda c: (abs(c[0]) + abs(c[1]), c[1], c[0]))

        # Breaker turn
        best_b_move = max(candidates_list, key=lambda c: get_agent_priority(c, m_cells, b_cells, active, -1, breaker_agent))
        b_cells.append(best_b_move)
        trace.append({"turn": turn + 1, "player": "breaker", "move": [best_b_move[0], best_b_move[1]]})

    winner_name = maker_agent.name if maker_won else breaker_agent.name
    print(f"\nMatch finished! Winner: {winner_name} ({'Maker' if maker_won else 'Breaker'}) in {len(m_cells)} turns.")
    return trace, winning_shape, winner_name, len(m_cells)

def run_match_and_save(maker_agent, breaker_agent, trace_file, html_file, title):
    trace, shape, winner, turns = play_match(maker_agent, breaker_agent)
    with open(trace_file, "w") as f:
        json.dump({"trace": trace, "winningShape": shape}, f)
    make_html(trace_file, html_file, title=f"{title} - Winner: {winner} ({turns} turns)")
    print(f"Generated replay: {html_file}")
    return winner, turns
