import sys
import os
import torch
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "big_nn"))
from resnet import SnakyNet
from env import SnakyEnv

print("=== Test 1: SnakyNet 6-channel Forward Pass ===")
model = SnakyNet(in_channels=6, num_resBlocks=2, num_channels=64, board_size=13)
x = torch.randn(4, 6, 13, 13)
p, v = model(x)
print(f"Policy output shape: {p.shape}, Value output shape: {v.shape}")
assert p.shape == (4, 169)
assert v.shape == (4, 1)
print("Forward pass successful!")

print("\n=== Test 2: Threat Computation & Critical Blocking ===")
temp_env = SnakyEnv(size=13)
mask_cells = []
for m in temp_env.win_masks:
    mask_cells.append([i for i in range(169) if (m & (1 << i))])
WIN_MASK_CELLS = np.array(mask_cells, dtype=np.int32)
WEIGHT_LOOKUP = np.array([0, 2, 10, 50, 250, 10000, 0], dtype=np.float32)

target_mask = WIN_MASK_CELLS[5]
maker_cells = target_mask[:5]
winning_cell = target_mask[5]

m_arr = np.zeros(169, dtype=np.float32)
b_arr = np.zeros(169, dtype=np.float32)
m_arr[maker_cells] = 1.0

# Compute threat
mask_b_counts = b_arr[WIN_MASK_CELLS].sum(axis=1)
active_idx = np.where(mask_b_counts == 0)[0]
active_cells = WIN_MASK_CELLS[active_idx]
m_counts = m_arr[active_cells].sum(axis=1).astype(np.int32)
is_crit = bool(np.any(m_counts == 5))
weights = WEIGHT_LOOKUP[m_counts]
empty_mask = (m_arr[active_cells] == 0)
t_map = np.zeros(169, dtype=np.float32)
np.add.at(t_map, active_cells[empty_mask], np.broadcast_to(weights[:, None], active_cells.shape)[empty_mask])

assert is_crit is True
assert np.argmax(t_map) == winning_cell
print(f"Critical threat identified correctly! Winning cell: {winning_cell}, Score: {t_map[winning_cell]}")

# Test policy blending
uniform_policy = np.ones(169, dtype=np.float32) / 169.0
legal_moves = [i for i in range(169) if m_arr[i] == 0]
t_legal = t_map[legal_moves]
crit_mask = (t_legal >= 9000)
p_threat = np.zeros_like(t_legal)
p_threat[crit_mask] = 1.0 / np.sum(crit_mask)
blended = 0.05 * uniform_policy[legal_moves] + 0.95 * p_threat

winning_cell_idx_in_legal = legal_moves.index(winning_cell)
print(f"Blended probability assigned to winning cell {winning_cell}: {blended[winning_cell_idx_in_legal]:.4f}")
assert blended[winning_cell_idx_in_legal] > 0.90
print("Policy blending prioritizes critical block with >90% probability!")

print("\nALL NNv3 TESTS PASSED PERFECTLY!")
