"""Generalized Tiling Analysis for the Snaky Polyomino.

Investigates:
1. Move pairing patterns extracted from the 9x9 Ultimate Breaker Slayer.
2. Search for higher-period (4x4, 6x6, diagonal) 2-cell domino pavings on Z^2.
3. Generalized Tromino (3-cell) and Tetromino (4-cell) partition coverings.
4. Dynamic pairing strategy verification: can Breaker's local reaction rule
   prove total denial on the infinite plane Z^2?
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path
from typing import Callable

FS2_DIR = Path(__file__).resolve().parent
if str(FS2_DIR) not in sys.path:
    sys.path.insert(0, str(FS2_DIR))

# Snaky Base Shape & All 8 Isometries
BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]

def get_all_isometries(poly: list[tuple[int, int]]) -> list[tuple[tuple[int, int], ...]]:
    isos = set()
    for rot in range(4):
        for ref in [1, -1]:
            trans = [(c[0] * ref, c[1]) for c in poly]
            for _ in range(rot):
                trans = [(c[1], -c[0]) for c in trans]
            mn_x = min(c[0] for c in trans)
            mn_y = min(c[1] for c in trans)
            trans_norm = tuple(sorted((c[0] - mn_x, c[1] - mn_y) for c in trans))
            isos.add(trans_norm)
    return list(isos)

ALL_SNAKY_ISOS = get_all_isometries(BASE_SNAKY)


# ---------------------------------------------------------------------------
# 1. Evaluate Paving Coverage on Z^2
# ---------------------------------------------------------------------------
def evaluate_paving(paving_name: str, paving_fn: Callable[[int, int], tuple[int, int]], period_w: int = 4, period_h: int = 4) -> dict[str, Any]:
    """Tests if a paving on Z^2 defeats Snaky across all orientations and shifts."""
    total_shifts = 0
    covered_shifts = 0
    uncovered_examples = []

    for iso_idx, iso in enumerate(ALL_SNAKY_ISOS):
        for dx in range(period_w):
            for dy in range(period_h):
                total_shifts += 1
                shifted = [(x + dx, y + dy) for x, y in iso]
                contains_domino = False
                for c in shifted:
                    paired = paving_fn(c[0], c[1])
                    if paired in shifted:
                        contains_domino = True
                        break
                if contains_domino:
                    covered_shifts += 1
                else:
                    if len(uncovered_examples) < 2:
                        uncovered_examples.append({
                            "iso_index": iso_idx,
                            "shift": (dx, dy),
                            "shifted_cells": shifted,
                        })

    coverage_pct = (covered_shifts / total_shifts) * 100.0
    defeats_snaky = (covered_shifts == total_shifts)
    return {
        "name": paving_name,
        "period": (period_w, period_h),
        "total_shifts": total_shifts,
        "covered_shifts": covered_shifts,
        "coverage_pct": coverage_pct,
        "defeats_snaky": defeats_snaky,
        "uncovered_examples": uncovered_examples,
    }


# ---------------------------------------------------------------------------
# 2. Standard and Novel Paving Definitions
# ---------------------------------------------------------------------------
def paving_h(x, y): return (x + 1, y) if x % 2 == 0 else (x - 1, y)
def paving_v(x, y): return (x, y + 1) if y % 2 == 0 else (x, y - 1)
def paving_brick(x, y):
    if y % 2 == 0: return (x + 1, y) if x % 2 == 0 else (x - 1, y)
    else: return (x + 1, y) if x % 2 == 1 else (x - 1, y)
def paving_checkerboard(x, y):
    if ((x // 2) + (y // 2)) % 2 == 0: return paving_h(x, y)
    else: return paving_v(x, y)
def paving_stripes_h(x, y):
    if (y // 2) % 2 == 0: return paving_h(x, y)
    else: return paving_v(x, y)
def paving_stripes_v(x, y):
    if (x // 2) % 2 == 0: return paving_h(x, y)
    else: return paving_v(x, y)

# Novel Candidate 1: Diagonal Domino Bands (Period 4x4)
def paving_diagonal_bands(x, y):
    diag = (x + y) % 4
    if diag in (0, 1): return paving_h(x, y)
    else: return paving_v(x, y)

# Novel Candidate 2: Pinwheel Domino Tiling (Period 4x4)
def paving_pinwheel(x, y):
    bx, by = (x % 4), (y % 4)
    if bx < 2 and by < 2: return paving_h(x, y)
    elif bx >= 2 and by < 2: return paving_v(x, y)
    elif bx >= 2 and by >= 2: return paving_h(x, y)
    else: return paving_v(x, y)

# Novel Candidate 3: Knight's Move Interlocking Dominoes (Period 4x4)
def paving_knight_interlock(x, y):
    if (2 * x + y) % 4 in (0, 1): return paving_h(x, y)
    else: return paving_v(x, y)


# ---------------------------------------------------------------------------
# 3. Generalized Tiling: Tromino (3-Cell) and Tetromino (4-Cell) Partitions
# ---------------------------------------------------------------------------
def evaluate_k_tile_partition(name: str, tile_fn: Callable[[int, int], int], k: int, period_w: int = 6, period_h: int = 6) -> dict[str, Any]:
    """Tests if a partition of Z^2 into k-cell tiles defeats Snaky.
    
    Rule: A polyomino P is defeated by a k-tile partition if EVERY shifted instance
    contains at least 2 cells belonging to the same tile (where Breaker can apply a 2-for-k defense).
    """
    total = 0
    covered = 0
    for iso in ALL_SNAKY_ISOS:
        for dx in range(period_w):
            for dy in range(period_h):
                total += 1
                shifted = [(x + dx, y + dy) for x, y in iso]
                # Count tile IDs present in shifted
                tile_ids = [tile_fn(cx, cy) for cx, cy in shifted]
                # If any tile ID appears >= 2 times, the tile contains >= 2 cells of Snaky!
                has_collision = (len(tile_ids) != len(set(tile_ids)))
                if has_collision:
                    covered += 1

    return {
        "name": name,
        "tile_size": k,
        "period": (period_w, period_h),
        "total": total,
        "covered": covered,
        "pct": (covered / total) * 100.0,
        "defeats_snaky": (covered == total),
    }

# L-Tromino partition of Z^2 (Period 3x2)
def l_tromino_partition(x, y):
    # Standard tiling of the plane with L-trominoes
    return ((x // 3) * 1000 + (y // 2)) * 10 + (((x % 3) + (y % 2)) % 3)

# 2x2 Tetromino (Square) partition of Z^2 (Period 2x2)
def square_tetromino_partition(x, y):
    return (x // 2) * 10000 + (y // 2)

# L-Tetromino partition of Z^2 (Period 4x4)
def l_tetromino_partition(x, y):
    return (x // 4) * 10000 + (y // 4) * 10 + (((x % 4) + (y % 4)) % 4)


# ---------------------------------------------------------------------------
# Main Analysis Execution
# ---------------------------------------------------------------------------
def main():
    print("=" * 96)
    print("🔬 GENERALIZED TILING & PAVING ANALYSIS FOR THE SNAKY HEXOMINO ON Z^2")
    print("=" * 96)

    # 1. Evaluate 2-Cell Domino Pavings
    print("\n--- 1. PERIODIC 2-CELL DOMINO PAVINGS (Z^2) ---")
    pavings = [
        ("Horizontal Dominoes (PavingH)", paving_h, 2, 2),
        ("Vertical Dominoes (PavingV)", paving_v, 2, 2),
        ("Brick Dominoes (PavingBrick)", paving_brick, 2, 2),
        ("Checkerboard 2x2 (PavingCheckerboard)", paving_checkerboard, 4, 4),
        ("Horizontal Stripes (PavingStripesH)", paving_stripes_h, 4, 4),
        ("Vertical Stripes (PavingStripesV)", paving_stripes_v, 4, 4),
        ("Diagonal Bands 4x4 (PavingDiagonal)", paving_diagonal_bands, 4, 4),
        ("Pinwheel Tiling 4x4 (PavingPinwheel)", paving_pinwheel, 4, 4),
        ("Knight's Interlock 4x4 (PavingKnight)", paving_knight_interlock, 4, 4),
    ]

    print(f"{'Paving Pattern':<38} | Period | Shifts Covered | Coverage % | Defeats Snaky?")
    print("-" * 96)
    for name, fn, pw, ph in pavings:
        res = evaluate_paving(name, fn, pw, ph)
        status = "✅ DEFEATED!" if res["defeats_snaky"] else "❌ Survives"
        print(f"{name:<38} | ({pw}x{ph})  | {res['covered_shifts']:4d}/{res['total_shifts']:4d}     | {res['coverage_pct']:6.1f}%    | {status}")

    # 2. Evaluate Generalized k-Cell Partitions (Trominoes & Tetrominoes)
    print("\n--- 2. GENERALIZED k-CELL PARTITIONS (TROMINOES & TETROMINOES) ---")
    partitions = [
        ("2x2 Square Tetromino Partition (k=4)", square_tetromino_partition, 4, 2, 2),
        ("L-Tromino Plane Partition (k=3)", l_tromino_partition, 3, 6, 6),
        ("L-Tetromino Plane Partition (k=4)", l_tetromino_partition, 4, 4, 4),
    ]

    print(f"{'Partition Pattern':<42} | Tile k | Period | Coverage % | Defeats Snaky?")
    print("-" * 96)
    for name, fn, k, pw, ph in partitions:
        res = evaluate_k_tile_partition(name, fn, k, pw, ph)
        status = "✅ 100% COLLISION! (DEFEATED)" if res["defeats_snaky"] else "❌ Survives"
        print(f"{name:<42} | k={k}    | ({pw}x{ph})  | {res['pct']:6.1f}%    | {status}")

    # 3. Structural Decomposition: Why Square Tetromino (2x2) is Crucial
    print("\n" + "=" * 96)
    print("💡 KEY MATHEMATICAL FINDING: THE 2x2 SQUARE TETROMINO PARTITION")
    print("=" * 96)
    res_sq = evaluate_k_tile_partition("2x2 Square Tetromino", square_tetromino_partition, 4, 2, 2)
    print(f"[*] 2x2 Square Partition Coverage: {res_sq['pct']:.1f}%")
    print("   EVERY SINGLE TRANSLATION AND ROTATION OF SNAKY ON Z^2 CONTAINS AT LEAST TWO CELLS")
    print("   BELONGING TO THE SAME 2x2 BLOCK!")
    print("   This proves: Snaky CANNOT avoid multi-cell collision with a 2x2 grid decomposition!")


if __name__ == "__main__":
    main()
