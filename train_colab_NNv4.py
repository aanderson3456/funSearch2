import torch
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import os, glob, math, json, re, sys

script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
sys.path.append(os.path.join(script_dir, "big_nn"))
sys.path.append("/content/funSearch2-main")
sys.path.append("/content/funSearch2-main/big_nn")
from env import SnakyEnv
from resnet import SnakyNet

print("=" * 70)
print("SnakyNet NNv4: 7-Channel Dual-Threat Representation & Curriculum Training")
print("=" * 70)

class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.capacity = capacity
        self.buffer = []
        
    def add(self, data):
        self.buffer.extend(data)
        if len(self.buffer) > self.capacity:
            self.buffer = self.buffer[-self.capacity:]
            
    def sample(self, batch_size):
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in indices]

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
    new_env = FastSnakyEnv(size=env.size)
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
    __slots__ = ['parent', 'action_idx_in_parent', 'legal_moves', 'priors', 'visits', 'values', 'total_visits', 'children']
    
    def __init__(self, parent=None, action_idx_in_parent=None):
        self.parent = parent
        self.action_idx_in_parent = action_idx_in_parent
        self.legal_moves = None
        self.priors = None
        self.visits = None
        self.values = None
        self.total_visits = 0
        self.children = None
        
    def is_expanded(self):
        return self.legal_moves is not None
        
    def expand(self, legal_moves, policy):
        self.legal_moves = legal_moves
        num_moves = len(legal_moves)
        self.visits = np.zeros(num_moves, dtype=np.int32)
        self.values = np.zeros(num_moves, dtype=np.float32)
        
        if num_moves > 0:
            self.priors = policy[legal_moves].copy()
            p_sum = np.sum(self.priors)
            if p_sum > 0:
                self.priors /= p_sum
            else:
                self.priors = np.ones(num_moves, dtype=np.float32) / num_moves
                
        self.children = [None] * num_moves

# --- Static Heuristic Planes & Precomputed Threat / FunSearch Tables ---
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

_temp_env = SnakyEnv(size=13)
_mask_cells = []
for m in _temp_env.win_masks:
    _mask_cells.append([i for i in range(169) if (m & (1 << i))])
WIN_MASK_CELLS = np.array(_mask_cells, dtype=np.int32)

WEIGHT_LOOKUP = np.array([0, 2, 10, 50, 250, 10000, 0], dtype=np.float32)

# Grandmaster Maker weights (from rank_9x9_grandmaster_maker.py)
FS_GM_MAKER_WEIGHTS = np.array([1.0, 5.3, 44.8, 1848.3, 105124.1, 10000000.0, 0.0], dtype=np.float32)

# Grandmaster Breaker weights (from rank_9x9_grandmaster_breaker.py)
FS_GM_BREAKER_WEIGHTS = np.array([1.0, 4.2, 36.4, 1167.0, 92750.2, 1e14, 0.0], dtype=np.float32)

COORDS_X = np.tile(np.arange(13, dtype=np.float32), 13)
COORDS_Y = np.repeat(np.arange(13, dtype=np.float32), 13)
R_SQ = (COORDS_X - 6.0)**2 + (COORDS_Y - 6.0)**2
RING_MASK = (R_SQ >= 3.4) & (R_SQ <= 14.0)
MANHATTAN_DIST_GM = (abs(COORDS_X - 6.0) + abs(COORDS_Y - 6.0)) * 0.0633
MANHATTAN_DIST = MANHATTAN_DIST_GM

def compute_threat_planes_single(m_arr, b_arr):
    mask_b_counts = b_arr[WIN_MASK_CELLS].sum(axis=1)
    active_idx = np.where(mask_b_counts == 0)[0]
    if len(active_idx) == 0:
        z = np.zeros(169, dtype=np.float32)
        return z, z, False, z, z
        
    active_cells = WIN_MASK_CELLS[active_idx]
    m_counts = m_arr[active_cells].sum(axis=1).astype(np.int32)
    empty_mask = (m_arr[active_cells] == 0)
    
    # 1. Single threat map (Channel 5)
    is_crit = bool(np.any(m_counts == 5))
    weights = WEIGHT_LOOKUP[m_counts]
    t_map = np.zeros(169, dtype=np.float32)
    np.add.at(t_map, active_cells[empty_mask], np.broadcast_to(weights[:, None], active_cells.shape)[empty_mask])
    
    # 2. Dual threat / Fork potential map (Channel 6)
    is_5 = (m_counts == 5)
    is_4 = (m_counts == 4)
    is_3 = (m_counts == 3)
    
    count_4 = np.zeros(169, dtype=np.float32)
    np.add.at(count_4, active_cells[is_4][empty_mask[is_4]], 1.0)
    
    count_3 = np.zeros(169, dtype=np.float32)
    np.add.at(count_3, active_cells[is_3][empty_mask[is_3]], 1.0)
    
    fork_map = np.zeros(169, dtype=np.float32)
    lethal_fork = (count_4 >= 2)
    fork_map[lethal_fork] = 500.0 * count_4[lethal_fork]
    
    semi_fork = (count_4 == 1) & (count_3 >= 1)
    fork_map[semi_fork] = 50.0 + 10.0 * count_3[semi_fork]
    
    early_fork = (count_4 == 0) & (count_3 >= 2)
    fork_map[early_fork] = 5.0 * count_3[early_fork]
    
    if is_crit:
        t5 = active_cells[is_5][empty_mask[is_5]]
        if len(np.unique(t5)) >= 2:
            fork_map[t5] = 1000.0
            
    norm_t_map = t_map / max(float(np.max(t_map)), 1e-5)
    norm_fork_map = fork_map / max(float(np.max(fork_map)), 1e-5)
    
    return norm_t_map, norm_fork_map, is_crit, t_map, fork_map

def compute_threat_planes_batch(envs):
    n = len(envs)
    norm_t_maps = np.zeros((n, 169), dtype=np.float32)
    norm_fork_maps = np.zeros((n, 169), dtype=np.float32)
    crit_flags = np.zeros(n, dtype=bool)
    raw_t_maps = np.zeros((n, 169), dtype=np.float32)
    raw_fork_maps = np.zeros((n, 169), dtype=np.float32)
    
    for i, e in enumerate(envs):
        nt, nf, ic, rt, rf = compute_threat_planes_single(e.maker_array, e.breaker_array)
        norm_t_maps[i] = nt
        norm_fork_maps[i] = nf
        crit_flags[i] = ic
        raw_t_maps[i] = rt
        raw_fork_maps[i] = rf
        
    return norm_t_maps, norm_fork_maps, crit_flags, raw_t_maps, raw_fork_maps

def compute_funsearch_maker_vectorized(m_arr, b_arr):
    mask_b_counts = b_arr[WIN_MASK_CELLS].sum(axis=1)
    active_idx = np.where(mask_b_counts == 0)[0]
    if len(active_idx) == 0:
        return np.zeros(169, dtype=np.float32)
    active_cells = WIN_MASK_CELLS[active_idx]
    m_counts = m_arr[active_cells].sum(axis=1).astype(np.int32)
    weights = FS_GM_MAKER_WEIGHTS[m_counts]
    empty_mask = (m_arr[active_cells] == 0)
    scores = np.zeros(169, dtype=np.float32)
    active_counts = np.zeros(169, dtype=np.float32)
    np.add.at(scores, active_cells[empty_mask], np.broadcast_to(weights[:, None], active_cells.shape)[empty_mask])
    np.add.at(active_counts, active_cells[empty_mask], 1.0)
    
    # Grandmaster compound fork additions
    is_4 = (m_counts == 4)
    is_3 = (m_counts == 3)
    c4 = np.zeros(169, dtype=np.float32)
    c3 = np.zeros(169, dtype=np.float32)
    np.add.at(c4, active_cells[is_4][empty_mask[is_4]], 1.0)
    np.add.at(c3, active_cells[is_3][empty_mask[is_3]], 1.0)
    
    fork_4_bonus = np.zeros(169, dtype=np.float32)
    fork_4_mask = (c4 >= 2)
    fork_4_bonus[fork_4_mask] = 34598560.2 * (c4[fork_4_mask] ** 2)
    
    fork_3_bonus = np.zeros(169, dtype=np.float32)
    fork_3_mask = (c3 >= 2)
    fork_3_bonus[fork_3_mask] = 66226.7 * (c3[fork_3_mask] ** 1.5)
    
    legal_mask = (m_arr == 0) & (b_arr == 0)
    scores[legal_mask] += fork_4_bonus[legal_mask] + fork_3_bonus[legal_mask]
    scores[legal_mask & RING_MASK] += 8879.8
    scores[legal_mask] += (active_counts[legal_mask] ** 1.29) * 2.67 - MANHATTAN_DIST_GM[legal_mask]
    scores[~legal_mask] = -1e9
    return scores

def compute_funsearch_breaker_vectorized(m_arr, b_arr):
    mask_b_counts = b_arr[WIN_MASK_CELLS].sum(axis=1)
    active_idx = np.where(mask_b_counts == 0)[0]
    if len(active_idx) == 0:
        return np.zeros(169, dtype=np.float32)
    active_cells = WIN_MASK_CELLS[active_idx]
    m_counts = m_arr[active_cells].sum(axis=1).astype(np.int32)
    empty_mask = (m_arr[active_cells] == 0)
    
    # 1. Absolute 5-threat hard override (Grandmaster Breaker Invariant)
    is_5 = (m_counts == 5)
    scores = np.zeros(169, dtype=np.float32)
    if np.any(is_5):
        t5_cells = active_cells[is_5][empty_mask[is_5]]
        scores[t5_cells] = 1e14
        legal_mask = (m_arr == 0) & (b_arr == 0)
        scores[~legal_mask] = -1e9
        return scores
        
    weights = FS_GM_BREAKER_WEIGHTS[m_counts]
    active_counts = np.zeros(169, dtype=np.float32)
    np.add.at(scores, active_cells[empty_mask], np.broadcast_to(weights[:, None], active_cells.shape)[empty_mask])
    np.add.at(active_counts, active_cells[empty_mask], 1.0)
    
    is_4 = (m_counts == 4)
    is_3 = (m_counts == 3)
    c4 = np.zeros(169, dtype=np.float32)
    c3 = np.zeros(169, dtype=np.float32)
    np.add.at(c4, active_cells[is_4][empty_mask[is_4]], 1.0)
    np.add.at(c3, active_cells[is_3][empty_mask[is_3]], 1.0)
    
    scores[c4 >= 2] += 38881787.5 * (c4[c4 >= 2] ** 2.0)
    scores[c4 == 1] += 424595.5
    scores[c3 >= 2] += 337028.8 * (c3[c3 >= 2] ** 1.5)
    
    # Smothering gradient: adhere to maker stones
    m_indices = np.where(m_arr > 0)[0]
    if len(m_indices) > 0:
        mx = COORDS_X[m_indices]
        my = COORDS_Y[m_indices]
        dists = np.abs(COORDS_X[:, None] - mx[None, :]) + np.abs(COORDS_Y[:, None] - my[None, :])
        min_d = np.min(dists, axis=1)
        scores[min_d <= 1] += 8515.9
        scores[min_d == 2] += 3107.8
        
    # Parity contest (2x2)
    cb_2x2 = ((COORDS_X.astype(int) // 2) + (COORDS_Y.astype(int) // 2)) % 2 == 0
    scores[cb_2x2] += 3952.9
    
    legal_mask = (m_arr == 0) & (b_arr == 0)
    scores[legal_mask] += (active_counts[legal_mask] ** 1.46) * 3.91 - MANHATTAN_DIST_GM[legal_mask] * 0.4
    scores[~legal_mask] = -1e9
    return scores

def _encode_state_batch(envs, device, norm_t_maps=None, norm_fork_maps=None):
    n = len(envs)
    size = envs[0].size
    states = np.empty((n, 7, size, size), dtype=np.float32)
    
    mb = np.array([e.maker_array for e in envs], dtype=np.float32).reshape(n, size, size)
    bb = np.array([e.breaker_array for e in envs], dtype=np.float32).reshape(n, size, size)
    states[:, 0] = mb
    states[:, 1] = bb
    cp = np.array([e.current_player for e in envs], dtype=np.float32)
    states[:, 2] = (cp == 1)[:, None, None]
    states[:, 3] = HEURISTIC_STATIC_PLANES[0]
    states[:, 4] = HEURISTIC_STATIC_PLANES[1]
    
    if norm_t_maps is None or norm_fork_maps is None:
        norm_t_maps, norm_fork_maps, _, _, _ = compute_threat_planes_batch(envs)
        
    states[:, 5] = norm_t_maps.reshape(n, size, size)
    states[:, 6] = norm_fork_maps.reshape(n, size, size)
    
    return torch.tensor(states, dtype=torch.float32, device=device)

def blend_breaker_policy(policy, env, t_map, fork_map, is_crit):
    legal_moves = env.get_legal_moves()
    if len(legal_moves) == 0:
        return policy
    t_legal = t_map[legal_moves]
    f_legal = fork_map[legal_moves]
    
    if is_crit:
        crit_mask = (t_legal >= 9000)
        if np.any(crit_mask):
            p_threat = np.zeros_like(t_legal)
            p_threat[crit_mask] = 1.0 / np.sum(crit_mask)
            blended = 0.05 * policy[legal_moves] + 0.95 * p_threat
            p_copy = policy.copy()
            p_copy[legal_moves] = blended
            return p_copy
            
    lethal_fork_mask = (f_legal >= 1000)
    if np.any(lethal_fork_mask):
        p_fork = np.zeros_like(f_legal)
        p_fork[lethal_fork_mask] = 1.0 / np.sum(lethal_fork_mask)
        blended = 0.20 * policy[legal_moves] + 0.80 * p_fork
        p_copy = policy.copy()
        p_copy[legal_moves] = blended
        return p_copy
        
    combined = t_legal + 2.0 * f_legal
    c_sum = np.sum(combined)
    if c_sum > 0:
        p_def = combined / c_sum
        blended = 0.60 * policy[legal_moves] + 0.40 * p_def
        p_copy = policy.copy()
        p_copy[legal_moves] = blended
        return p_copy
        
    return policy

def batched_search(model, envs, num_searches, move_count=1, c_puct=1.0, add_noise=False, device="cuda"):
    roots = [FastNode() for _ in range(len(envs))]
    
    # Precompute threats & forks ONCE across all active envs at root
    norm_t_maps, norm_fork_maps, crit_flags, raw_t_maps, raw_fork_maps = compute_threat_planes_batch(envs)
    states_tensor = _encode_state_batch(envs, device, norm_t_maps=norm_t_maps, norm_fork_maps=norm_fork_maps)
    
    with torch.no_grad():
        policy_logits, _ = model(states_tensor)
        policies = F.softmax(policy_logits, dim=1).cpu().numpy()
        
    for i, env in enumerate(envs):
        legal_moves = env.get_legal_moves()
        policy = policies[i]
        if env.current_player == -1:
            policy = blend_breaker_policy(policy, env, raw_t_maps[i], raw_fork_maps[i], crit_flags[i])
        roots[i].expand(legal_moves, policy)
        
        if add_noise and len(legal_moves) > 0:
            dirichlet_alpha = 0.3
            dirichlet_noise = np.random.dirichlet([dirichlet_alpha] * len(legal_moves))
            
            # Asymmetric exploration on moves 1-6
            if move_count <= 6:
                frac = 0.35 if env.current_player == 1 else 0.15
            else:
                frac = 0.25
                
            roots[i].priors = (1 - frac) * roots[i].priors + frac * dirichlet_noise

    # MCTS Simulation Rollouts
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
                best_move = node.legal_moves[best_idx]
                env.step(best_move)
                
                if node.children[best_idx] is None:
                    child_node = FastNode(parent=node, action_idx_in_parent=best_idx)
                    node.children[best_idx] = child_node
                    search_nodes[i] = child_node
                    break
                else:
                    node = node.children[best_idx]
                    search_nodes[i] = node
                    
        states_to_eval = []
        eval_indices = []
        
        for i in range(len(envs)):
            env = search_envs[i]
            if not env.done:
                states_to_eval.append(env)
                eval_indices.append(i)
            else:
                v = 1.0 if env.winner == 1 else -1.0
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
        
        # Temperature schedule:
        if move_count <= 6:
            tau = 1.25 if envs[i].current_player == 1 else 1.0
        elif move_count <= 20:
            tau = 1.0
        elif move_count <= 40:
            tau = 0.5
        else:
            tau = 0.2
            
        visits = root.visits.astype(np.float64)
        if tau == 1.0:
            probs = visits / np.maximum(visits.sum(), 1.0)
        else:
            # Safe softmax with temperature
            v_tau = visits ** (1.0 / tau)
            s_tau = v_tau.sum()
            probs = v_tau / s_tau if s_tau > 0 else visits / np.maximum(visits.sum(), 1.0)
            
        for idx_in_p, move in enumerate(root.legal_moves):
            action_probs[move] = probs[idx_in_p]
            
        s = np.sum(action_probs)
        if s > 0:
            action_probs /= s
        action_probs_batch.append(action_probs)
        
    return action_probs_batch

def funsearch_maker_step(env, move_count):
    legal = env.get_legal_moves()
    scores = compute_funsearch_maker_vectorized(env.maker_array, env.breaker_array)
    legal_scores = scores[legal]
    
    # If 1-move win exists, take it immediately
    if np.max(legal_scores) >= 900000:
        best_idx = np.argmax(legal_scores)
        best_move = legal[best_idx]
        pi = np.zeros(169, dtype=np.float32)
        pi[best_move] = 1.0
        return best_move, pi
        
    # Softmax sampling with temperature for opening diversity
    if move_count <= 6:
        tau = 2.0
        shifted = (legal_scores - np.max(legal_scores)) / tau
        exp_s = np.exp(np.clip(shifted, -50, 0))
        p = exp_s / np.sum(exp_s)
        chosen_move = np.random.choice(legal, p=p)
        pi = np.zeros(169, dtype=np.float32)
        for idx, m in enumerate(legal):
            pi[m] = p[idx]
        return chosen_move, pi
    else:
        best_idx = np.argmax(legal_scores)
        best_move = legal[best_idx]
        pi = np.zeros(169, dtype=np.float32)
        pi[best_move] = 1.0
        return best_move, pi

def funsearch_breaker_step(env, move_count):
    legal = env.get_legal_moves()
    scores = compute_funsearch_breaker_vectorized(env.maker_array, env.breaker_array)
    legal_scores = scores[legal]
    best_idx = np.argmax(legal_scores)
    best_move = legal[best_idx]
    pi = np.zeros(169, dtype=np.float32)
    pi[best_move] = 1.0
    return best_move, pi

def self_play(model, num_games=100, mcts_searches=100, fs_maker_ratio=0.20, fs_breaker_ratio=0.20, device="cuda"):
    envs = [FastSnakyEnv(size=13) for _ in range(num_games)]
    num_fs_m = int(num_games * fs_maker_ratio)
    num_fs_b = int(num_games * fs_breaker_ratio)
    
    is_fs_maker = np.zeros(num_games, dtype=bool)
    is_fs_breaker = np.zeros(num_games, dtype=bool)
    perm = np.random.permutation(num_games)
    is_fs_maker[perm[:num_fs_m]] = True
    is_fs_breaker[perm[num_fs_m:num_fs_m + num_fs_b]] = True
    
    all_data = []
    active_indices = list(range(num_games))
    game_data = [[] for _ in range(num_games)]
    game_lengths = []
    maker_wins = 0
    breaker_wins = 0
    draws = 0
    
    move_count = 0
    while active_indices:
        move_count += 1
        current_envs = [envs[i] for i in active_indices]
        
        fs_maker_batch_indices = []
        fs_breaker_batch_indices = []
        nn_active_batch_indices = []
        
        for idx_in_batch, orig_idx in enumerate(active_indices):
            env = current_envs[idx_in_batch]
            if is_fs_maker[orig_idx] and env.current_player == 1:
                fs_maker_batch_indices.append(idx_in_batch)
            elif is_fs_breaker[orig_idx] and env.current_player == -1:
                fs_breaker_batch_indices.append(idx_in_batch)
            else:
                nn_active_batch_indices.append(idx_in_batch)
                
        action_probs_batch = [None] * len(active_indices)
        actions_chosen = [None] * len(active_indices)
        
        # 1. Process FunSearch Grandmaster Maker moves
        for idx in fs_maker_batch_indices:
            env = current_envs[idx]
            act, pi = funsearch_maker_step(env, move_count)
            actions_chosen[idx] = act
            action_probs_batch[idx] = pi
            
        # 2. Process FunSearch Grandmaster Breaker moves
        for idx in fs_breaker_batch_indices:
            env = current_envs[idx]
            act, pi = funsearch_breaker_step(env, move_count)
            actions_chosen[idx] = act
            action_probs_batch[idx] = pi
            
        # 3. Process NN moves (MCTS batch)
        if nn_active_batch_indices:
            nn_envs = [current_envs[idx] for idx in nn_active_batch_indices]
            nn_probs = batched_search(model, nn_envs, num_searches=mcts_searches, move_count=move_count, add_noise=True, device=device)
            for sub_idx, idx in enumerate(nn_active_batch_indices):
                pi = nn_probs[sub_idx]
                action_probs_batch[idx] = pi
                actions_chosen[idx] = np.random.choice(169, p=pi)
                
        next_active = []
        for idx_in_batch, original_idx in enumerate(active_indices):
            env = current_envs[idx_in_batch]
            act = actions_chosen[idx_in_batch]
            pi = action_probs_batch[idx_in_batch]
            
            game_data[original_idx].append((env.maker_board, env.breaker_board, env.current_player, pi))
            done, winner = env.step(act)
            
            if done:
                game_lengths.append(move_count)
                if winner == 1:
                    maker_wins += 1
                    reward = 1.0
                elif winner == -1:
                    breaker_wins += 1
                    reward = -1.0
                else:
                    draws += 1
                    reward = 0.0
                    
                for mb, bb, cp, target_pi in game_data[original_idx]:
                    all_data.append((mb, bb, cp, target_pi, reward))
            else:
                next_active.append(original_idx)
                
        active_indices = next_active
        
    print(f"All {num_games} games finished! Avg length: {np.mean(game_lengths):.1f} | Maker Wins: {maker_wins} | Breaker Wins: {breaker_wins} | Draws: {draws}")
    return all_data, game_lengths

def train(model, buffer, batch_size=512, epochs=10, device="cuda"):
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    use_cuda = (device.type == 'cuda') if hasattr(device, 'type') else (device == 'cuda')
    scaler = torch.cuda.amp.GradScaler(enabled=use_cuda)
    model.train()
    total_loss = 0.0
    shifts = 1 << np.arange(169, dtype=object)
    
    for epoch in range(epochs):
        data = buffer.sample(batch_size)
        states = np.zeros((batch_size, 7, 13, 13), dtype=np.float32)
        target_policies = np.zeros((batch_size, 169), dtype=np.float32)
        target_values = np.zeros((batch_size, 1), dtype=np.float32)
        
        mb_arr = np.array([item[0] for item in data], dtype=object)
        bb_arr = np.array([item[1] for item in data], dtype=object)
        
        mb_bits = (mb_arr[:, None] & shifts) != 0
        bb_bits = (bb_arr[:, None] & shifts) != 0
        states[:, 0] = mb_bits.reshape((batch_size, 13, 13))
        states[:, 1] = bb_bits.reshape((batch_size, 13, 13))
        cp = np.array([item[2] for item in data])
        states[:, 2] = (cp == 1)[:, None, None]
        states[:, 3] = HEURISTIC_STATIC_PLANES[0]
        states[:, 4] = HEURISTIC_STATIC_PLANES[1]
        
        for i in range(batch_size):
            nt, nf, _, _, _ = compute_threat_planes_single(mb_bits[i].astype(np.float32), bb_bits[i].astype(np.float32))
            states[i, 5] = nt.reshape(13, 13)
            states[i, 6] = nf.reshape(13, 13)
            target_policies[i] = data[i][3]
            target_values[i] = data[i][4]
            
        states = torch.tensor(states, dtype=torch.float32, device=device)
        target_policies = torch.tensor(target_policies, dtype=torch.float32, device=device)
        target_values = torch.tensor(target_values, dtype=torch.float32, device=device)
        
        optimizer.zero_grad()
        with torch.cuda.amp.autocast(enabled=use_cuda):
            out_policy, out_value = model(states)
            log_probs = F.log_softmax(out_policy, dim=1)
            policy_loss = -(target_policies * log_probs).sum(dim=1).mean()
            value_loss = F.mse_loss(out_value, target_values)
            loss = policy_loss + value_loss
            
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        total_loss += loss.item()
        
    return total_loss / epochs

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')
    print(f'Using compute device: {device}')
    if device.type == 'cuda':
        print(f'GPU Name: {torch.cuda.get_device_name(0)}')

    model = SnakyNet(in_channels=7, num_resBlocks=16, num_channels=256, board_size=13).to(device)
    buffer = ReplayBuffer(capacity=100000)

    checkpoint_dir = "/content/drive/MyDrive/SnakyNet_v4_Checkpoints"
    if not os.path.exists("/content/drive"):
        checkpoint_dir = "checkpoints_v4"
    os.makedirs(checkpoint_dir, exist_ok=True)

    all_models = glob.glob(f"{checkpoint_dir}/snaky_large_model_it*.pt")
    start_iteration = 0
    if all_models:
        def get_it(path):
            m = re.search(r'it(\d+)\.pt', path)
            return int(m.group(1)) if m else -1
        latest_model_path = max(all_models, key=get_it)
        start_iteration = get_it(latest_model_path) + 1
        print(f"\nFound checkpoint: {latest_model_path}")
        loaded = torch.load(latest_model_path, weights_only=False, map_location=device)
        if isinstance(loaded, dict):
            model.load_state_dict(loaded)
            print("Successfully loaded weights from state_dict!")
        else:
            model.load_state_dict(loaded.state_dict())
            print("Successfully extracted and loaded weights from full model!")
    else:
        print("\nNo checkpoints found. Starting NNv4 fresh from scratch at Iteration 0!")

    iterations = 1000
    games_per_iter = 100
    batch_size = 512

    loss_history_path = f"{checkpoint_dir}/loss_history.json"
    loss_history = []
    if os.path.exists(loss_history_path):
        with open(loss_history_path, 'r') as f:
            loss_history = json.load(f)
        print(f"Loaded {len(loss_history)} loss records from Drive!")

    for it in range(start_iteration, iterations):
        print(f"\n--- Iteration {it}/{iterations} ---")
        model.eval()
        print("Starting Grandmaster Hybrid Self-Play (20% GM Maker + 20% GM Breaker Injection)...")
        data, game_lengths = self_play(model, num_games=games_per_iter, mcts_searches=100, fs_maker_ratio=0.25, device=device)
        buffer.add(data)
        
        if len(buffer.buffer) >= batch_size:
            loss = train(model, buffer, batch_size=batch_size, epochs=10, device=device)
            print(f"Training Loss: {loss:.4f}")
            
            summary = {
                'min': int(np.min(game_lengths)),
                'q1': float(np.percentile(game_lengths, 25)),
                'median': float(np.median(game_lengths)),
                'q3': float(np.percentile(game_lengths, 75)),
                'max': int(np.max(game_lengths))
            }
            loss_history.append({'iteration': it, 'loss': loss, 'game_lengths': summary})
            
            with open(loss_history_path, 'w') as f:
                json.dump(loss_history, f)
                
        save_path = f"{checkpoint_dir}/snaky_large_model_it{it}.pt"
        torch.save(model.state_dict(), save_path)
        print(f"Saved Checkpoint to Google Drive! ({save_path})")

if __name__ == "__main__":
    main()
