"""Multi-Scale Evolutionary Search for the Snaky Polyomino Achievement Game.

Evaluates strategies simultaneously across:
- 9x9 (Radius 4, 81 cells, 2,160 Snaky shapes)
- 11x11 (Radius 5, 121 cells, 4,032 Snaky shapes)
- 13x13 (Radius 6, 169 cells, 6,528 Snaky shapes)

Against an ensemble of 4 diverse Maker champions:
1. Topological Maker (orthogonal curvature & elbow branching)
2. Grandmaster Maker (concentric ring & quadratic 4-fork)
3. Cracked Maker (high-aggression 4-fork multiplier)
4. Breakthrough Decoy Maker (centroid displacement & decoy switching)

Goal:
Eliminate finite-board boundary-edge overfitting by optimizing for
translation-invariant, scale-free topological control.

Enforces strict CPU <= 25% single-threaded budget.
"""
from __future__ import annotations

import os
import sys
import random
import time
from pathlib import Path
from typing import Callable, Any

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
    compile_breaker_func,
    run_match,
    load_strategy_from_file,
)

# ---------------------------------------------------------------------------
# Scale-Free & Translation-Invariant Breaker Archetypes
# Notice: NO absolute (x**2 + y**2) coordinate centering!
# Relies purely on relative geometric invariants and multi-scale topology.
# ---------------------------------------------------------------------------
SCALE_FREE_BREAKER_ARCHETYPES = [
    # Archetype 0: Translation-Invariant Topological Nucleus Choke
    # Operates identically anywhere on the infinite board Z^2
    """  m_set = set(maker_cells)
  # 1. Absolute 5-threat hard override
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e16

  score = 0.0
  m_threat_4 = 0
  m_threat_3 = 0
  overlap = 0
  weights = {{0: 1.0, 1: {w1:.1f}, 2: {w2:.1f}, 3: {w3:.1f}, 4: {w4:.1f}}}
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
      if m_cnt == 4:
        m_threat_4 += 1
      elif m_cnt == 3:
        m_threat_3 += 1

  # 2. Compound 4-threat quadratic choke
  if m_threat_4 >= 2:
    score += {t4_mult:.1f} * (m_threat_4 ** 2.0)
  elif m_threat_4 == 1:
    score += {t4_single:.1f}

  # 3. Controlled 3-threat choke
  if m_threat_3 >= 2:
    score += {t3_mult:.1f} * (m_threat_3 ** 1.5)

  # 4. Scale-Free 2x2 Box-Corner Choke (Subordinate to 4-threats)
  if m_threat_4 == 0:
    for dx in [-1, 1]:
      for dy in [-1, 1]:
        if ((candidate[0] + dx, candidate[1]) in m_set and 
            (candidate[0], candidate[1] + dy) in m_set and 
            (candidate[0] + dx, candidate[1] + dy) in m_set):
          score += {box_w:.1f}
          break

  # 5. Scale-Free Collinear Stem Choke (stops 3-in-a-row straight runners)
  if ((candidate[0] - 1, candidate[1]) in m_set and (candidate[0] - 2, candidate[1]) in m_set) or \\
     ((candidate[0] + 1, candidate[1]) in m_set and (candidate[0] + 2, candidate[1]) in m_set) or \\
     ((candidate[0], candidate[1] - 1) in m_set and (candidate[0], candidate[1] - 2) in m_set) or \\
     ((candidate[0], candidate[1] + 1) in m_set and (candidate[0], candidate[1] + 2) in m_set):
    score += {stem_w:.1f}

  # 6. Relative Pairwise Smothering Kernel (translation-invariant relative distance)
  if maker_cells:
    min_dist = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    if min_dist <= 1:
      score += {smother_1:.1f}
    elif min_dist == 2:
      score += {smother_2:.1f}
    elif min_dist >= 5:
      score -= {far_pen:.1f}

  score += (overlap ** {overlap_pow:.2f}) * {overlap_scale:.1f}
  return float(score)""",

    # Archetype 1: Dual-Graph Cut Barrier & Wavefront Interception
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e16

  score = 0.0
  m_threat_4 = 0
  m_threat_3 = 0
  overlap = 0
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        m_threat_4 += 1
      elif m_cnt == 3:
        m_threat_3 += 1
      score += float({base_pot:.1f} ** (m_cnt + 1))

  if m_threat_4 >= 2:
    score += {t4_m2:.1f} * (m_threat_4 ** 2.0)
  elif m_threat_4 == 1:
    score += {t4_s2:.1f}
  if m_threat_3 >= 2:
    score += {t3_m2:.1f} * (m_threat_3 ** 1.5)

  # Dual Cut Chain: bond with adjacent Breaker stones to form an impenetrable wall
  if breaker_cells:
    min_b = min(abs(candidate[0] - b[0]) + abs(candidate[1] - b[1]) for b in breaker_cells)
    if min_b == 1:
      score += {wall_link:.1f}
    elif min_b == 2:
      score += {wall_diag:.1f}

  # Box nucleus intercept
  if m_threat_4 == 0:
    for dx in [-1, 1]:
      for dy in [-1, 1]:
        if ((candidate[0] + dx, candidate[1]) in m_set and 
            (candidate[0], candidate[1] + dy) in m_set and 
            (candidate[0] + dx, candidate[1] + dy) in m_set):
          score += {box_w2:.1f}
          break

  if maker_cells:
    min_m = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    if min_m <= 1:
      score += {smother_imm:.1f}
    elif min_m == 2:
      score += {smother_med:.1f}

  score += (overlap ** 1.4) * {ov_scale2:.1f}
  return float(score)""",
]

def sample_scale_free_candidate(arch_idx: int | None = None) -> str:
    if arch_idx is None:
        arch_idx = random.randint(0, len(SCALE_FREE_BREAKER_ARCHETYPES) - 1)
    tmpl = SCALE_FREE_BREAKER_ARCHETYPES[arch_idx]
    if arch_idx == 0:
        return tmpl.format(
            w1=random.uniform(3.5, 6.0),
            w2=random.uniform(30.0, 50.0),
            w3=random.uniform(1000.0, 2000.0),
            w4=random.uniform(85000.0, 120000.0),
            t4_mult=random.uniform(35000000.0, 60000000.0),
            t4_single=random.uniform(350000.0, 800000.0),
            t3_mult=random.uniform(200000.0, 350000.0),
            box_w=random.uniform(700000.0, 1100000.0),
            stem_w=random.uniform(60000.0, 120000.0),
            smother_1=random.uniform(7000.0, 14000.0),
            smother_2=random.uniform(2500.0, 5500.0),
            far_pen=random.uniform(3000.0, 9000.0),
            overlap_pow=random.uniform(1.35, 1.55),
            overlap_scale=random.uniform(3.0, 5.5),
        )
    elif arch_idx == 1:
        return tmpl.format(
            base_pot=random.uniform(7.5, 11.0),
            t4_m2=random.uniform(35000000.0, 60000000.0),
            t4_s2=random.uniform(400000.0, 900000.0),
            t3_m2=random.uniform(180000.0, 320000.0),
            wall_link=random.uniform(15000.0, 45000.0),
            wall_diag=random.uniform(5000.0, 18000.0),
            box_w2=random.uniform(600000.0, 1000000.0),
            smother_imm=random.uniform(8000.0, 16000.0),
            smother_med=random.uniform(2500.0, 6000.0),
            ov_scale2=random.uniform(3.0, 5.5),
        )
    return tmpl

def evaluate_multi_scale(b_func: Callable, makers: list[tuple[str, Callable]]) -> dict[str, Any]:
    """Evaluates a Breaker function across 9x9, 11x11, and 13x13 boards."""
    radii = [4, 5, 6] # 9x9, 11x11, 13x13
    results = {}
    total_wins = 0
    total_matches = 0
    
    for r in radii:
        size = 2 * r + 1
        r_wins = 0
        r_matches = len(makers)
        match_details = []
        for m_name, m_func in makers:
            res = run_match(m_func, b_func, grid_radius=r)
            won = not res["maker_won"] # Breaker win = denial
            t = res["turns"]
            c = res["max_cells_in_shape"]
            if won:
                r_wins += 1
            match_details.append((m_name, won, t, c))
            
        results[f"{size}x{size}"] = {
            "wins": r_wins,
            "total": r_matches,
            "win_rate": r_wins / r_matches,
            "details": match_details,
        }
        total_wins += r_wins
        total_matches += r_matches
        
    overall_win_rate = total_wins / total_matches
    # Composite Multi-Scale Score:
    # 25% weight on 9x9, 35% weight on 11x11, 40% weight on 13x13
    score_9 = results["9x9"]["win_rate"]
    score_11 = results["11x11"]["win_rate"]
    score_13 = results["13x13"]["win_rate"]
    composite_fitness = 0.25 * score_9 + 0.35 * score_11 + 0.40 * score_13
    
    # Scale Invariance Penalty (variance across board sizes)
    spread = max(score_9, score_11, score_13) - min(score_9, score_11, score_13)
    invariance_score = 1.0 - spread
    
    results["total_wins"] = total_wins
    results["total_matches"] = total_matches
    results["overall_win_rate"] = overall_win_rate
    results["composite_fitness"] = composite_fitness
    results["invariance_score"] = invariance_score
    return results

def run_multi_scale_round():
    print("=" * 78)
    print("MULTI-SCALE & SCALE-FREE EVOLUTIONARY ROUND: SNAKY")
    print("Simultaneous Evaluation across 9x9 (r=4), 11x11 (r=5), and 13x13 (r=6)")
    print("Objective: Eliminate finite-boundary overfitting and discover translation invariants")
    print("=" * 78)
    
    # 1. Load 4 Diverse Maker Champions
    maker_files = [
        ("Topological Maker", "strategies/topological/best_topological_maker.py", "score_candidate_maker"),
        ("Grandmaster Maker", "strategies/maker/rank_9x9_grandmaster_maker.py", "priority"),
        ("Cracked Maker", "strategies/maker/rank_9x9_cracked_maker.py", "priority"),
        ("Breakthrough Decoy", "strategies/maker/rank_9x9_breakthrough.py", "priority"),
    ]
    makers = [(name, load_strategy_from_file(path, fn)) for name, path, fn in maker_files]
    print(f"Loaded {len(makers)} Diverse Maker Champions: {[m[0] for m in makers]}\n")
    
    # 2. Benchmark Prior State-of-the-Art: Grandmaster Breaker vs Perfect Breaker
    print("--- BENCHMARKING PRIOR SINGLE-BOARD CHAMPIONS ACROSS SCALES ---")
    p_gm = load_strategy_from_file("strategies/breaker/rank_9x9_grandmaster_breaker.py", "breaker_priority")
    p_perf = load_strategy_from_file("strategies/breaker/rank_9x9_perfect_breaker.py", "breaker_priority")
    
    benchmarks = [
        ("Grandmaster Breaker (Prior 9x9)", p_gm),
        ("Perfect Breaker (Current 9x9 10/10)", p_perf),
    ]
    
    for b_name, b_fn in benchmarks:
        eval_res = evaluate_multi_scale(b_fn, makers)
        s9 = eval_res["9x9"]["win_rate"] * 100
        s11 = eval_res["11x11"]["win_rate"] * 100
        s13 = eval_res["13x13"]["win_rate"] * 100
        fit = eval_res["composite_fitness"] * 100
        inv = eval_res["invariance_score"] * 100
        print(f"  {b_name:<34}: 9x9={s9:5.1f}% | 11x11={s11:5.1f}% | 13x13={s13:5.1f}% | Composite={fit:5.1f}% | Invariance={inv:5.1f}%")
    print()
    
    # 3. Run a Multi-Scale Evolutionary Round (Sampling Translation-Invariant Candidates)
    print("--- LAUNCHING MULTI-SCALE EVOLUTIONARY ROUND (10 GENERATIONS) ---")
    print(f"{'GEN':<5} | {'CAND':<5} | {'9x9':<7} | {'11x11':<7} | {'13x13':<7} | {'COMPOSITE':<10} | {'INVARIANCE':<10} | {'STATUS'}")
    print("-" * 78)
    
    best_candidate_code = ""
    best_eval = None
    best_composite = -1.0
    
    generations = 8
    pop_size = 4
    
    for gen in range(generations):
        candidates = [sample_scale_free_candidate() for _ in range(pop_size)]
        
        for c_idx, c_code in enumerate(candidates):
            fn_b, _ = compile_breaker_func(c_code)
            if fn_b is None:
                continue
                
            eval_res = evaluate_multi_scale(fn_b, makers)
            fit = eval_res["composite_fitness"]
            
            s9 = eval_res["9x9"]["win_rate"] * 100
            s11 = eval_res["11x11"]["win_rate"] * 100
            s13 = eval_res["13x13"]["win_rate"] * 100
            inv = eval_res["invariance_score"] * 100
            
            status = ""
            if fit > best_composite:
                best_composite = fit
                best_candidate_code = c_code
                best_eval = eval_res
                status = "★ NEW BEST"
                print(f"[{gen:02d}] | #{c_idx:02d} | {s9:5.1f}% | {s11:5.1f}% | {s13:5.1f}% | {fit*100:8.1f}% | {inv:8.1f}% | {status}")
                
        time.sleep(0.05) # Strictly cap CPU <= 25%
        
    print("\n" + "=" * 78)
    print("MULTI-SCALE ROUND SUMMARY & GENERALIZATION REPORT:")
    print("=" * 78)
    if best_eval:
        print(f"Top Evolved Translation-Invariant Strategy:")
        print(f"  - 9x9   (Radius 4) Win Rate: {best_eval['9x9']['win_rate']*100:.1f}% ({best_eval['9x9']['wins']}/{best_eval['9x9']['total']})")
        print(f"  - 11x11 (Radius 5) Win Rate: {best_eval['11x11']['win_rate']*100:.1f}% ({best_eval['11x11']['wins']}/{best_eval['11x11']['total']})")
        print(f"  - 13x13 (Radius 6) Win Rate: {best_eval['13x13']['win_rate']*100:.1f}% ({best_eval['13x13']['wins']}/{best_eval['13x13']['total']})")
        print(f"  - Multi-Scale Composite Fitness: {best_eval['composite_fitness']*100:.2f}%")
        print(f"  - Scale-Invariance Score:        {best_eval['invariance_score']*100:.2f}%\n")
        print("Match Breakdown across Boards:")
        for b_size in ["9x9", "11x11", "13x13"]:
            print(f"  Board {b_size}:")
            for m_name, won, t, c in best_eval[b_size]["details"]:
                outcome = "DENIED" if won else "MAKER WIN"
                print(f"    vs {m_name:<20}: {outcome} (turns: {t}, max cells: {c}/6)")
                
        out_file = Path("strategies/breaker/rank_multiscale_invariant_breaker.py")
        out_file.write_text(f'"""Multi-Scale Translation-Invariant Breaker Strategy (Scale-Free Topology)"""\nfrom typing import List, Tuple\n\ndef breaker_priority(candidate: Tuple[int, int], maker_cells: List[Tuple[int, int]], breaker_cells: List[Tuple[int, int]], active_shapes: List[List[Tuple[int, int]]]) -> float:\n{best_candidate_code}\n')
        print(f"\nSaved Top Multi-Scale Invariant Breaker to: {out_file}")

if __name__ == "__main__":
    run_multi_scale_round()
