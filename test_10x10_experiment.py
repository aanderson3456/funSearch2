"""Test 10x10 Board Dynamics and Tiling Generalization.

Investigate:
1. Exact Snaky shapes on 10x10 grid (0..9, 0..9) vs 9x9 (-4..4, -4..4).
2. 2x2 block partition verification on 10x10:
   - 10x10 tiles evenly into 25 blocks of 2x2.
   - For every Snaky hexomino placement in 10x10, how many cells land in each 2x2 block?
3. Benchmark Ultimate Breaker Slayer (rank_9x9_ultimate_slayer.py) and
   2x2 Parity / Tiling Breakers against the 10-Maker Staunch Gauntlet on 10x10!
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, Callable

# Limit thread contention to keep CPU <= 25%
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

FS2_DIR = Path(__file__).resolve().parent
if str(FS2_DIR) not in sys.path:
    sys.path.insert(0, str(FS2_DIR))

from boost_mock_evolution import (
    compile_maker_func,
    compile_breaker_func,
    load_strategy_from_file,
)
from benchmark_staunch_strats import build_staunch_maker_battery

_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]

def get_grid_shapes(width: int = 10, height: int = 10) -> list[frozenset[tuple[int, int]]]:
    """Generates all Snaky placements within [0, width-1] x [0, height-1]."""
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
        max_ox = max(p[0] for p in ori)
        max_oy = max(p[1] for p in ori)
        for dx in range(width - max_ox):
            for dy in range(height - max_oy):
                translated = tuple(sorted((x + dx, y + dy) for x, y in ori))
                shapes.append(frozenset(translated))

    return list(set(shapes))

def run_match_arbitrary(
    maker_func: Callable,
    breaker_func: Callable,
    all_shapes: list[frozenset[tuple[int, int]]],
    max_turns: int = 50,
) -> dict[str, Any]:
    """Simulates a full match between Maker and Breaker on an arbitrary shape set."""
    m_cells, b_cells = [], []
    maker_won = False

    for turn in range(max_turns):
        m_set, b_set = set(m_cells), set(b_cells)

        for s in all_shapes:
            if s.issubset(m_set):
                maker_won = True
                break
        if maker_won:
            break

        active = [tuple(s) for s in all_shapes if not (s & b_set)]
        if not active:
            break

        candidates = set()
        for s in active:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates.add(p)
        if not candidates:
            break

        best_m = max(candidates, key=lambda c: maker_func(c, m_cells, b_cells, active))
        m_cells.append(best_m)
        m_set.add(best_m)

        for s in all_shapes:
            if s.issubset(m_set):
                maker_won = True
                break
        if maker_won:
            break

        active_b = [tuple(s) for s in all_shapes if not (s & b_set)]
        if not active_b:
            break

        candidates_b = set()
        for s in active_b:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates_b.add(p)
        if not candidates_b:
            break

        best_b = max(candidates_b, key=lambda c: breaker_func(c, m_cells, b_cells, active_b))
        b_cells.append(best_b)

    m_set = set(m_cells)
    max_cells = max((len(s & m_set) for s in all_shapes), default=0)
    return {
        "maker_won": maker_won,
        "turns": len(m_cells),
        "max_cells_in_shape": max_cells,
        "total_maker_cells": len(m_cells),
        "total_breaker_cells": len(b_cells),
    }

def main():
    print("=" * 90)
    print("🔬 10x10 BOARD DYNAMICS & TILING GENERALIZATION STUDY")
    print("=" * 90)

    shapes_8x8 = get_grid_shapes(8, 8)
    shapes_9x9 = get_grid_shapes(9, 9)
    shapes_10x10 = get_grid_shapes(10, 10)
    shapes_13x13 = get_grid_shapes(13, 13)

    print(f"Board 8x8:   64 cells,  {len(shapes_8x8):4d} valid Snaky placements")
    print(f"Board 9x9:   81 cells,  {len(shapes_9x9):4d} valid Snaky placements")
    print(f"Board 10x10: 100 cells, {len(shapes_10x10):4d} valid Snaky placements")
    print(f"Board 13x13: 169 cells, {len(shapes_13x13):4d} valid Snaky placements\n")

    # 1. Verify 2x2 Block Partition on 10x10
    print("--- STEP 1: 2x2 Block Partition Verification on 10x10 ---")
    blocks = {}
    for bx in range(5):
        for by in range(5):
            b_cells = frozenset({
                (2 * bx, 2 * by), (2 * bx + 1, 2 * by),
                (2 * bx, 2 * by + 1), (2 * bx + 1, 2 * by + 1)
            })
            blocks[(bx, by)] = b_cells

    print(f"Total 2x2 blocks covering 10x10 exactly: {len(blocks)} (100 cells total, 0 overlap, 0 missing)")

    min_shared = 999
    collision_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for s in shapes_10x10:
        max_in_single_block = max(len(s & b) for b in blocks.values())
        min_shared = min(min_shared, max_in_single_block)
        collision_counts[max_in_single_block] = collision_counts.get(max_in_single_block, 0) + 1

    print(f"Minimum maximum-overlap with any 2x2 block across all 10x10 shapes: {min_shared}")
    for k, v in sorted(collision_counts.items()):
        pct = (v / len(shapes_10x10)) * 100
        print(f"  Shapes with max {k} cells in a single 2x2 block: {v:4d} ({pct:5.1f}%)")

    if min_shared >= 2:
        print("  ==> THEOREM HOLDS ON 10x10: 100% of Snaky placements share >= 2 cells in at least one 2x2 block!\n")
    else:
        print("  ==> Exception found!\n")

    # 2. Benchmark Ultimate Breaker Slayer on 10x10 against 10 Staunch Makers
    print("--- STEP 2: Ultimate Breaker Slayer vs Staunch Makers on 10x10 ---")
    p_ult = FS2_DIR / "strategies/breaker/rank_9x9_ultimate_slayer.py"
    ult_b_fn = load_strategy_from_file(str(p_ult), "breaker_priority")

    def build_10x10_maker_battery():
        battery = []

        # 1. 2-Ply Compound Threat Lookahead Maker
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
            dist = abs(c[0] - 4.5) + abs(c[1] - 4.5)
            return float(overlap - dist * 0.05)
        battery.append(("2-Ply Compound Threat Maker", two_ply_lookahead_maker))

        # 2. Minimax Threat-Space Deep Search Maker
        def minimax_tss_maker(c, m_cells, b_cells, active):
            m_set = set(m_cells)
            for s in active:
                if sum(1 for p in s if p in m_set) == 5 and c in s:
                    return 1e11
            score = 0.0
            for s in active:
                if c in s:
                    m_cnt = sum(1 for p in s if p in m_set)
                    if m_cnt == 4: score += 500000.0
                    elif m_cnt == 3: score += 15000.0
                    elif m_cnt == 2: score += 500.0
                    else: score += 10.0
            score -= ((c[0] - 4.5) ** 2 + (c[1] - 4.5) ** 2) * 0.01
            return float(score)
        battery.append(("Minimax TSS Deep Search Maker", minimax_tss_maker))

        # 3. 1-Lookahead Greedy Overlap Maker
        def one_look_ahead_maker(c, m_cells, b_cells, active):
            m_set = set(m_cells)
            for s in active:
                if sum(1 for p in s if p in m_set) == 5 and c in s:
                    return 1e11
            return float(sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s))
        battery.append(("1-Lookahead Greedy Maker", one_look_ahead_maker))

        # 4. Checkerboard Parity Paving Maker (2x2)
        def checkerboard_maker(c, m_cells, b_cells, active):
            m_set = set(m_cells)
            for s in active:
                if sum(1 for p in s if p in m_set) == 5 and c in s:
                    return 1e11
            is_cb = ((c[0] // 2) + (c[1] // 2)) % 2 == 0
            score = sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s)
            return float(score + (10000.0 if is_cb else 0.0))
        battery.append(("Checkerboard Parity (2x2) Maker", checkerboard_maker))

        # 5. Higher-Order Topological Paving Maker (3x3)
        def higher_topo_maker(c, m_cells, b_cells, active):
            m_set = set(m_cells)
            for s in active:
                if sum(1 for p in s if p in m_set) == 5 and c in s:
                    return 1e11
            is_ht = ((c[0] // 3) + (c[1] // 3)) % 2 == 0
            score = sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s)
            return float(score + (10000.0 if is_ht else 0.0))
        battery.append(("Higher-Order Topo (3x3) Maker", higher_topo_maker))

        # 6. 15-Turn 3-Way Compound Threat Maker (rank_plumb_latest.py)
        p_plumb = FS2_DIR / "strategies/maker/rank_plumb_latest.py"
        if p_plumb.exists():
            body = p_plumb.read_text().split(":\n", 1)[1]
            fn, _ = compile_maker_func(body)
            if fn: battery.append(("15-Turn 3-Way Fork Maker", fn))

        # 7. Breakthrough Decoy Maker (rank_9x9_breakthrough.py)
        p_bk = FS2_DIR / "strategies/maker/rank_9x9_breakthrough.py"
        if p_bk.exists():
            body = p_bk.read_text().split(":\n", 1)[1]
            fn, _ = compile_maker_func(body)
            if fn: battery.append(("Breakthrough Decoy Maker", fn))

        # 8. Boost Champion Maker 960.00
        p_m960 = FS2_DIR / "strategies/maker/rank_boost_score_960.00.py"
        if p_m960.exists():
            body = p_m960.read_text().split(":\n", 1)[1]
            fn, _ = compile_maker_func(body)
            if fn: battery.append(("Boost Champion Maker 960.00", fn))

        # 9. Rank 0 Maker 300.00
        p_m300 = FS2_DIR / "strategies/maker/rank_boost_score_300.00.py"
        if p_m300.exists():
            body = p_m300.read_text().split(":\n", 1)[1]
            fn, _ = compile_maker_func(body)
            if fn: battery.append(("Rank 0 Maker 300.00", fn))

        # 10. Pure Random Maker
        import random
        def random_maker(c, m_cells, b_cells, active):
            m_set = set(m_cells)
            for s in active:
                if sum(1 for p in s if p in m_set) == 5 and c in s:
                    return 1e11
            return float(random.random())
        battery.append(("Baseline Random Maker", random_maker))

        return battery

    maker_battery = build_10x10_maker_battery()

    print(f"\nRunning 10x10 Gauntlet: Ultimate Breaker Slayer vs {len(maker_battery)} Makers")
    print(f"{'Staunch Maker Strategy':<32} | Winner | Turns | Max Cells | Defensive Verdict")
    print("-" * 90)

    b_wins = 0
    m_wins = 0

    for name, m_fn in maker_battery:
        res = run_match_arbitrary(m_fn, ult_b_fn, shapes_10x10, max_turns=50)
        winner = "Maker" if res["maker_won"] else "Breaker"
        turns = res["turns"]
        max_c = res["max_cells_in_shape"]
        if not res["maker_won"]:
            b_wins += 1
            verdict = f"TOTAL DENIAL (Capped at {max_c}/6 cells) 🛡️"
        else:
            m_wins += 1
            verdict = f"Maker Won ({max_c}/6 completed) ⚠️"
        print(f"{name:<32} | {winner:<7} | {turns:2d}t   | {max_c}/6     | {verdict}")

    print("-" * 90)
    print(f"Final 10x10 Score: Breaker {b_wins}/{len(maker_battery)} Wins ({b_wins / len(maker_battery) * 100:.1f}%), Maker {m_wins}/{len(maker_battery)} Wins")

    # 3. Test Pure 2x2 Block Pairing Breaker on 10x10
    print("\n--- STEP 3: Pure 2x2 Block Pairing Breaker Strategy on 10x10 ---")
    def block_pairing_breaker(c, m_cells, b_cells, active):
        # 1. Immediate win block
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        # 2. Block Maker's most recent move within its 2x2 block
        last_m = m_cells[-1] if m_cells else None
        if last_m:
            bx, by = last_m[0] // 2, last_m[1] // 2
            if c[0] // 2 == bx and c[1] // 2 == by:
                return 1e9 + sum(1 for s in active if c in s)
        # 3. General threat blocking
        score = 0.0
        for s in active:
            if c in s:
                m_cnt = sum(1 for p in s if p in m_set)
                score += (8.0 ** m_cnt)
        return float(score)

    print("Testing Pure 2x2 Block Pairing Breaker on 10x10:")
    b_pairing_wins = 0
    for name, m_fn in maker_battery:
        res = run_match_arbitrary(m_fn, block_pairing_breaker, shapes_10x10, max_turns=50)
        winner = "Maker" if res["maker_won"] else "Breaker"
        turns = res["turns"]
        max_c = res["max_cells_in_shape"]
        if not res["maker_won"]:
            b_pairing_wins += 1
            verdict = f"DENIAL ({max_c}/6 cells) 🛡️"
        else:
            verdict = f"Maker Won ({max_c}/6 completed) ⚠️"
        print(f"{name:<32} | {winner:<7} | {turns:2d}t   | {max_c}/6     | {verdict}")

    print(f"Block Pairing Breaker Score: {b_pairing_wins}/{len(maker_battery)} Wins ({b_pairing_wins / len(maker_battery) * 100:.1f}%)")

if __name__ == "__main__":
    main()
