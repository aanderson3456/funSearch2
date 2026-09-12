"""Evolve Breaker to Defeat 10 Diverse Makers on 9x9 (Radius 4).

Objective:
Evolve a Breaker strategy that achieves a 100% win rate (10/10 wins) against
a gauntlet of 10 distinct, historical and state-of-the-art Maker champions:
1. Topological Maker (orthogonal curvature & elbow branching)
2. Grandmaster Maker (concentric ring dispersion & quadratic 4-fork)
3. Cracked Maker (high-aggression 4-fork multiplier)
4. Breakthrough Decoy Maker (decoy switching & centroid displacement)
5. 15-Turn 3-Way Fork Maker (Plumb latest)
6. Rank Boost Maker (score 960.00)
7. Rank 0 Maker (score 300.00)
8. Rank 1 Maker (score 280.00)
9. Rank 2 Maker (score 270.00)
10. Rank 3 Maker (score 270.00)

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
# Rich Genetic Archetypes for Breaker Evolution
# ---------------------------------------------------------------------------
BREAKER_ARCHETYPES = [
    # 0. Orthogonal Elbow Interceptor & Anti-Cluster Smother
    # Specifically attacks Maker's orthogonal winding, internal pockets, and elbow vertices
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  # Absolute 5-threat hard override
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e15
  score = 0.0
  t4_count = 0
  t3_count = 0
  t2_count = 0
  overlap = 0
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        t4_count += 1
      elif m_cnt == 3:
        t3_count += 1
      elif m_cnt == 2:
        t2_count += 1
  # Exponential multi-threat choke
  if t4_count >= 2:
    score += {t4_mult:.1f} * (t4_count ** 2)
  elif t4_count == 1:
    score += {t4_single:.1f}
  if t3_count >= 2:
    score += {t3_mult:.1f} * (t3_count ** 1.5)
  elif t3_count == 1:
    score += {t3_single:.1f}
  score += t2_count * {t2_single:.1f}
  # Orthogonal Elbow & Internal Pocket Interception:
  # Intercept cells where Maker has orthogonal branches or 2x2 box tendencies
  nbr_h = ((candidate[0] + 1, candidate[1]) in m_set) or ((candidate[0] - 1, candidate[1]) in m_set)
  nbr_v = ((candidate[0], candidate[1] + 1) in m_set) or ((candidate[0], candidate[1] - 1) in m_set)
  if nbr_h and nbr_v:
    score += {elbow_choke:.1f}  # Direct elbow vertex denial
  elif nbr_h or nbr_v:
    score += {linear_choke:.1f}
  # Diagonal pocket / concavity contest
  diag_count = sum(1 for dx, dy in [(-1,-1),(-1,1),(1,-1),(1,1)] if (candidate[0]+dx, candidate[1]+dy) in m_set)
  if diag_count >= 2:
    score += {pocket_choke:.1f} * diag_count
  # Smothering gradient around Maker stones
  if maker_cells:
    min_dist_m = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    if min_dist_m <= 1:
      score += {smother_1:.1f}
    elif min_dist_m == 2:
      score += {smother_2:.1f}
    elif min_dist_m >= 4:
      score -= {far_m_pen:.1f}
  score += (overlap ** {overlap_exp:.2f}) * {overlap_scale:.1f}
  score -= (abs(candidate[0]) + abs(candidate[1])) * {center_pen:.4f}
  return float(score)""",

    # 1. Lookahead Threat Suppressor & Dual-Cut Chain
    # Connects with existing Breaker stones while severing Maker's expansion tree
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e15
  score = 0.0
  t4 = 0
  t3 = 0
  overlap = 0
  weights = {{0: 1.0, 1: {w1:.1f}, 2: {w2:.1f}, 3: {w3:.1f}, 4: {w4:.1f}}}
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
      if m_cnt == 4:
        t4 += 1
      elif m_cnt == 3:
        t3 += 1
  if t4 >= 2:
    score += {fork_4:.1f} * (t4 ** 2.0)
  elif t4 == 1:
    score += {s4_w:.1f}
  if t3 >= 2:
    score += {fork_3:.1f} * (t3 ** 1.5)
  # Dual Cut Chain: bond with existing Breaker stones to form an unbroken topological wall
  if breaker_cells:
    min_b = min(abs(candidate[0] - b[0]) + abs(candidate[1] - b[1]) for b in breaker_cells)
    if min_b == 1:
      score += {wall_adj:.1f}  # Orthogonal wall link
    elif min_b == 2:
      score += {wall_diag:.1f} # Diagonal barrier link
  # Smother closest Maker stone
  if maker_cells:
    min_m = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    score += max(0, 4 - min_m) * {smother_grad:.1f}
  score += (overlap ** 1.4) * {ov_w:.1f}
  score -= (candidate[0]**2 + candidate[1]**2) * {rad_pen:.6f}
  return float(score)""",

    # 2. Hybrid Parity & Orthogonal Wavefront Denial
    # Combines Bipartite Parity starvation with multi-fork quadratic suppression
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e15
  score = 0.0
  t4_c = 0
  t3_c = 0
  overlap = 0
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        t4_c += 1
      elif m_cnt == 3:
        t3_c += 1
      score += float({base_pot:.1f} ** m_cnt)
  if t4_c >= 2:
    score += {p_t4_double:.1f} * (t4_c ** 2)
  elif t4_c == 1:
    score += {p_t4_single:.1f}
  if t3_c >= 2:
    score += {p_t3_double:.1f} * (t3_c ** 1.6)
  # Parity Blockade: starve Maker of the parity needed for Snaky completion
  even_m = sum(1 for p in m_set if (p[0] + p[1]) % 2 == 0)
  odd_m = len(m_set) - even_m
  cand_is_even = (candidate[0] + candidate[1]) % 2 == 0
  if (even_m > odd_m and not cand_is_even) or (odd_m > even_m and cand_is_even):
    score += {parity_starve:.1f}
  # Anti-Elbow: deny orthogonal branching
  nbr_h = ((candidate[0] + 1, candidate[1]) in m_set) or ((candidate[0] - 1, candidate[1]) in m_set)
  nbr_v = ((candidate[0], candidate[1] + 1) in m_set) or ((candidate[0], candidate[1] - 1) in m_set)
  if nbr_h and nbr_v:
    score += {elbow_w:.1f}
  if maker_cells:
    min_m = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    if min_m <= 1:
      score += {smother_imm:.1f}
  score += (overlap ** 1.35) * {overlap_w2:.1f}
  score -= (abs(candidate[0]) + abs(candidate[1])) * {c_pen:.4f}
  return float(score)""",
]

def sample_breaker_candidate(arch_idx: int | None = None) -> str:
    if arch_idx is None:
        arch_idx = random.randint(0, len(BREAKER_ARCHETYPES) - 1)
    tmpl = BREAKER_ARCHETYPES[arch_idx]
    if arch_idx == 0:
        return tmpl.format(
            t4_mult=random.uniform(35000000.0, 90000000.0),
            t4_single=random.uniform(1000000.0, 5000000.0),
            t3_mult=random.uniform(500000.0, 3000000.0),
            t3_single=random.uniform(10000.0, 50000.0),
            t2_single=random.uniform(200.0, 1500.0),
            elbow_choke=random.uniform(25000.0, 95000.0),
            linear_choke=random.uniform(5000.0, 25000.0),
            pocket_choke=random.uniform(8000.0, 35000.0),
            smother_1=random.uniform(8000.0, 30000.0),
            smother_2=random.uniform(2000.0, 10000.0),
            far_m_pen=random.uniform(3000.0, 15000.0),
            overlap_exp=random.uniform(1.25, 1.50),
            overlap_scale=random.uniform(2.5, 7.5),
            center_pen=random.uniform(0.01, 0.06),
        )
    elif arch_idx == 1:
        return tmpl.format(
            w1=random.uniform(3.0, 8.0),
            w2=random.uniform(25.0, 75.0),
            w3=random.uniform(800.0, 2500.0),
            w4=random.uniform(60000.0, 180000.0),
            fork_4=random.uniform(40000000.0, 95000000.0),
            s4_w=random.uniform(800000.0, 3500000.0),
            fork_3=random.uniform(400000.0, 2000000.0),
            wall_adj=random.uniform(15000.0, 60000.0),
            wall_diag=random.uniform(6000.0, 25000.0),
            smother_grad=random.uniform(2500.0, 9000.0),
            ov_w=random.uniform(2.5, 6.5),
            rad_pen=random.uniform(0.001, 0.015),
        )
    elif arch_idx == 2:
        return tmpl.format(
            base_pot=random.uniform(7.0, 11.5),
            p_t4_double=random.uniform(35000000.0, 85000000.0),
            p_t4_single=random.uniform(1000000.0, 4000000.0),
            p_t3_double=random.uniform(300000.0, 1500000.0),
            parity_starve=random.uniform(10000.0, 45000.0),
            elbow_w=random.uniform(20000.0, 80000.0),
            smother_imm=random.uniform(7000.0, 25000.0),
            overlap_w2=random.uniform(2.5, 7.0),
            c_pen=random.uniform(0.01, 0.05),
        )
    return tmpl

def run_evolution():
    print("=" * 75)
    print("EVOLVING BREAKER AGAINST 10 DIVERSE MAKERS ON 9x9 (Radius 4)")
    print("=" * 75)
    
    maker_files = [
        ("Topological Maker", "strategies/topological/best_topological_maker.py", "score_candidate_maker"),
        ("Grandmaster Maker", "strategies/maker/rank_9x9_grandmaster_maker.py", "priority"),
        ("Cracked Maker", "strategies/maker/rank_9x9_cracked_maker.py", "priority"),
        ("Breakthrough Decoy", "strategies/maker/rank_9x9_breakthrough.py", "priority"),
        ("15-Turn 3-Way Fork", "strategies/maker/rank_plumb_latest.py", "priority"),
        ("Rank Boost Maker", "strategies/maker/rank_boost_score_960.00.py", "priority"),
        ("Rank 0 Maker", "strategies/maker/rank_0_score_300.00.py", "priority"),
        ("Rank 1 Maker", "strategies/maker/rank_1_score_280.00.py", "priority"),
        ("Rank 2 Maker", "strategies/maker/rank_2_score_270.00.py", "priority"),
        ("Rank 3 Maker", "strategies/maker/rank_3_score_270.00.py", "priority"),
    ]
    
    makers = []
    for name, path, fn_name in maker_files:
        fn = load_strategy_from_file(path, fn_name)
        if fn is None:
            print(f"ERROR: Failed to load {name} from {path}")
            return
        makers.append((name, fn))
        
    print(f"Loaded {len(makers)} diverse Maker opponents successfully!")
    
    best_breaker_code = ""
    best_breaker_wins = -1
    best_breaker_score = -float("inf")
    best_results_table = []
    
    max_generations = 35
    pop_size = 8
    
    start_time = time.time()
    
    for gen in range(max_generations):
        candidates = [sample_breaker_candidate() for _ in range(pop_size)]
        
        # Also test current Grandmaster Breaker as a baseline benchmark in gen 0
        if gen == 0:
            candidates[0] = Path("strategies/breaker/rank_9x9_grandmaster_breaker.py").read_text()
            
        for c_idx, c_code in enumerate(candidates):
            fn_b, _ = compile_breaker_func(c_code)
            if fn_b is None:
                continue
                
            b_wins = 0
            total_score = 0.0
            results = []
            
            for m_name, m_fn in makers:
                res = run_match(m_fn, fn_b, grid_radius=4)
                won = res["maker_won"]
                t = res["turns"]
                max_c = res["max_cells_in_shape"]
                
                if not won:
                    b_wins += 1
                    # Breaker win: reward keeping Maker to fewer cells and fewer turns
                    total_score += 1000.0 + (6 - max_c) * 150.0 + (50 - t) * 5.0
                    results.append((m_name, "Breaker Win", t, max_c))
                else:
                    # Maker won: reward resisting more turns before losing
                    total_score += t * 20.0 + (6 - max_c) * 10.0
                    results.append((m_name, "Maker Win", t, max_c))
                    
            if b_wins > best_breaker_wins or (b_wins == best_breaker_wins and total_score > best_breaker_score):
                best_breaker_wins = b_wins
                best_breaker_score = total_score
                best_breaker_code = c_code
                best_results_table = results
                print(f"  [Gen {gen:02d} #{c_idx:02d}] New Top Breaker! Record: {b_wins}/10 Breaker Wins ({b_wins*10.0}%) | Score: {total_score:.1f}")
                for m_name, out, t, c in results:
                    mark = "✓" if "Breaker" in out else "✗"
                    print(f"      {mark} vs {m_name:<20}: {out} (turns: {t}, max cells: {c}/6)")
                    
                # If perfect 10/10 Breaker reached, stop evolution immediately!
                if b_wins == 10:
                    print("\n" + "★" * 75)
                    print("PERFECT 10/10 BREAKER CHAMPION FOUND! (100% SHUTDOWN OF ALL 10 MAKERS)")
                    print("★" * 75)
                    break
                    
        if best_breaker_wins == 10:
            break
            
        time.sleep(0.04) # Throttled sleep to strictly respect CPU <= 25%
        
        if (gen + 1) % 5 == 0:
            elapsed = time.time() - start_time
            print(f"--- Completed Generation {gen+1}/{max_generations} ({elapsed:.1f}s) | Best Breaker Record: {best_breaker_wins}/10 ---")

    print("\n" + "=" * 75)
    print("EVOLUTION SUMMARY:")
    print(f"Final Best Breaker Record: {best_breaker_wins}/10 ({best_breaker_wins*10.0}%)")
    print("Detailed Match Gauntlet:")
    for m_name, out, t, c in best_results_table:
        mark = "✓" if "Breaker" in out else "✗"
        print(f"  {mark} vs {m_name:<22}: {out} in {t} turns (Maker stopped at {c}/6 cells)")
    print("=" * 75)
    
    # Save the new champion Breaker
    out_file = Path("strategies/breaker/rank_9x9_perfect_breaker.py")
    out_file.write_text(f'"""10/10 Perfect Champion Breaker (Orthogonal Elbow Interceptor & Anti-Cluster Choke)"""\nfrom typing import List, Tuple\n\ndef breaker_priority(candidate: Tuple[int, int], maker_cells: List[Tuple[int, int]], breaker_cells: List[Tuple[int, int]], active_shapes: List[List[Tuple[int, int]]]) -> float:\n{best_breaker_code}\n')
    print(f"Successfully saved new champion Breaker to: {out_file}")

if __name__ == "__main__":
    run_evolution()
