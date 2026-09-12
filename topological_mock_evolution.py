"""Topological Mock Evolution for Snaky Polyomino Achievement Game.

Explores topological invariants and patterns in Maker and Breaker strategies:
1. Bipartite Homology & Parity Balance (Z2 2-coloring: even vs odd lattice sites)
2. Discrete Planar Winding & Curvature (Snaky's 90-degree elbow joint vs straight stem)
3. Topological Connectivity, Boundary & Euler Characteristic (chi = V - E + F)
4. Dual-Graph Cut / Percolation Obstruction (Breaker boundary chain vs Maker pathway)
5. Multi-front Homological Dispersion (quadrupole moment & axis-balanced expansion)

Tests scalability across board dimensions (Radius 3 = 7x7, Radius 4 = 9x9, Radius 5 = 11x11).
Enforces strict CPU <= 25% single-threaded budget.
"""
from __future__ import annotations

import os
import sys
import random
import time
from pathlib import Path
import numpy as np

# Strict single-threading to keep CPU <= 25%
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
# Topological Maker Archetypes
# ---------------------------------------------------------------------------
TOPOLOGICAL_MAKER_ARCHETYPES = [
    # 0. Bipartite Homology & Parity Balance
    # Exploits the 3-even / 3-odd cell requirement of Snaky to maintain topological balance
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  active_count = 0
  t4_count = 0
  t3_count = 0
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        t4_count += 1
        score += {t4_weight:.1f}
      elif m_cnt == 3:
        t3_count += 1
        score += {t3_weight:.1f}
      else:
        score += float({base:.1f} ** m_cnt)
  # Parity balance: Snaky requires 3 even and 3 odd cells in Z^2 bipartite graph
  even_m = sum(1 for p in m_set if (p[0] + p[1]) % 2 == 0)
  odd_m = len(m_set) - even_m
  cand_is_even = (candidate[0] + candidate[1]) % 2 == 0
  parity_diff = (even_m - odd_m) if cand_is_even else (odd_m - even_m)
  if parity_diff <= 0:
    score += {parity_bonus:.1f}
  else:
    score -= {parity_penalty:.1f} * parity_diff
  if t4_count >= 2:
    score += {fork_t4:.1f} * (t4_count ** 2)
  if t3_count >= 3:
    score += {fork_t3:.1f} * (t3_count ** 1.5)
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {dist_pen:.6f}
  score += (active_count ** {dens_p:.2f}) * {dens_scale:.1f}
  return float(score)""",

    # 1. Discrete Planar Winding & Curvature Integration
    # Snaky has exactly one 90-degree elbow bend. Maker establishes orthogonal wavefronts.
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  active_count = 0
  t4_count = 0
  t3_count = 0
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        t4_count += 1
        score += {t4_w:.1f}
      elif m_cnt == 3:
        t3_count += 1
        score += {t3_w:.1f}
      else:
        score += float({base_w:.1f} ** m_cnt)
  # Topological Winding: reward orthogonal elbow connectivity to prevent collinear blocking
  has_horizontal_neighbor = (candidate[0] + 1, candidate[1]) in m_set or (candidate[0] - 1, candidate[1]) in m_set
  has_vertical_neighbor = (candidate[0], candidate[1] + 1) in m_set or (candidate[0], candidate[1] - 1) in m_set
  if has_horizontal_neighbor and has_vertical_neighbor:
    score += {elbow_bonus:.1f}  # Snaky elbow vertex
  elif has_horizontal_neighbor or has_vertical_neighbor:
    score += {linear_bonus:.1f}  # Snaky 4-stem extension
  if t4_count >= 2:
    score += {fork_mult:.1f} * (t4_count ** 2)
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {d_pen:.4f}
  score += (active_count ** 1.3) * {overlap_scale:.1f}
  return float(score)""",

    # 2. Topological Boundary Expansion & Dual Graph Evasion
    # Avoids dense clusters that Breaker can enclose; expands Euler boundary.
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  active_count = 0
  t4 = 0
  next_m = m_set | {{candidate}}
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_after = sum(1 for p in shape if p in next_m)
      if m_after == 5:
        return 1e11
      elif m_after == 4:
        t4 += 1
        score += {s4:.1f}
      else:
        score += float({b_exp:.1f} ** m_after)
  # Euler boundary: count empty neighbors (open degree) in dual grid
  open_deg = sum(1 for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)] if (candidate[0]+dx, candidate[1]+dy) not in m_set and (candidate[0]+dx, candidate[1]+dy) not in b_set)
  score += open_deg * {open_deg_w:.1f}
  # Distance to Breaker's dual cut barrier
  if breaker_cells:
    min_b_dist = min(abs(candidate[0] - b[0]) + abs(candidate[1] - b[1]) for b in breaker_cells)
    if min_b_dist >= {escape_dist:d}:
      score += {escape_bonus:.1f}
    elif min_b_dist <= 1:
      score -= {smother_pen:.1f}
  if t4 >= 2:
    score += {t4_fork:.1f} * (t4 ** 2)
  score += (active_count ** 1.35) * {active_w:.1f}
  score -= (candidate[0]**2 + candidate[1]**2) * {cent_pen:.6f}
  return float(score)""",

    # 3. Covariance Matrix & Spatial Dispersion Multipole
    # Ensures multi-axial expansion (bivariate Gaussian dispersion)
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  active_count = 0
  t4_count = 0
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        t4_count += 1
        score += {s4_cov:.1f}
      elif m_cnt == 3:
        score += {s3_cov:.1f}
      else:
        score += float({base_cov:.1f} ** m_cnt)
  if len(maker_cells) >= 2:
    mean_x = sum(c[0] for c in maker_cells) / len(maker_cells)
    mean_y = sum(c[1] for c in maker_cells) / len(maker_cells)
    dx = candidate[0] - mean_x
    dy = candidate[1] - mean_y
    if abs(dx) > abs(dy):
      score += abs(dy) * {axis_bal:.1f}
    else:
      score += abs(dx) * {axis_bal:.1f}
  if t4_count >= 2:
    score += {t4_mult:.1f} * (t4_count ** 2)
  r_sq = candidate[0] ** 2 + candidate[1] ** 2
  if {r_lo:.1f} <= r_sq <= {r_hi:.1f}:
    score += {ring_w:.1f}
  score += (active_count ** 1.3) * {dens_cov:.1f}
  return float(score)""",
]

# ---------------------------------------------------------------------------
# Topological Breaker Archetypes
# ---------------------------------------------------------------------------
TOPOLOGICAL_BREAKER_ARCHETYPES = [
    # 0. Dual Graph Cut & Percolation Barrier
    # Builds a dual topological cut separating Maker's high-threat clusters
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  threat_5 = 0
  threat_4 = 0
  threat_3 = 0
  blocked_shapes = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 5:
        threat_5 += 1
      elif m_cnt == 4:
        threat_4 += 1
      elif m_cnt == 3:
        threat_3 += 1
      blocked_shapes += 1
  if threat_5 > 0:
    return 1e14 * threat_5
  if threat_4 >= 2:
    score += {t4_double:.1f} * (threat_4 ** 2)
  elif threat_4 == 1:
    score += {t4_single:.1f}
  score += threat_3 * {t3_w:.1f}
  # Dual graph cut: place cell adjacent to Breaker chain (form continuous barrier)
  if breaker_cells:
    min_dist_b = min(abs(candidate[0] - b[0]) + abs(candidate[1] - b[1]) for b in breaker_cells)
    if min_dist_b == 1:
      score += {barrier_adj:.1f}
    elif min_dist_b == 2:
      score += {barrier_diag:.1f}
  if maker_cells:
    min_dist_m = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    if min_dist_m <= 1:
      score += {smother_bonus:.1f}
    elif min_dist_m >= 4:
      score -= {far_m_pen:.1f}
  score += (blocked_shapes ** 1.3) * {dens_scale:.1f}
  score -= (abs(candidate[0]) + abs(candidate[1])) * {center_pen:.4f}
  return float(score)""",

    # 1. Parity Inversion & Bipartite Blockade
    # Denies Maker the requisite even/odd cell balance for completing Snaky
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  threat_5 = 0
  threat_4 = 0
  threat_3 = 0
  blocked_shapes = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 5:
        threat_5 += 1
      elif m_cnt == 4:
        threat_4 += 1
      elif m_cnt == 3:
        threat_3 += 1
      blocked_shapes += 1
  if threat_5 > 0:
    return 1e14 * threat_5
  if threat_4 >= 2:
    score += {t4_choke:.1f} * (threat_4 ** 2)
  elif threat_4 == 1:
    score += {t4_s:.1f}
  score += threat_3 * {t3_s:.1f}
  # Parity Blockade: target the parity class that Maker is currently starved of
  even_m = sum(1 for p in m_set if (p[0] + p[1]) % 2 == 0)
  odd_m = len(m_set) - even_m
  cand_is_even = (candidate[0] + candidate[1]) % 2 == 0
  if (even_m > odd_m and not cand_is_even) or (odd_m > even_m and cand_is_even):
    score += {parity_starve:.1f}
  if maker_cells:
    min_m = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    score += (4 - min_m) * {smother_w:.1f}
  score += (blocked_shapes ** 1.25) * {b_dens:.1f}
  return float(score)""",
]

def sample_topological_maker(arch_idx: int | None = None) -> str:
    if arch_idx is None:
        arch_idx = random.randint(0, len(TOPOLOGICAL_MAKER_ARCHETYPES) - 1)
    tmpl = TOPOLOGICAL_MAKER_ARCHETYPES[arch_idx]
    if arch_idx == 0:
        return tmpl.format(
            t4_weight=random.uniform(50000.0, 150000.0),
            t3_weight=random.uniform(1500.0, 6000.0),
            base=random.uniform(6.0, 10.5),
            parity_bonus=random.uniform(3000.0, 15000.0),
            parity_penalty=random.uniform(1000.0, 8000.0),
            fork_t4=random.uniform(15000000.0, 50000000.0),
            fork_t3=random.uniform(300000.0, 2000000.0),
            dist_pen=random.uniform(0.001, 0.015),
            dens_p=random.uniform(1.2, 1.45),
            dens_scale=random.uniform(2.0, 7.0),
        )
    elif arch_idx == 1:
        return tmpl.format(
            t4_w=random.uniform(60000.0, 160000.0),
            t3_w=random.uniform(2000.0, 8000.0),
            base_w=random.uniform(7.0, 11.0),
            elbow_bonus=random.uniform(8000.0, 35000.0),
            linear_bonus=random.uniform(3000.0, 12000.0),
            fork_mult=random.uniform(20000000.0, 60000000.0),
            d_pen=random.uniform(0.01, 0.06),
            overlap_scale=random.uniform(2.5, 8.0),
        )
    elif arch_idx == 2:
        return tmpl.format(
            s4=random.uniform(50000.0, 120000.0),
            b_exp=random.uniform(6.5, 10.5),
            open_deg_w=random.uniform(2000.0, 10000.0),
            escape_dist=random.choice([2, 3, 4]),
            escape_bonus=random.uniform(10000.0, 40000.0),
            smother_pen=random.uniform(3000.0, 15000.0),
            t4_fork=random.uniform(20000000.0, 50000000.0),
            active_w=random.uniform(2.0, 6.5),
            cent_pen=random.uniform(0.002, 0.012),
        )
    elif arch_idx == 3:
        return tmpl.format(
            s4_cov=random.uniform(50000.0, 140000.0),
            s3_cov=random.uniform(1500.0, 6000.0),
            base_cov=random.uniform(6.5, 10.0),
            axis_bal=random.uniform(1000.0, 8000.0),
            t4_mult=random.uniform(15000000.0, 45000000.0),
            r_lo=random.uniform(2.0, 5.0),
            r_hi=random.uniform(10.0, 18.0),
            ring_w=random.uniform(5000.0, 20000.0),
            dens_cov=random.uniform(2.0, 6.0),
        )
    return tmpl

def sample_topological_breaker(arch_idx: int | None = None) -> str:
    if arch_idx is None:
        arch_idx = random.randint(0, len(TOPOLOGICAL_BREAKER_ARCHETYPES) - 1)
    tmpl = TOPOLOGICAL_BREAKER_ARCHETYPES[arch_idx]
    if arch_idx == 0:
        return tmpl.format(
            t4_double=random.uniform(25000000.0, 60000000.0),
            t4_single=random.uniform(800000.0, 3000000.0),
            t3_w=random.uniform(5000.0, 25000.0),
            barrier_adj=random.uniform(10000.0, 50000.0),
            barrier_diag=random.uniform(5000.0, 25000.0),
            smother_bonus=random.uniform(8000.0, 30000.0),
            far_m_pen=random.uniform(3000.0, 12000.0),
            dens_scale=random.uniform(3.0, 10.0),
            center_pen=random.uniform(0.01, 0.08),
        )
    elif arch_idx == 1:
        return tmpl.format(
            t4_choke=random.uniform(30000000.0, 70000000.0),
            t4_s=random.uniform(1000000.0, 4000000.0),
            t3_s=random.uniform(6000.0, 30000.0),
            parity_starve=random.uniform(8000.0, 35000.0),
            smother_w=random.uniform(2000.0, 8000.0),
            b_dens=random.uniform(3.0, 9.0),
        )
    return tmpl

def run_topological_evolution(num_generations: int = 25, pop_size: int = 8, grid_radius: int = 4):
    board_size = 2 * grid_radius + 1
    print("=" * 70)
    print(f"Topological FunSearch Mock Evolution: Snaky on {board_size}x{board_size} (Radius {grid_radius})")
    print(f"Generations: {num_generations} | Population: {pop_size} Maker & Breaker Candidates")
    print("Topological Invariants: Bipartite Parity, Winding Curvature, Dual Cut")
    print("=" * 70)
    
    # Load established Grandmaster benchmarks
    p_gm_maker = FS2_DIR / "strategies/maker/rank_9x9_grandmaster_maker.py"
    fn_gm_maker = load_strategy_from_file(str(p_gm_maker), "priority")
    
    p_gm_breaker = FS2_DIR / "strategies/breaker/rank_9x9_grandmaster_breaker.py"
    fn_gm_breaker = load_strategy_from_file(str(p_gm_breaker), "breaker_priority")
    
    p_ult = FS2_DIR / "strategies/breaker/rank_9x9_ultimate_slayer.py"
    fn_ult_breaker = load_strategy_from_file(str(p_ult), "breaker_priority")
    
    best_maker_code = None
    best_maker_score = -1.0
    best_maker_max_c = 0
    best_maker_turns = 999
    
    best_breaker_code = None
    best_breaker_score = -1.0
    
    maker_wins_total = 0
    breaker_wins_total = 0
    
    start_time = time.time()
    
    for gen in range(num_generations):
        # 1. Generate Topological Maker Candidates
        candidates_maker = [sample_topological_maker() for _ in range(pop_size)]
        
        for m_idx, m_code in enumerate(candidates_maker):
            fn_m, _ = compile_maker_func(m_code)
            if fn_m is None:
                continue
            
            # Test against GM Breaker
            res1 = run_match(fn_m, fn_gm_breaker, grid_radius=grid_radius)
            # Test against Ultimate Slayer
            res2 = run_match(fn_m, fn_ult_breaker, grid_radius=grid_radius)
            
            score = 0.0
            if res1['maker_won']:
                score += 1000.0 - res1['turns'] * 10
                maker_wins_total += 1
            else:
                score += res1['max_cells_in_shape'] * 50.0 + res1['turns']
                breaker_wins_total += 1
                
            if res2['maker_won']:
                score += 1000.0 - res2['turns'] * 10
                maker_wins_total += 1
            else:
                score += res2['max_cells_in_shape'] * 50.0 + res2['turns']
                breaker_wins_total += 1
                
            max_c = max(res1['max_cells_in_shape'], res2['max_cells_in_shape'])
            if score > best_maker_score:
                best_maker_score = score
                best_maker_code = m_code
                best_maker_max_c = max_c
                best_maker_turns = res1['turns'] if res1['maker_won'] else res2['turns']
                print(f"  [Gen {gen:02d} M#{m_idx:02d}] Top Maker! Score: {score:.1f} | MaxCells: {max_c}/6 (vs GM: {'W' if res1['maker_won'] else 'L'} in {res1['turns']}t, vs Ult: {'W' if res2['maker_won'] else 'L'} in {res2['turns']}t)")

        # 2. Generate Topological Breaker Candidates
        candidates_breaker = [sample_topological_breaker() for _ in range(pop_size)]
        for b_idx, b_code in enumerate(candidates_breaker):
            fn_b, _ = compile_breaker_func(b_code)
            if fn_b is None:
                continue
            
            # Test against GM Maker
            res_b = run_match(fn_gm_maker, fn_b, grid_radius=grid_radius)
            
            score_b = 0.0
            if not res_b['maker_won']:
                # Breaker won / denied Maker
                score_b += 500.0 + (6 - res_b['max_cells_in_shape']) * 100.0 + (50 - res_b['turns'])
            else:
                score_b -= res_b['turns'] * 10
                
            if score_b > best_breaker_score:
                best_breaker_score = score_b
                best_breaker_code = b_code
                print(f"  [Gen {gen:02d} B#{b_idx:02d}] Top Breaker! Score: {score_b:.1f} | Kept Maker to {res_b['max_cells_in_shape']}/6 in {res_b['turns']}t")
                
        time.sleep(0.04)
        
        if (gen + 1) % 5 == 0 or gen == num_generations - 1:
            elapsed = time.time() - start_time
            print(f"--- Completed Generation {gen+1}/{num_generations} ({elapsed:.1f}s) | Maker Wins: {maker_wins_total} | Breaker Wins: {breaker_wins_total} ---")

    print("\n" + "=" * 70)
    print("TOPOLOGICAL EVOLUTION RESULTS:")
    total_matches = maker_wins_total + breaker_wins_total
    print(f"Total Matches Played: {total_matches}")
    print(f"Maker Total Wins: {maker_wins_total}")
    print(f"Breaker Total Wins: {breaker_wins_total}")
    if total_matches > 0:
        print(f"Maker Win Rate: {maker_wins_total / total_matches * 100:.2f}%")
        print(f"Breaker Win Rate: {breaker_wins_total / total_matches * 100:.2f}%")
    print(f"Best Maker Max Snaky Completion: {best_maker_max_c}/6")
    print("=" * 70)
    
    out_dir = Path("strategies/topological")
    out_dir.mkdir(exist_ok=True, parents=True)
    
    if best_maker_code:
        maker_file = out_dir / "best_topological_maker.py"
        full_code = f'"""Topological Snaky Maker Strategy (Bipartite Homology & Winding Curvature)"""\nfrom typing import List, Tuple\n\ndef score_candidate_maker(candidate: Tuple[int, int], maker_cells: List[Tuple[int, int]], breaker_cells: List[Tuple[int, int]], active_shapes: List[List[Tuple[int, int]]]) -> float:\n{best_maker_code}\n'
        maker_file.write_text(full_code)
        print(f"Saved: {maker_file}")
        
    if best_breaker_code:
        breaker_file = out_dir / "best_topological_breaker.py"
        full_code = f'"""Topological Snaky Breaker Strategy (Dual Cut & Parity Blockade)"""\nfrom typing import List, Tuple\n\ndef score_candidate_breaker(candidate: Tuple[int, int], maker_cells: List[Tuple[int, int]], breaker_cells: List[Tuple[int, int]], active_shapes: List[List[Tuple[int, int]]]) -> float:\n{best_breaker_code}\n'
        breaker_file.write_text(full_code)
        print(f"Saved: {breaker_file}")

if __name__ == "__main__":
    run_topological_evolution(num_generations=20, pop_size=6, grid_radius=4)
