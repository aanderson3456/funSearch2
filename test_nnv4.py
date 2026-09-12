import sys
import os
import time
import torch
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "big_nn"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "co_evolve_champions"))
from resnet import SnakyNet
from env import SnakyEnv
from arena_tournament import ALL_SHAPES_13X13
import maker_top_1_score_112 as fs_maker

print("=" * 60)
print("=== Test 1: SnakyNet 7-channel Forward Pass ===")
print("=" * 60)
model = SnakyNet(in_channels=7, num_resBlocks=2, num_channels=64, board_size=13)
x = torch.randn(4, 7, 13, 13)
p, v = model(x)
print(f"Policy output shape: {p.shape}, Value output shape: {v.shape}")
assert p.shape == (4, 169)
assert v.shape == (4, 1)
print("Test 1 Passed: 7-Channel SnakyNet forward pass successful!")

print("\n" + "=" * 60)
print("=== Test 2: Dual Threat & Fork Detection (Channel 6) ===")
print("=" * 60)
temp_env = SnakyEnv(size=13)
mask_cells = []
for m in temp_env.win_masks:
    mask_cells.append([i for i in range(169) if (m & (1 << i))])
WIN_MASK_CELLS = np.array(mask_cells, dtype=np.int32)
WEIGHT_LOOKUP = np.array([0, 2, 10, 50, 250, 10000, 0], dtype=np.float32)

def compute_threat_planes_single(m_arr, b_arr):
    mask_b_counts = b_arr[WIN_MASK_CELLS].sum(axis=1)
    active_idx = np.where(mask_b_counts == 0)[0]
    if len(active_idx) == 0:
        return np.zeros(169, dtype=np.float32), np.zeros(169, dtype=np.float32), False, np.zeros(169, dtype=np.float32), np.zeros(169, dtype=np.float32)
        
    active_cells = WIN_MASK_CELLS[active_idx]
    m_counts = m_arr[active_cells].sum(axis=1).astype(np.int32)
    empty_mask = (m_arr[active_cells] == 0)
    
    # Single Threat Map (Channel 5)
    is_crit = bool(np.any(m_counts == 5))
    weights = WEIGHT_LOOKUP[m_counts]
    t_map = np.zeros(169, dtype=np.float32)
    np.add.at(t_map, active_cells[empty_mask], np.broadcast_to(weights[:, None], active_cells.shape)[empty_mask])
    
    # Dual Threat / Fork Potential Map (Channel 6)
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

target_pair = None
for i in range(len(WIN_MASK_CELLS)):
    s_i = set(WIN_MASK_CELLS[i])
    for j in range(i+1, min(i+50, len(WIN_MASK_CELLS))):
        s_j = set(WIN_MASK_CELLS[j])
        inter = s_i.intersection(s_j)
        if len(inter) == 1:
            fc = list(inter)[0]
            m_i = list(s_i - {fc})[:4]
            m_j = list(s_j - {fc})[:4]
            if len(set(m_i).intersection(set(m_j))) == 0:
                target_pair = (fc, m_i, m_j)
                break
    if target_pair:
        break

assert target_pair is not None, "Failed to find intersecting shape pair"
fc, m_i, m_j = target_pair
m_arr = np.zeros(169, dtype=np.float32)
b_arr = np.zeros(169, dtype=np.float32)
m_arr[m_i] = 1.0
m_arr[m_j] = 1.0

nt, nf, ic, raw_t, raw_f = compute_threat_planes_single(m_arr, b_arr)
print(f"Fork cell: {fc}, Fork score: {raw_f[fc]}, Normalized fork score: {nf[fc]:.3f}")
assert raw_f[fc] >= 1000.0, f"Expected fork score >= 1000, got {raw_f[fc]}"
assert nf[fc] >= 0.5, f"Expected normalized fork score >= 0.5, got {nf[fc]}"
print("Test 2 Passed: Dual threat fork correctly identified and detected at fork vertex!")

print("\n" + "=" * 60)
print("=== Test 3: Vectorized FunSearch Equivalence ===")
print("=" * 60)
FS_WEIGHTS = np.array([1.0, 4.3, 20.5, 581.6, 25000.0, 1000000.0, 0.0], dtype=np.float32)
MANHATTAN_DIST = np.zeros(169, dtype=np.float32)
for i in range(169):
    y, x = divmod(i, 13)
    MANHATTAN_DIST[i] = (abs(x - 6) + abs(y - 6)) * 0.08

def compute_funsearch_maker_vectorized(m_arr, b_arr):
    mask_b_counts = b_arr[WIN_MASK_CELLS].sum(axis=1)
    active_idx = np.where(mask_b_counts == 0)[0]
    if len(active_idx) == 0:
        return np.zeros(169, dtype=np.float32)
    active_cells = WIN_MASK_CELLS[active_idx]
    m_counts = m_arr[active_cells].sum(axis=1).astype(np.int32)
    weights = FS_WEIGHTS[m_counts]
    empty_mask = (m_arr[active_cells] == 0)
    scores = np.zeros(169, dtype=np.float32)
    active_counts = np.zeros(169, dtype=np.float32)
    np.add.at(scores, active_cells[empty_mask], np.broadcast_to(weights[:, None], active_cells.shape)[empty_mask])
    np.add.at(active_counts, active_cells[empty_mask], 1.0)
    legal_mask = (m_arr == 0) & (b_arr == 0)
    scores[legal_mask] += (active_counts[legal_mask] ** 1.3) * 2.35 - MANHATTAN_DIST[legal_mask]
    scores[~legal_mask] = -1e9
    return scores

np.random.seed(123)
for trial in range(5):
    m_test = np.zeros(169, dtype=np.float32)
    b_test = np.zeros(169, dtype=np.float32)
    rand_moves = np.random.choice(169, 12, replace=False)
    m_test[rand_moves[:6]] = 1.0
    b_test[rand_moves[6:]] = 1.0
    
    vec_s = compute_funsearch_maker_vectorized(m_test, b_test)
    
    m_cells = [(divmod(i, 13)[1] - 6, divmod(i, 13)[0] - 6) for i in rand_moves[:6]]
    b_cells = [(divmod(i, 13)[1] - 6, divmod(i, 13)[0] - 6) for i in rand_moves[6:]]
    b_set = set(b_cells)
    active_shapes = [s for s in ALL_SHAPES_13X13 if not (s & b_set)]
    
    orig_s = np.full(169, -1e9, dtype=np.float32)
    for idx in range(169):
        if m_test[idx] == 0 and b_test[idx] == 0:
            y, x = divmod(idx, 13)
            c = (x - 6, y - 6)
            orig_s[idx] = fs_maker.priority(c, m_cells, b_cells, active_shapes)
            
    diff = np.abs(vec_s - orig_s)
    max_err = np.max(diff[orig_s > -1e8])
    assert max_err < 1e-3, f"Trial {trial} failed with max error {max_err}"

print("Test 3 Passed: Vectorized FunSearch perfectly matches champion heuristic across all trials!")

print("\n" + "=" * 60)
print("=== Test 4: Breaker Fork & Critical Defense Blending ===")
print("=" * 60)
def blend_breaker_policy_v4(policy, legal_moves, t_map, fork_map, is_crit):
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
            p_out = policy.copy()
            p_out[legal_moves] = blended
            return p_out
    
    lethal_fork_mask = (f_legal >= 1000)
    if np.any(lethal_fork_mask):
        p_fork = np.zeros_like(f_legal)
        p_fork[lethal_fork_mask] = 1.0 / np.sum(lethal_fork_mask)
        blended = 0.20 * policy[legal_moves] + 0.80 * p_fork
        p_out = policy.copy()
        p_out[legal_moves] = blended
        return p_out
        
    combined = t_legal + 2.0 * f_legal
    c_sum = np.sum(combined)
    if c_sum > 0:
        p_def = combined / c_sum
        blended = 0.60 * policy[legal_moves] + 0.40 * p_def
        p_out = policy.copy()
        p_out[legal_moves] = blended
        return p_out
        
    return policy

uniform_policy = np.ones(169, dtype=np.float32) / 169.0
legal_moves = [i for i in range(169) if m_arr[i] == 0 and b_arr[i] == 0]
blended = blend_breaker_policy_v4(uniform_policy, legal_moves, raw_t, raw_f, is_crit=False)
print(f"Probability Breaker assigns to blocking fork vertex {fc}: {blended[fc]:.4f} (baseline uniform was {uniform_policy[fc]:.4f})")
assert blended[fc] >= uniform_policy[fc] * 5, f"Expected Breaker fork defense >= 5x baseline, got {blended[fc]}"
print("Test 4 Passed: Breaker vigorously blocks lethal fork vertices!")

print("\n" + "=" * 60)
print("=== Test 5: Full 7-Channel State Encoding & Forward Speed ===")
print("=" * 60)
checkerboard = np.zeros((13, 13), dtype=np.float32)
centrality = np.zeros((13, 13), dtype=np.float32)
center = 6.0
max_dist = 13 / 1.414
for _y in range(13):
    for _x in range(13):
        checkerboard[_y, _x] = 1.0 if (_x + _y) % 2 == 0 else 0.0
        dist = np.sqrt((_x - center)**2 + (_y - center)**2)
        centrality[_y, _x] = max(0.0, 1.0 - (dist / max_dist))

def encode_state_single(m_arr, b_arr, current_player):
    state = np.zeros((7, 13, 13), dtype=np.float32)
    state[0] = m_arr.reshape(13, 13)
    state[1] = b_arr.reshape(13, 13)
    state[2] = 1.0 if current_player == 1 else 0.0
    state[3] = checkerboard
    state[4] = centrality
    norm_t, norm_f, _, _, _ = compute_threat_planes_single(m_arr, b_arr)
    state[5] = norm_t.reshape(13, 13)
    state[6] = norm_f.reshape(13, 13)
    return state

t0 = time.time()
N_ITERS = 100
for _ in range(N_ITERS):
    st = encode_state_single(m_arr, b_arr, 1)
t1 = time.time()
encode_time_ms = ((t1 - t0) / N_ITERS) * 1000
print(f"7-Channel State Encoding Time: {encode_time_ms:.3f} ms/state")
assert encode_time_ms < 5.0, f"Encoding too slow: {encode_time_ms} ms"

batch_tensor = torch.tensor(np.stack([st] * 32), dtype=torch.float32)
model.eval()
with torch.no_grad():
    t0 = time.time()
    for _ in range(50):
        out_p, out_v = model(batch_tensor)
    t1 = time.time()
batch_infer_ms = ((t1 - t0) / 50) * 1000
print(f"ResNet Forward Pass (Batch size 32): {batch_infer_ms:.3f} ms/batch ({batch_infer_ms/32:.3f} ms/state)")

print("\n" + "=" * 60)
print("ALL NNv4 LOCAL TESTS PASSED WITH 100% SUCCESS!")
print("=" * 60)
