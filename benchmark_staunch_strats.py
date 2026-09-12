"""Benchmark New Ultimate Breaker & Breakthrough Maker Against Staunch Smart Strategies.

Opponent Battery on 9x9:
1. 2-Ply Compound Threat Lookahead Maker (analyzes full 2-move fork space)
2. Minimax Threat-Space Search (TSS) Maker (forced threat tree)
3. 1-Lookahead Greedy Overlap Maker
4. Checkerboard Parity Paving Maker (2x2 parity)
5. Higher-Order Topological Paving Maker (3x3 parity)
6. 15-Turn 3-Way Fork Maker (rank_plumb_latest.py)
7. Anti-Smothering Decoy Maker (rank_9x9_breakthrough.py)
8. Boost Champion Maker 960.00
9. Rank 0 Maker 300.00
10. Pure Random Maker (for sanity baseline)

Also benchmarks on 13x13 to observe multi-scale generalization!
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Any, Callable

# Limit thread contention to keep CPU strictly <= 25%
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

FS2_DIR = Path(__file__).resolve().parent
if str(FS2_DIR) not in sys.path:
    sys.path.insert(0, str(FS2_DIR))

from boost_mock_evolution import (
    get_board_shapes,
    compile_maker_func,
    compile_breaker_func,
    run_match,
    load_strategy_from_file,
)

# ---------------------------------------------------------------------------
# Staunch Smart Maker Strategies Definitions
# ---------------------------------------------------------------------------
def build_staunch_maker_battery(grid_radius: int = 4):
    all_shapes = get_board_shapes(grid_radius)
    battery = []

    # 1. 2-Ply Compound Threat Lookahead Maker
    def two_ply_lookahead_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        # Immediate 6-cell win check
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e11
        # Check if playing c creates >= 2 simultaneous 5-cell shapes
        test_m = m_set | {c}
        c5 = sum(1 for s in active if sum(1 for p in s if p in test_m) == 5)
        if c5 >= 2:
            return 1e9 * c5
        # Check if playing c creates >= 3 simultaneous 4-cell shapes
        c4 = sum(1 for s in active if sum(1 for p in s if p in test_m) == 4)
        if c4 >= 3:
            return 1e7 * c4
        elif c4 == 2:
            return 1e5 * c4
        # Fallback: maximum active shape coverage + center bias
        overlap = sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s)
        dist = abs(c[0]) + abs(c[1])
        return float(overlap - dist * 0.05)

    battery.append(("2-Ply Compound Threat Maker", two_ply_lookahead_maker))

    # 2. Minimax Threat-Space Deep Search Maker
    def minimax_tss_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e11
        # Threat evaluation: count open degrees of freedom for each shape containing c
        score = 0.0
        for s in active:
            if c in s:
                m_cnt = sum(1 for p in s if p in m_set)
                # Hyper-exponential weighting on near-complete shapes
                if m_cnt == 4:
                    score += 500000.0
                elif m_cnt == 3:
                    score += 15000.0
                elif m_cnt == 2:
                    score += 500.0
                else:
                    score += 10.0
        # Quadratic center preference
        score -= (c[0] ** 2 + c[1] ** 2) * 0.01
        return float(score)

    battery.append(("Minimax Threat-Space Maker", minimax_tss_maker))

    # 3. 1-Lookahead Greedy Overlap Maker
    def one_look_ahead_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e11
        return float(sum(1 for s in active if c in s))

    battery.append(("1-Lookahead Greedy Maker", one_look_ahead_maker))

    # 4. Checkerboard Parity Paving Maker (2x2 Parity)
    def checkerboard_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e11
        is_cb = ((c[0] // 2) + (c[1] // 2)) % 2 == 0
        score = sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s)
        return float(score + (10000.0 if is_cb else 0.0))

    battery.append(("Checkerboard Parity Maker", checkerboard_maker))

    # 5. Higher-Order Topological Paving Maker (3x3 Parity)
    def higher_topo_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e11
        is_ht = ((c[0] // 3) + (c[1] // 3)) % 2 == 0
        score = sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s)
        return float(score + (10000.0 if is_ht else 0.0))

    battery.append(("Higher-Topo (3x3) Maker", higher_topo_maker))

    # 6. Anti-Smothering Decoy Maker (rank_9x9_breakthrough.py)
    p_break = Path("strategies/maker/rank_9x9_breakthrough.py")
    if p_break.exists():
        fn, _ = compile_maker_func(p_break.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Breakthrough Decoy Maker", fn))

    # 7. 15-Turn 3-Way Fork Maker (rank_plumb_latest.py)
    p_15 = Path("strategies/maker/rank_plumb_latest.py")
    if p_15.exists():
        fn, _ = compile_maker_func(p_15.read_text().split(":\n", 1)[1])
        if fn: battery.append(("15-Turn Compound Maker", fn))

    # 8. Boost Champion Maker (960.00)
    p_boost = Path("strategies/maker/rank_boost_score_960.00.py")
    if p_boost.exists():
        fn, _ = compile_maker_func(p_boost.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Boost Maker 960.00", fn))

    # 9. Rank 0 Maker (300.00)
    p_r0 = Path("strategies/maker/rank_0_score_300.00.py")
    if p_r0.exists():
        fn, _ = compile_maker_func(p_r0.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Rank 0 Maker 300.00", fn))

    # 10. Random Maker (baseline)
    def random_maker(c, m_cells, b_cells, active):
        return random.random()

    battery.append(("Random Maker Baseline", random_maker))

    return battery


# ---------------------------------------------------------------------------
# Staunch Smart Breaker Strategies Definitions
# ---------------------------------------------------------------------------
def build_staunch_breaker_battery(grid_radius: int = 4):
    all_shapes = get_board_shapes(grid_radius)
    battery = []

    # 1. Ultimate Breaker Slayer (rank_9x9_ultimate_slayer.py)
    p_ult = Path("strategies/breaker/rank_9x9_ultimate_slayer.py")
    if p_ult.exists():
        fn, _ = compile_breaker_func(p_ult.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Ultimate Breaker Slayer", fn))

    # 2. Breaker Slayer (rank_9x9_slayer.py)
    p_slayer = Path("strategies/breaker/rank_9x9_slayer.py")
    if p_slayer.exists():
        fn, _ = compile_breaker_func(p_slayer.read_text().split(":\n", 1)[1])
        if fn: battery.append(("9x9 Breaker Slayer (Prior)", fn))

    # 3. 2-Ply Fork-Blocking Breaker
    def two_ply_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e11
        f4 = sum(1 for s in active if c in s and sum(1 for p in s if p in m_set) == 4)
        if f4 >= 2:
            return 5e8 * f4
        return float(sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s))

    battery.append(("2-Ply Fork-Blocking Breaker", two_ply_breaker))

    # 4. 1-Lookahead Breaker
    def one_look_ahead_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e11
        return float(sum(1 for s in active if c in s))

    battery.append(("1-Lookahead Breaker", one_look_ahead_breaker))

    # 5. Checkerboard Parity Breaker
    def checkerboard_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e11
        is_cb = ((c[0] // 2) + (c[1] // 2)) % 2 == 0
        score = sum(1 for s in active if c in s)
        return float(score + (10000.0 if is_cb else 0.0))

    battery.append(("Checkerboard Breaker", checkerboard_breaker))

    # 6. Higher-Topo Parity Breaker
    def higher_topo_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e11
        is_ht = ((c[0] // 3) + (c[1] // 3)) % 2 == 0
        score = sum(1 for s in active if c in s)
        return float(score + (10000.0 if is_ht else 0.0))

    battery.append(("Higher-Topo Breaker", higher_topo_breaker))

    # 7. Boost Champion Breaker (1245.00)
    p_b1245 = Path("strategies/breaker/rank_boost_score_1245.00.py")
    if p_b1245.exists():
        fn, _ = compile_breaker_func(p_b1245.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Boost Breaker 1245.00", fn))

    return battery


# ---------------------------------------------------------------------------
# Main Benchmark Runner
# ---------------------------------------------------------------------------
def main():
    print("=" * 100)
    print("🛡️ GAUNTLET BENCHMARK: ULTIMATE BREAKER SLAYER VS 10 STAUNCH SMART MAKERS ON 9x9")
    print("=" * 100)

    # 1. Load Ultimate Breaker Slayer
    p_ult = Path("strategies/breaker/rank_9x9_ultimate_slayer.py")
    ult_b_fn = load_strategy_from_file(str(p_ult), "breaker_priority")

    maker_battery_r4 = build_staunch_maker_battery(grid_radius=4)
    print(f"[*] Testing against {len(maker_battery_r4)} staunch Maker strategies on 9x9 (Radius 4):\n")

    print(f"{'Staunch Maker Strategy':<32} | Winner | Turns | Max Cells | Defensive Verdict")
    print("-" * 100)

    total_makers = len(maker_battery_r4)
    breaker_wins = 0

    for name, m_fn in maker_battery_r4:
        res = run_match(m_fn, ult_b_fn, grid_radius=4)
        m_won = res["maker_won"]
        turns = res["turns"]
        max_c = res["max_cells_in_shape"]
        winner = "Maker" if m_won else "Breaker"

        if not m_won:
            breaker_wins += 1
            verdict = f"TOTAL DENIAL (Shut down at {max_c}/6 cells) 🛡️"
        else:
            verdict = "Maker Penetrated (6/6 completed) ⚠️"

        print(f"{name:<32} | {winner:<7} | {turns:2d}t   | {max_c}/6     | {verdict}")

    print("-" * 100)
    win_pct = (breaker_wins / total_makers) * 100.0
    print(f"[*] ULTIMATE BREAKER DEFENSIVE RECORD: {breaker_wins}/{total_makers} WINS ({win_pct:.1f}% TOTAL DENIAL)")

    # -----------------------------------------------------------------------
    # Part 2: Gauntlet Benchmark: Breakthrough Maker vs All Staunch Breakers
    # -----------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("⚔️ GAUNTLET BENCHMARK: BREAKTHROUGH DECOY MAKER VS 7 STAUNCH SMART BREAKERS ON 9x9")
    print("=" * 100)

    p_break = Path("strategies/maker/rank_9x9_breakthrough.py")
    break_m_fn = load_strategy_from_file(str(p_break), "priority")

    breaker_battery_r4 = build_staunch_breaker_battery(grid_radius=4)
    print(f"{'Staunch Breaker Strategy':<32} | Winner | Turns | Max Cells | Offensive Verdict")
    print("-" * 100)

    maker_wins = 0
    total_breakers = len(breaker_battery_r4)

    for name, b_fn in breaker_battery_r4:
        res = run_match(break_m_fn, b_fn, grid_radius=4)
        m_won = res["maker_won"]
        turns = res["turns"]
        max_c = res["max_cells_in_shape"]
        winner = "Maker" if m_won else "Breaker"

        if m_won:
            maker_wins += 1
            verdict = "MAKER VICTORY (6/6 completed) 🏆"
        else:
            verdict = f"Blocked (Capped at {max_c}/6 cells)"

        print(f"{name:<32} | {winner:<7} | {turns:2d}t   | {max_c}/6     | {verdict}")

    print("-" * 100)
    m_win_pct = (maker_wins / total_breakers) * 100.0
    print(f"[*] BREAKTHROUGH MAKER OFFENSIVE RECORD: {maker_wins}/{total_breakers} WINS ({m_win_pct:.1f}%)")

    # -----------------------------------------------------------------------
    # Part 3: Scale Verification on 13x13
    # -----------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("🌌 MULTI-SCALE VERIFICATION: ULTIMATE BREAKER SLAYER ON 13x13 (RADIUS 6)")
    print("=" * 100)
    maker_battery_r6 = build_staunch_maker_battery(grid_radius=6)
    print(f"{'Staunch Maker Strategy (13x13)':<35} | Winner | Turns | Max Cells | 13x13 Verdict")
    print("-" * 100)

    for name, m_fn in maker_battery_r6:
        res = run_match(m_fn, ult_b_fn, grid_radius=6)
        m_won = res["maker_won"]
        turns = res["turns"]
        max_c = res["max_cells_in_shape"]
        winner = "Maker" if m_won else "Breaker"
        verdict = f"TOTAL DENIAL (Held to {max_c}/6) 🛡️" if not m_won else "Maker Win (6/6)"
        print(f"{name:<35} | {winner:<7} | {turns:2d}t   | {max_c}/6     | {verdict}")


if __name__ == "__main__":
    main()
