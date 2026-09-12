"""Neural Network v4 (Iteration 223) vs. FunSearch Heuristic Champions.

Showdown on 13x13 Board (169 cells, 864 valid Snaky shapes):
1. Grandmaster Maker vs. SnakyNet v4 Breaker
2. SnakyNet v4 Maker vs. Grandmaster Breaker
3. 15-Turn 3-Way Fork Maker vs. SnakyNet v4 Breaker
4. Breakthrough Decoy Maker vs. SnakyNet v4 Breaker
5. SnakyNet v4 Maker vs. Ultimate Slayer Breaker

Uses .venv/bin/python with PyTorch, SnakyNet 16-block 256-channel architecture,
and 7-channel state encoding with critical threat and fork blending.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
import numpy as np
import torch

# Ensure thread limit CPU <= 25%
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

FS2_DIR = Path(__file__).resolve().parent
if str(FS2_DIR) not in sys.path:
    sys.path.insert(0, str(FS2_DIR))
sys.path.append(str(FS2_DIR / "big_nn"))

from resnet import SnakyNet
from env import SnakyEnv
from boost_mock_evolution import load_strategy_from_file, compile_maker_func, compile_breaker_func

# ---------------------------------------------------------------------------
# Setup 13x13 Win Masks & Threat Computation (From test_nnv4.py)
# ---------------------------------------------------------------------------
temp_env = SnakyEnv(size=13)
mask_cells = []
for m in temp_env.win_masks:
    mask_cells.append([i for i in range(169) if (m & (1 << i))])
WIN_MASK_CELLS = np.array(mask_cells, dtype=np.int32)
WEIGHT_LOOKUP = np.array([0, 2, 10, 50, 250, 10000, 0], dtype=np.float32)

checkerboard = np.zeros((13, 13), dtype=np.float32)
centrality = np.zeros((13, 13), dtype=np.float32)
center = 6.0
max_dist = 13 / 1.414
for _y in range(13):
    for _x in range(13):
        checkerboard[_y, _x] = 1.0 if (_x + _y) % 2 == 0 else 0.0
        dist = np.sqrt((_x - center)**2 + (_y - center)**2)
        centrality[_y, _x] = max(0.0, 1.0 - (dist / max_dist))

def compute_threat_planes_single(m_arr, b_arr):
    mask_b_counts = b_arr[WIN_MASK_CELLS].sum(axis=1)
    active_idx = np.where(mask_b_counts == 0)[0]
    if len(active_idx) == 0:
        return np.zeros(169, dtype=np.float32), np.zeros(169, dtype=np.float32), False, np.zeros(169, dtype=np.float32), np.zeros(169, dtype=np.float32)
        
    active_cells = WIN_MASK_CELLS[active_idx]
    m_counts = m_arr[active_cells].sum(axis=1).astype(np.int32)
    empty_mask = (m_arr[active_cells] == 0)
    
    is_crit = bool(np.any(m_counts == 5))
    weights = WEIGHT_LOOKUP[m_counts]
    t_map = np.zeros(169, dtype=np.float32)
    np.add.at(t_map, active_cells[empty_mask], np.broadcast_to(weights[:, None], active_cells.shape)[empty_mask])
    
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

def blend_breaker_policy(policy, legal_moves, t_map, fork_map, is_crit):
    if len(legal_moves) == 0:
        return policy
    t_legal = t_map[legal_moves]
    f_legal = fork_map[legal_moves]
    
    if is_crit:
        crit_mask = (t_legal >= 9000)
        if np.any(crit_mask):
            p_threat = np.zeros_like(t_legal)
            p_threat[crit_mask] = 1.0 / np.sum(crit_mask)
            blended = 0.02 * policy[legal_moves] + 0.98 * p_threat
            p_out = policy.copy()
            p_out[legal_moves] = blended
            return p_out
            
    lethal_fork_mask = (f_legal >= 1000)
    if np.any(lethal_fork_mask):
        p_fork = np.zeros_like(f_legal)
        p_fork[lethal_fork_mask] = 1.0 / np.sum(lethal_fork_mask)
        blended = 0.10 * policy[legal_moves] + 0.90 * p_fork
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

# ---------------------------------------------------------------------------
# All 13x13 Snaky Shapes for FunSearch Evaluation
# ---------------------------------------------------------------------------
_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]
def get_all_shapes_13x13() -> list[frozenset[tuple[int, int]]]:
    orientations = set()
    for rot in range(4):
        for ref in range(2):
            s = _BASE_SNAKY
            if ref: s = [(-p[0], p[1]) for p in s]
            for _ in range(rot): s = [(p[1], -p[0]) for p in s]
            mx = min(p[0] for p in s)
            my = min(p[1] for p in s)
            normalized = tuple(sorted((p[0] - mx, p[1] - my) for p in s))
            orientations.add(normalized)
    shapes = []
    for ori in orientations:
        max_ox = max(p[0] for p in ori)
        max_oy = max(p[1] for p in ori)
        for dx in range(13 - max_ox):
            for dy in range(13 - max_oy):
                shapes.append(frozenset((x + dx, y + dy) for x, y in ori))
    return list(set(shapes))

ALL_SHAPES_13X13 = get_all_shapes_13x13()

# ---------------------------------------------------------------------------
# Match Runners
# ---------------------------------------------------------------------------
def run_fs_maker_vs_nn_breaker(fs_maker_fn, model, device):
    """FunSearch Maker (1st) vs. Neural Network Breaker (2nd) on 13x13."""
    m_cells, b_cells = [], []
    m_arr = np.zeros(169, dtype=np.float32)
    b_arr = np.zeros(169, dtype=np.float32)
    maker_won = False
    
    for turn in range(85):
        m_set, b_set = set(m_cells), set(b_cells)
        active = [tuple(s) for s in ALL_SHAPES_13X13 if not (s & b_set)]
        cands = set(p for s in active for p in s if p not in m_set and p not in b_set)
        if not cands: break
        
        # Maker move (FunSearch heuristic)
        # Adapt [0..12] coordinates to centered [-6..6]
        def centered_cand(c):
            c_cent = (c[0] - 6, c[1] - 6)
            m_cent = [(x - 6, y - 6) for x, y in m_cells]
            b_cent = [(x - 6, y - 6) for x, y in b_cells]
            act_cent = [tuple((x - 6, y - 6) for x, y in s) for s in active]
            return fs_maker_fn(c_cent, m_cent, b_cent, act_cent)
            
        best_m = max(cands, key=centered_cand)
        m_cells.append(best_m)
        m_set.add(best_m)
        m_idx = best_m[1] * 13 + best_m[0]
        m_arr[m_idx] = 1.0
        
        if any(s.issubset(m_set) for s in ALL_SHAPES_13X13):
            maker_won = True
            break
            
        # Breaker move (Neural Network with threat blending)
        active_b = [tuple(s) for s in ALL_SHAPES_13X13 if not (s & b_set)]
        if not active_b: break
        
        legal_moves = [i for i in range(169) if m_arr[i] == 0 and b_arr[i] == 0]
        if not legal_moves: break
        
        state_np = encode_state_single(m_arr, b_arr, current_player=-1)
        state_t = torch.tensor(state_np, dtype=torch.float32, device=device).unsqueeze(0)
        with torch.no_grad():
            p_out, v_out = model(state_t)
            raw_policy = torch.softmax(p_out[0], dim=-1).cpu().numpy()
            
        _, _, is_crit, raw_t, raw_f = compute_threat_planes_single(m_arr, b_arr)
        blended_p = blend_breaker_policy(raw_policy, legal_moves, raw_t, raw_f, is_crit)
        
        best_b_idx = legal_moves[np.argmax(blended_p[legal_moves])]
        best_b = (best_b_idx % 13, best_b_idx // 13)
        b_cells.append(best_b)
        b_set.add(best_b)
        b_arr[best_b_idx] = 1.0
        
    m_set = set(m_cells)
    max_c = max((len(s & m_set) for s in ALL_SHAPES_13X13), default=0)
    return {
        "maker_won": maker_won,
        "turns": len(m_cells),
        "max_cells": max_c,
        "maker_cells": m_cells,
        "breaker_cells": b_cells,
    }


def run_nn_maker_vs_fs_breaker(model, fs_breaker_fn, device):
    """Neural Network Maker (1st) vs. FunSearch Breaker (2nd) on 13x13."""
    m_cells, b_cells = [], []
    m_arr = np.zeros(169, dtype=np.float32)
    b_arr = np.zeros(169, dtype=np.float32)
    maker_won = False
    
    for turn in range(85):
        m_set, b_set = set(m_cells), set(b_cells)
        active = [tuple(s) for s in ALL_SHAPES_13X13 if not (s & b_set)]
        if not active: break
        
        legal_moves = [i for i in range(169) if m_arr[i] == 0 and b_arr[i] == 0]
        if not legal_moves: break
        
        # NN Maker move
        state_np = encode_state_single(m_arr, b_arr, current_player=1)
        state_t = torch.tensor(state_np, dtype=torch.float32, device=device).unsqueeze(0)
        with torch.no_grad():
            p_out, v_out = model(state_t)
            raw_policy = torch.softmax(p_out[0], dim=-1).cpu().numpy()
            
        best_m_idx = legal_moves[np.argmax(raw_policy[legal_moves])]
        best_m = (best_m_idx % 13, best_m_idx // 13)
        m_cells.append(best_m)
        m_set.add(best_m)
        m_arr[best_m_idx] = 1.0
        
        if any(s.issubset(m_set) for s in ALL_SHAPES_13X13):
            maker_won = True
            break
            
        # FunSearch Breaker move
        active_b = [tuple(s) for s in ALL_SHAPES_13X13 if not (s & b_set)]
        cands_b = set(p for s in active_b for p in s if p not in m_set and p not in b_set)
        if not cands_b: break
        
        def centered_cand_b(c):
            c_cent = (c[0] - 6, c[1] - 6)
            m_cent = [(x - 6, y - 6) for x, y in m_cells]
            b_cent = [(x - 6, y - 6) for x, y in b_cells]
            act_cent = [tuple((x - 6, y - 6) for x, y in s) for s in active_b]
            return fs_breaker_fn(c_cent, m_cent, b_cent, act_cent)
            
        best_b = max(cands_b, key=centered_cand_b)
        b_cells.append(best_b)
        b_set.add(best_b)
        b_idx = best_b[1] * 13 + best_b[0]
        b_arr[b_idx] = 1.0
        
    m_set = set(m_cells)
    max_c = max((len(s & m_set) for s in ALL_SHAPES_13X13), default=0)
    return {
        "maker_won": maker_won,
        "turns": len(m_cells),
        "max_cells": max_c,
        "maker_cells": m_cells,
        "breaker_cells": b_cells,
    }


def main():
    print("=" * 100)
    print("🤖⚡ CLASH OF TITANS: SNAKYNET V4 (18.98M PARAMS, IT223) VS. EVOLVED FUNSEARCH CHAMPIONS")
    print("=" * 100)
    
    device = torch.device("cpu")
    ckpt_path = "/Users/austinanderson/Library/CloudStorage/GoogleDrive-pianowater@gmail.com/My Drive/SnakyNet_v4_Checkpoints/snaky_large_model_it223.pt"
    
    print("[*] Loading 16-Block SnakyNet v4 from checkpoint...")
    model = SnakyNet(in_channels=7, num_resBlocks=16, num_channels=256, board_size=13)
    state = torch.load(ckpt_path, map_location=device)
    model.load_state_dict(state)
    model.eval()
    print("[+] Model successfully loaded!\n")
    
    # Load FunSearch Heuristic Champions
    p_gm_maker = FS2_DIR / "strategies/maker/rank_9x9_grandmaster_maker.py"
    fn_gm_maker = load_strategy_from_file(str(p_gm_maker), "priority")
    
    p_gm_breaker = FS2_DIR / "strategies/breaker/rank_9x9_grandmaster_breaker.py"
    fn_gm_breaker = load_strategy_from_file(str(p_gm_breaker), "breaker_priority")
    
    p_plumb_maker = FS2_DIR / "strategies/maker/rank_plumb_latest.py"
    fn_plumb_maker = load_strategy_from_file(str(p_plumb_maker), "priority")
    
    p_decoy_maker = FS2_DIR / "strategies/maker/rank_9x9_breakthrough.py"
    fn_decoy_maker = load_strategy_from_file(str(p_decoy_maker), "priority")
    
    p_ult_breaker = FS2_DIR / "strategies/breaker/rank_9x9_ultimate_slayer.py"
    fn_ult_breaker = load_strategy_from_file(str(p_ult_breaker), "breaker_priority")
    
    matches = [
        ("Grandmaster Maker (Honed)", "SnakyNet v4 Breaker (it223)", lambda: run_fs_maker_vs_nn_breaker(fn_gm_maker, model, device)),
        ("15-Turn 3-Way Fork Maker", "SnakyNet v4 Breaker (it223)", lambda: run_fs_maker_vs_nn_breaker(fn_plumb_maker, model, device)),
        ("Breakthrough Decoy Maker", "SnakyNet v4 Breaker (it223)", lambda: run_fs_maker_vs_nn_breaker(fn_decoy_maker, model, device)),
        ("SnakyNet v4 Maker (it223)", "Grandmaster Breaker (Honed)", lambda: run_nn_maker_vs_fs_breaker(model, fn_gm_breaker, device)),
        ("SnakyNet v4 Maker (it223)", "Ultimate Slayer Breaker", lambda: run_nn_maker_vs_fs_breaker(model, fn_ult_breaker, device)),
    ]
    
    print(f"{'Matchup':<60} | {'Winner':<10} | {'Turns':<6} | {'Max Cells'} | {'Verdict'}")
    print("-" * 105)
    
    for m_name, b_name, run_fn in matches:
        title = f"{m_name} vs {b_name}"
        t0 = time.time()
        res = run_fn()
        elapsed = time.time() - t0
        
        winner = m_name if res["maker_won"] else b_name
        winner_short = "Maker" if res["maker_won"] else "Breaker"
        turns = res["turns"]
        max_c = res["max_cells"]
        verdict = "MAKER WIN (6/6) ⚔️" if res["maker_won"] else f"DENIAL (Capped at {max_c}/6) 🛡️"
        
        print(f"{title:<60} | {winner_short:<10} | {turns:2d}t   | {max_c}/6     | {verdict} ({elapsed:.1f}s)")
        
    print("-" * 105)
    print("Tournament Completed.")

if __name__ == "__main__":
    main()
