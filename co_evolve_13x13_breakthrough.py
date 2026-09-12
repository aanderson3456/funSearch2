"""13x13 Breakthrough Co-Evolution: Can Breaker Defend the Open Field?

On 13x13 (open field approximating Z^2), Maker currently wins 75-100% of matches.
This script runs evolutionary search on Breaker strategies specifically to see if
ANY Breaker heuristic can deny Maker on 13x13, while preserving single-threaded execution (CPU <= 25%).
"""
from __future__ import annotations

import os
import sys
import time
import random
from pathlib import Path
from typing import Callable

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
    run_match,
    load_strategy_from_file,
)

print("Precomputing 13x13 board shapes (radius 6, 864 shapes)...")
SHAPES_13x13 = get_board_shapes(radius=6)

# Load Top Maker Benchmarks
MAKERS = [
    ("Rank 0 Maker", load_strategy_from_file("strategies/maker/rank_0_score_300.00.py", "priority")),
    ("15-Turn Fork Maker", load_strategy_from_file("strategies/maker/rank_plumb_latest.py", "priority")),
    ("Grandmaster Maker", load_strategy_from_file("strategies/maker/rank_9x9_grandmaster_maker.py", "priority")),
]

def make_breaker_candidate(params: dict[str, float]) -> Callable:
    w0 = params["w0"]
    w1 = params["w1"]
    w2 = params["w2"]
    w3 = params["w3"]
    w4 = params["w4"]
    fork4_mult = params["fork4_mult"]
    fork3_mult = params["fork3_mult"]
    box_bonus = params["box_bonus"]
    stem_bonus = params["stem_bonus"]
    dist_bonus1 = params["dist_bonus1"]
    dist_bonus2 = params["dist_bonus2"]
    dist_penalty = params["dist_penalty"]
    overlap_power = params["overlap_power"]
    overlap_weight = params["overlap_weight"]
    
    def breaker_priority(candidate, maker_cells, breaker_cells, active_shapes) -> float:
        m_set = set(maker_cells)
        # Immediate 5-threat block
        for s in active_shapes:
            if candidate in s and sum(1 for p in s if p in m_set) == 5:
                return 1e16

        score = 0.0
        threat_4 = 0
        threat_3 = 0
        overlap = 0
        weights = {0: w0, 1: w1, 2: w2, 3: w3, 4: w4}
        for s in active_shapes:
            if candidate in s:
                overlap += 1
                m_cnt = sum(1 for p in s if p in m_set)
                score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
                if m_cnt == 4:
                    threat_4 += 1
                elif m_cnt == 3:
                    threat_3 += 1

        if threat_4 >= 2:
            score += fork4_mult * (threat_4 ** 2.0)
        elif threat_4 == 1:
            score += fork4_mult * 0.01

        if threat_3 >= 2:
            score += fork3_mult * (threat_3 ** 1.5)

        # 2x2 box choke
        if threat_4 == 0:
            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    if ((candidate[0] + dx, candidate[1]) in m_set and 
                        (candidate[0], candidate[1] + dy) in m_set and 
                        (candidate[0] + dx, candidate[1] + dy) in m_set):
                        score += box_bonus
                        break

        # Collinear stem choke
        if (((candidate[0] - 1, candidate[1]) in m_set and (candidate[0] - 2, candidate[1]) in m_set) or
            ((candidate[0] + 1, candidate[1]) in m_set and (candidate[0] + 2, candidate[1]) in m_set) or
            ((candidate[0], candidate[1] - 1) in m_set and (candidate[0], candidate[1] - 2) in m_set) or
            ((candidate[0], candidate[1] + 1) in m_set and (candidate[0], candidate[1] + 2) in m_set)):
            score += stem_bonus

        # Pairwise distance kernel
        if maker_cells:
            min_dist = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
            if min_dist <= 1:
                score += dist_bonus1
            elif min_dist == 2:
                score += dist_bonus2
            elif min_dist >= 5:
                score -= dist_penalty

        score += (overlap ** overlap_power) * overlap_weight
        return float(score)

    return breaker_priority

def evaluate_breaker_13x13(breaker_fn: Callable) -> tuple[float, int, int]:
    denials = 0
    total_turns = 0
    for m_name, m_fn in MAKERS:
        res = run_match(m_fn, breaker_fn, grid_radius=6)
        if not res["maker_won"]:
            denials += 1
            total_turns += 100
        else:
            total_turns += res["turns"]
    # Breaker fitness: max denials + longest survival
    fitness = denials * 1000.0 + total_turns
    return fitness, denials, len(MAKERS)

def run_evolution():
    print("=" * 78)
    print("13x13 ADVERSARIAL BREAKER EVOLUTION")
    print("Testing if Breaker can hold the open field against Top Makers")
    print("=" * 78)
    
    # Baseline invariant breaker parameters
    best_params = {
        "w0": 1.0, "w1": 3.7, "w2": 43.6, "w3": 1726.3, "w4": 99921.1,
        "fork4_mult": 59000172.3, "fork3_mult": 330405.3,
        "box_bonus": 1093831.1, "stem_bonus": 77343.7,
        "dist_bonus1": 10577.3, "dist_bonus2": 2676.7, "dist_penalty": 7705.1,
        "overlap_power": 1.39, "overlap_weight": 5.5
    }
    
    baseline_fn = make_breaker_candidate(best_params)
    best_fitness, denials, total = evaluate_breaker_13x13(baseline_fn)
    print(f"Baseline Invariant Breaker on 13x13: Denials={denials}/{total} (Fitness={best_fitness:.1f})")
    print("-" * 78)
    
    population = [best_params]
    for _ in range(9):
        mut = dict(best_params)
        for k in mut:
            mut[k] *= random.uniform(0.7, 1.4)
        population.append(mut)
        
    for gen in range(1, 6):
        scored_pop = []
        for ind in population:
            fn = make_breaker_candidate(ind)
            fit, den, tot = evaluate_breaker_13x13(fn)
            scored_pop.append((fit, den, ind))
            
        scored_pop.sort(key=lambda x: x[0], reverse=True)
        top_fit, top_den, top_ind = scored_pop[0]
        
        if top_fit > best_fitness:
            diff = top_fit - best_fitness
            best_fitness = top_fit
            best_params = top_ind
            print(f"[Gen {gen:2d}] 🚀 New Champion Breaker! Fitness: {top_fit:.1f} | Denials: {top_den}/{total} (+{diff:.1f})")
        else:
            print(f"[Gen {gen:2d}] Top Fitness: {top_fit:.1f} | Denials: {top_den}/{total}")
            
        # Selection & reproduction
        survivors = [p[2] for p in scored_pop[:4]]
        new_pop = list(survivors)
        while len(new_pop) < 10:
            parent = random.choice(survivors)
            child = dict(parent)
            # Mutate 2-3 genes
            genes_to_mutate = random.sample(list(child.keys()), k=random.randint(2, 4))
            for g in genes_to_mutate:
                child[g] *= random.uniform(0.6, 1.6)
            new_pop.append(child)
        population = new_pop

    print("=" * 78)
    final_fn = make_breaker_candidate(best_params)
    final_fit, final_den, total = evaluate_breaker_13x13(final_fn)
    print(f"EVOLUTION SUMMARY ON 13x13:")
    print(f"Final Breaker Denials: {final_den}/{total} ({final_den / total * 100:.1f}%)")
    print(f"Final Survival Fitness: {final_fit:.1f}")
    
    print("\nDetailed Match Results vs Top Makers on 13x13:")
    for m_name, m_fn in MAKERS:
        res = run_match(m_fn, final_fn, grid_radius=6)
        outcome = "MAKER WIN" if res["maker_won"] else "BREAKER DENIAL"
        print(f"  {m_name:<22} vs Evolved Breaker: {outcome:<14} (Turns: {res['turns']:2d}, Max Cells: {res['max_cells_in_shape']}/6)")

    # Save to strategies/breaker/rank_13x13_breakthrough_breaker.py
    out_code = f'''"""Evolved 13x13 Breakthrough Breaker Champion (Denials: {final_den}/{total})"""
from typing import List, Tuple

def breaker_priority(candidate: Tuple[int, int], maker_cells: List[Tuple[int, int]], breaker_cells: List[Tuple[int, int]], active_shapes: List[List[Tuple[int, int]]]) -> float:
    m_set = set(maker_cells)
    for s in active_shapes:
        if candidate in s and sum(1 for p in s if p in m_set) == 5:
            return 1e16

    score = 0.0
    threat_4 = 0
    threat_3 = 0
    overlap = 0
    weights = {{0: {best_params["w0"]:.3f}, 1: {best_params["w1"]:.3f}, 2: {best_params["w2"]:.3f}, 3: {best_params["w3"]:.3f}, 4: {best_params["w4"]:.3f}}}
    for s in active_shapes:
        if candidate in s:
            overlap += 1
            m_cnt = sum(1 for p in s if p in m_set)
            score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
            if m_cnt == 4:
                threat_4 += 1
            elif m_cnt == 3:
                threat_3 += 1

    if threat_4 >= 2:
        score += {best_params["fork4_mult"]:.1f} * (threat_4 ** 2.0)
    elif threat_4 == 1:
        score += {best_params["fork4_mult"] * 0.01:.1f}

    if threat_3 >= 2:
        score += {best_params["fork3_mult"]:.1f} * (threat_3 ** 1.5)

    if threat_4 == 0:
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                if ((candidate[0] + dx, candidate[1]) in m_set and 
                    (candidate[0], candidate[1] + dy) in m_set and 
                    (candidate[0] + dx, candidate[1] + dy) in m_set):
                    score += {best_params["box_bonus"]:.1f}
                    break

    if (((candidate[0] - 1, candidate[1]) in m_set and (candidate[0] - 2, candidate[1]) in m_set) or
        ((candidate[0] + 1, candidate[1]) in m_set and (candidate[0] + 2, candidate[1]) in m_set) or
        ((candidate[0], candidate[1] - 1) in m_set and (candidate[0], candidate[1] - 2) in m_set) or
        ((candidate[0], candidate[1] + 1) in m_set and (candidate[0], candidate[1] + 2) in m_set)):
        score += {best_params["stem_bonus"]:.1f}

    if maker_cells:
        min_dist = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
        if min_dist <= 1:
            score += {best_params["dist_bonus1"]:.1f}
        elif min_dist == 2:
            score += {best_params["dist_bonus2"]:.1f}
        elif min_dist >= 5:
            score -= {best_params["dist_penalty"]:.1f}

    score += (overlap ** {best_params["overlap_power"]:.2f}) * {best_params["overlap_weight"]:.2f}
    return float(score)
'''
    save_path = FS2_DIR / "strategies" / "breaker" / "rank_13x13_breakthrough_breaker.py"
    save_path.write_text(out_code)
    print(f"\nSaved 13x13 Breakthrough Breaker Champion to: {save_path.name}")
    print("=" * 78)

if __name__ == "__main__":
    run_evolution()
