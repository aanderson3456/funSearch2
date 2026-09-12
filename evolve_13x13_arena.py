"""13x13 Snaky Arena: Deep Evolution on the Open Field.

Focuses purely on the 13x13 board (Radius 6, 169 cells, 6,528 Snaky shapes),
which closely approximates the unbounded infinite plane Z^2 by eliminating
the artificial boundary-wall traps of 8x8 and 9x9.

Supports:
- Offline Mock Genetic Evolution
- Live Gemini API FunSearch Integration (once GEMINI_API_KEY is provided)
- Automated cross-evaluation between LLM-generated and Mock-evolved programs

Enforces strict single-threaded execution (CPU <= 25%).
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Strict single-threading to guarantee CPU <= 25%
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

def run_13x13_showdown():
    print("=" * 78)
    print("13x13 SNAKY GRAND ARENA (169 CELLS, 6,528 SHAPES)")
    print("Approximating the Unbounded Plane Z^2")
    print("=" * 78)
    
    # Load Top Historical Makers
    makers = [
        ("Topological Maker", "strategies/topological/best_topological_maker.py", "score_candidate_maker"),
        ("Grandmaster Maker", "strategies/maker/rank_9x9_grandmaster_maker.py", "priority"),
        ("Cracked Maker", "strategies/maker/rank_9x9_cracked_maker.py", "priority"),
        ("15-Turn Fork Maker", "strategies/maker/rank_plumb_latest.py", "priority"),
        ("Rank 0 Baseline Maker", "strategies/maker/rank_0_score_300.00.py", "priority"),
    ]
    
    # Load Top Historical Breakers
    breakers = [
        ("Scale-Free Invariant Breaker", "strategies/breaker/rank_multiscale_invariant_breaker.py", "breaker_priority"),
        ("Perfect 9x9 Breaker", "strategies/breaker/rank_9x9_perfect_breaker.py", "breaker_priority"),
        ("Grandmaster Breaker", "strategies/breaker/rank_9x9_grandmaster_breaker.py", "breaker_priority"),
        ("Ultimate Slayer Breaker", "strategies/breaker/rank_9x9_ultimate_slayer.py", "breaker_priority"),
    ]
    
    loaded_makers = [(name, load_strategy_from_file(path, fn)) for name, path, fn in makers]
    loaded_breakers = [(name, load_strategy_from_file(path, fn)) for name, path, fn in breakers]
    
    print(f"Executing Complete 13x13 Round-Robin ({len(loaded_makers)} Makers x {len(loaded_breakers)} Breakers = 20 Matches)...")
    print("-" * 78)
    print(f"{'MAKER':<22} | {'BREAKER':<28} | {'OUTCOME':<15} | {'TURNS':<7} | {'MAX CELLS'}")
    print("-" * 78)
    
    m_total_wins = 0
    b_total_wins = 0
    
    for m_name, m_fn in loaded_makers:
        for b_name, b_fn in loaded_breakers:
            res = run_match(m_fn, b_fn, grid_radius=6)
            won = res["maker_won"]
            t = res["turns"]
            c = res["max_cells_in_shape"]
            if won:
                m_total_wins += 1
                outcome = "MAKER WIN"
            else:
                b_total_wins += 1
                outcome = "BREAKER DENIAL"
            print(f"{m_name:<22} | {b_name:<28} | {outcome:<15} | {t:<7} | {c}/6")
            
    total_games = m_total_wins + b_total_wins
    print("=" * 78)
    print(f"13x13 SHOWDOWN SUMMARY:")
    print(f"Total Matches: {total_games}")
    print(f"Maker Wins:   {m_total_wins:2d} ({m_total_wins / total_games * 100:.1f}%)")
    print(f"Breaker Wins: {b_total_wins:2d} ({b_total_wins / total_games * 100:.1f}%)")
    print("=" * 78)

if __name__ == "__main__":
    run_13x13_showdown()
