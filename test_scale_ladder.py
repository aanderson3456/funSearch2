"""Test Scaling Ladder from 8x8 to 13x13.

Examines:
Does Ultimate Breaker Slayer win across all board sizes N x N from 8 to 13?
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Limit thread contention to keep CPU <= 25%
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

FS2_DIR = Path(__file__).resolve().parent
if str(FS2_DIR) not in sys.path:
    sys.path.insert(0, str(FS2_DIR))

from boost_mock_evolution import load_strategy_from_file, compile_maker_func
from test_10x10_experiment import get_grid_shapes, run_match_arbitrary

def main():
    p_ult = FS2_DIR / "strategies/breaker/rank_9x9_ultimate_slayer.py"
    ult_b_fn = load_strategy_from_file(str(p_ult), "breaker_priority")

    # Load 15-Turn Maker and Decoy Maker
    p_plumb = FS2_DIR / "strategies/maker/rank_plumb_latest.py"
    fn_plumb, _ = compile_maker_func(p_plumb.read_text().split(":\n", 1)[1])

    p_decoy = FS2_DIR / "strategies/maker/rank_9x9_breakthrough.py"
    fn_decoy, _ = compile_maker_func(p_decoy.read_text().split(":\n", 1)[1])

    def two_ply_lookahead_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e11
        test_m = m_set | {c}
        c5 = sum(1 for s in active if sum(1 for p in s if p in test_m) == 5)
        if c5 >= 2:
            return 1e9 * c5
        c4 = sum(1 for s in active if sum(1 for p in s if p in test_m) == 4)
        if c4 >= 3:
            return 1e7 * c4
        elif c4 == 2:
            return 1e5 * c4
        overlap = sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s)
        return float(overlap)

    makers = [
        ("15-Turn 3-Way Fork Maker", fn_plumb),
        ("Breakthrough Decoy Maker", fn_decoy),
        ("2-Ply Compound Threat Maker", two_ply_lookahead_maker),
    ]

    print("=" * 80)
    print("📏 N x N BOARD SCALING LADDER BENCHMARK (N = 8 to 13)")
    print("=" * 80)

    for N in [8, 9, 10, 11, 12, 13]:
        shapes = get_grid_shapes(N, N)
        max_turns = (N * N) // 2 + 1
        print(f"\n--- BOARD {N}x{N} ({N*N} cells, {len(shapes)} shapes, max {max_turns} turns) ---")
        for m_name, m_fn in makers:
            res = run_match_arbitrary(m_fn, ult_b_fn, shapes, max_turns=max_turns)
            winner = "Maker" if res["maker_won"] else "Breaker"
            turns = res["turns"]
            max_c = res["max_cells_in_shape"]
            status = "TOTAL DENIAL 🛡️" if not res["maker_won"] else "MAKER WIN ⚠️"
            print(f"  vs {m_name:<30}: {winner:<7} in {turns:2d} turns (Max cells: {max_c}/6) -> {status}")

if __name__ == "__main__":
    main()
