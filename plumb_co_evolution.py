"""Plumbing the Snaky Conjecture: Multi-Scale Co-Evolution (9x9 & 13x13).

Evolves Maker and Breaker heuristics using 3D MAP-Elites quality-diversity
and multi-island migration, pitted against:
1. 1-Lookahead Baselines (threat response)
2. 2-Ply Fork-Blocking & Fork-Hunting Baselines
3. Checkerboard (2x2) and Higher-Order Topological (3x3) Paving Baselines
4. Evolving Adversarial Champions

Evaluates simultaneously across:
- Grid Radius 4 (9x9, 81 cells)
- Grid Radius 6 (13x13, 169 cells)
"""
from __future__ import annotations

import dataclasses
import json
import os
import random
import re
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
from funsearch.core.advanced_evolution import (
    BehavioralFeatureExtractor,
    MapElitesArchive,
)

# ---------------------------------------------------------------------------
# Advanced Heuristic Templates for Maker & Breaker
# ---------------------------------------------------------------------------
MAKER_TEMPLATES = [
    # Template 1: Multi-Threat Fork Synthesizer
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  threat_4 = 0
  threat_3 = 0
  active_count = 0
  weights = {{0: 1.0, 1: {w1:.1f}, 2: {w2:.1f}, 3: {w3:.1f}, 4: {w4:.1f}, 5: 10000000.0}}
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
      if m_cnt == 4:
        threat_4 += 1
      elif m_cnt == 3:
        threat_3 += 1
  if threat_4 >= 2:
    score += {fork_4_bonus:.1f} * (threat_4 ** 2)
  if threat_3 >= 2:
    score += {fork_3_bonus:.1f} * (threat_3 ** 1.5)
  score += (active_count ** 1.3) * {density:.2f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {center_penalty:.4f}
  return float(score)""",

    # Template 2: Asymmetric Perimeter Paving & Branch Expansion
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += float({base:.1f} ** m_cnt)
      if m_cnt == 4:
        score += {instant_threat:.1f}
  # Non-linear topological dispersion
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {dist_penalty:.5f}
  score += (active_count ** {dens_exp:.2f}) * {dens_scale:.1f}
  return float(score)""",

    # Template 3: 2-Ply Anticipation Lookahead
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  next_m_set = m_set | {{candidate}}
  threat_count = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in next_m_set)
      if m_cnt == 5:
        threat_count += 1
        score += 50000.0
      elif m_cnt == 4:
        score += {p4:.1f}
      else:
        score += float(6.0 ** m_cnt)
  if threat_count >= 2:
    score += {unblockable_bonus:.1f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {dist_p:.4f}
  return float(score)""",

    # Template 4: Hybrid Perimeter Flank + 3-Way Compound Fork ($C_4 \ge 3$)
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  t4_count = 0
  t3_count = 0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        t4_count += 1
        score += 65000.0
      elif m_cnt == 3:
        t3_count += 1
        score += {t3_val:.1f}
      else:
        score += float({base_val:.1f} ** m_cnt)
  # 3-Way compound threat bonus: Breaker can block at most 1, leaving >= 2 open!
  if t4_count >= 3:
    score += {triple_fork_bonus:.1f}
  elif t4_count == 2:
    score += {double_fork_bonus:.1f}
  if t3_count >= 3:
    score += {tri_t3_bonus:.1f}
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {dist_sq_pen:.6f}
  score += (active_count ** {dens_p:.2f}) * {dens_m:.1f}
  return float(score)""",
]

BREAKER_TEMPLATES = [
    # Template 1: Dual-Fork Interceptor & Early Choke Defense
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  m_threat_4 = 0
  m_threat_3 = 0
  overlap = 0
  weights = {{0: 1.0, 1: {w1:.1f}, 2: {w2:.1f}, 3: {w3:.1f}, 4: {w4:.1f}, 5: 10000000.0}}
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
      if m_cnt == 4:
        m_threat_4 += 1
      elif m_cnt == 3:
        m_threat_3 += 1
  # Heavily intercept multi-fork convergence points:
  if m_threat_4 >= 2:
    score += {fork_block_4:.1f} * (m_threat_4 ** 2)
  if m_threat_3 >= 2:
    score += {fork_block_3:.1f} * (m_threat_3 ** 1.5)
  score += (overlap ** 1.4) * {choke_scale:.2f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {center_bias:.4f}
  return float(score)""",

    # Template 2: Spatial Paving & Convex Disruption
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt >= 4:
        score += {high_threat:.1f}
      elif m_cnt == 3:
        score += {mid_threat:.1f}
      else:
        score += float({base:.1f} ** m_cnt)
  # Parity suppression
  is_cb = ((candidate[0] // 2) + (candidate[1] // 2)) % 2 == 0
  if is_cb:
    score += {parity_bonus:.1f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {dist_pen:.4f}
  return float(score)""",

    # Template 3: Anticipatory Virtual Blockade (2-Ply Simulation)
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  fork_threats_eliminated = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        fork_threats_eliminated += 1
        score += 80000.0
      elif m_cnt == 3:
        score += {p3:.1f}
      else:
        score += float(7.0 ** m_cnt)
  if fork_threats_eliminated >= 2:
    score += {double_kill_bonus:.1f}
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {dist_sq_pen:.5f}
  return float(score)""",

    # Template 4: Dual Perimeter Patrol + Anti-Compound Choke ($C_4 \ge 3$)
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
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
        score += 95000.0
      elif m_cnt == 3:
        m_threat_3 += 1
        score += {b_t3:.1f}
      else:
        score += float({b_base:.1f} ** m_cnt)
  # Anti-compound intercept:
  if m_threat_4 >= 3:
    score += {triple_kill:.1f}
  elif m_threat_4 == 2:
    score += {double_kill:.1f}
  if m_threat_3 >= 3:
    score += {early_choke:.1f}
  # Quadratic perimeter patrol (suppresses wide flanking maneuvers):
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {b_dist_sq_pen:.6f}
  score += (overlap ** {b_ov_exp:.2f}) * {b_ov_scale:.1f}
  return float(score)""",
]


# ---------------------------------------------------------------------------
# Fixed Baseline Ensembles (1-Lookahead, 2-Ply Fork, Mathematical Pavings)
# ---------------------------------------------------------------------------
def build_baseline_ensembles(all_shapes: list[frozenset[tuple[int, int]]]):
    """Constructs fixed 1-lookahead, 2-ply fork, and paving baselines."""

    # 1. Breaker Baselines
    def one_look_ahead_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5:
                if c in s:
                    return 1e9
        return float(sum(1 for s in active if c in s))

    def two_ply_fork_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        # Immediate 5-cell block
        for s in active:
            if sum(1 for p in s if p in m_set) == 5:
                if c in s:
                    return 1e9
        # Check if candidate blocks a double-fork (two shapes reaching 5 if Maker played c)
        f4_count = 0
        for s in active:
            if c in s and sum(1 for p in s if p in m_set) == 4:
                f4_count += 1
        if f4_count >= 2:
            return 5e8 * f4_count
        return float(sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s))

    def checkerboard_breaker(c, m_cells, b_cells, active):
        is_cb = ((c[0] // 2) + (c[1] // 2)) % 2 == 0
        score = sum(1 for s in active if c in s)
        return float(score + (500.0 if is_cb else 0.0))

    def higher_topo_breaker(c, m_cells, b_cells, active):
        is_ht = ((c[0] // 3) + (c[1] // 3)) % 2 == 0
        score = sum(1 for s in active if c in s)
        return float(score + (500.0 if is_ht else 0.0))

    # 2. Maker Baselines
    def one_look_ahead_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5:
                if c in s:
                    return 1e9
        return float(sum(1 for s in active if c in s))

    def two_ply_fork_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5:
                if c in s:
                    return 1e9
        f4_count = sum(1 for s in active if c in s and sum(1 for p in s if p in m_set) == 4)
        if f4_count >= 2:
            return 5e8 * f4_count
        return float(sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s))

    def checkerboard_maker(c, m_cells, b_cells, active):
        is_cb = ((c[0] // 2) + (c[1] // 2)) % 2 == 0
        score = sum(1 for s in active if c in s)
        return float(score + (500.0 if is_cb else 0.0))

    def higher_topo_maker(c, m_cells, b_cells, active):
        is_ht = ((c[0] // 3) + (c[1] // 3)) % 2 == 0
        score = sum(1 for s in active if c in s)
        return float(score + (500.0 if is_ht else 0.0))

    # Seeded perimeter champion maker
    boost_maker_fn = load_strategy_from_file("strategies/maker/rank_boost_score_960.00.py", "priority")

    breaker_baselines = [one_look_ahead_breaker, two_ply_fork_breaker, checkerboard_breaker, higher_topo_breaker]
    maker_baselines = [one_look_ahead_maker, two_ply_fork_maker, checkerboard_maker, higher_topo_maker]
    if boost_maker_fn:
        maker_baselines.append(boost_maker_fn)
    return maker_baselines, breaker_baselines


# ---------------------------------------------------------------------------
# Fast In-Process Evaluator across Radius 4 (9x9) & Radius 6 (13x13)
# ---------------------------------------------------------------------------
def evaluate_candidate_maker(
    maker_func: Callable,
    active_breaker_func: Callable | None,
    grid_radius: int,
) -> tuple[float, float, int, bool]:
    """Returns (fitness_score, avg_turns, max_cells_formed, won_against_champ)."""
    all_shapes = get_board_shapes(grid_radius)
    _, breaker_baselines = build_baseline_ensembles(all_shapes)

    opponents = list(breaker_baselines)
    if active_breaker_func:
        opponents.insert(0, active_breaker_func)

    total_score = 0.0
    turns_list = []
    max_cells_list = []
    won_against_champ = False

    for idx, b_fn in enumerate(opponents):
        res = run_match(maker_func, b_fn, grid_radius=grid_radius)
        turns_list.append(res["turns"])
        max_cells_list.append(res["max_cells_in_shape"])

        if idx == 0 and active_breaker_func and res["maker_won"]:
            won_against_champ = True

        score = float(res["max_cells_in_shape"] * 20.0)
        if res["maker_won"]:
            score += 200.0 + (50 - min(res["turns"], 50)) * 10.0
        total_score += score

    avg_score = total_score / len(opponents)
    avg_turns = float(sum(turns_list) / len(turns_list))
    overall_max_cells = max(max_cells_list, default=0)
    return avg_score, avg_turns, overall_max_cells, won_against_champ


def evaluate_candidate_breaker(
    breaker_func: Callable,
    active_maker_func: Callable | None,
    grid_radius: int,
) -> tuple[float, float, int, bool]:
    """Returns (fitness_score, avg_turns, maker_max_cells, blocked_champ)."""
    all_shapes = get_board_shapes(grid_radius)
    maker_baselines, _ = build_baseline_ensembles(all_shapes)

    opponents = list(maker_baselines)
    if active_maker_func:
        opponents.insert(0, active_maker_func)

    total_score = 0.0
    turns_list = []
    max_cells_list = []
    blocked_champ = False

    for idx, m_fn in enumerate(opponents):
        res = run_match(m_fn, breaker_func, grid_radius=grid_radius)
        turns_list.append(res["turns"])
        max_cells_list.append(res["max_cells_in_shape"])

        if idx == 0 and active_maker_func and not res["maker_won"]:
            blocked_champ = True

        if not res["maker_won"]:
            # High reward for total denial (holding maker <= 5)
            block_quality = (5 - res["max_cells_in_shape"]) * 150.0
            total_score += 1000.0 + block_quality + res["turns"] * 5.0
        else:
            # Partial credit for delaying maker
            total_score += float(res["turns"] * 10.0)

    avg_score = total_score / len(opponents)
    avg_turns = float(sum(turns_list) / len(turns_list))
    overall_max_cells = max(max_cells_list, default=0)
    return avg_score, avg_turns, overall_max_cells, blocked_champ


# ---------------------------------------------------------------------------
# Evolution Generator
# ---------------------------------------------------------------------------
class HeuristicMutator:
    """Parametric & structural mutator for Maker & Breaker heuristics."""

    @staticmethod
    def mutate_maker() -> str:
        tmpl_idx = random.choice([0, 1, 2, 3])
        if tmpl_idx == 0:
            return MAKER_TEMPLATES[0].format(
                w1=random.uniform(3.0, 7.0),
                w2=random.uniform(20.0, 50.0),
                w3=random.uniform(400.0, 1200.0),
                w4=random.uniform(20000.0, 80000.0),
                fork_4_bonus=random.uniform(2000000.0, 10000000.0),
                fork_3_bonus=random.uniform(30000.0, 150000.0),
                density=random.uniform(1.0, 6.0),
                center_penalty=random.uniform(0.01, 0.12),
            )
        elif tmpl_idx == 1:
            return MAKER_TEMPLATES[1].format(
                base=random.uniform(6.0, 12.0),
                instant_threat=random.uniform(30000.0, 90000.0),
                dist_penalty=random.uniform(0.001, 0.02),
                dens_exp=random.uniform(1.1, 1.6),
                dens_scale=random.uniform(2.0, 8.0),
            )
        elif tmpl_idx == 2:
            return MAKER_TEMPLATES[2].format(
                p4=random.uniform(8000.0, 35000.0),
                unblockable_bonus=random.uniform(3000000.0, 9000000.0),
                dist_p=random.uniform(0.02, 0.09),
            )
        else:
            return MAKER_TEMPLATES[3].format(
                t3_val=random.uniform(800.0, 3000.0),
                base_val=random.uniform(5.5, 9.5),
                triple_fork_bonus=random.uniform(8000000.0, 25000000.0),
                double_fork_bonus=random.uniform(1500000.0, 6000000.0),
                tri_t3_bonus=random.uniform(50000.0, 250000.0),
                dist_sq_pen=random.uniform(0.002, 0.015),
                dens_p=random.uniform(1.2, 1.7),
                dens_m=random.uniform(3.0, 10.0),
            )

    @staticmethod
    def mutate_breaker() -> str:
        tmpl_idx = random.choice([0, 1, 2, 3])
        if tmpl_idx == 0:
            return BREAKER_TEMPLATES[0].format(
                w1=random.uniform(3.0, 6.0),
                w2=random.uniform(25.0, 60.0),
                w3=random.uniform(500.0, 1500.0),
                w4=random.uniform(30000.0, 100000.0),
                fork_block_4=random.uniform(3000000.0, 12000000.0),
                fork_block_3=random.uniform(40000.0, 200000.0),
                choke_scale=random.uniform(2.0, 7.0),
                center_bias=random.uniform(0.01, 0.08),
            )
        elif tmpl_idx == 1:
            return BREAKER_TEMPLATES[1].format(
                high_threat=random.uniform(40000.0, 100000.0),
                mid_threat=random.uniform(1000.0, 4000.0),
                base=random.uniform(6.0, 11.0),
                parity_bonus=random.uniform(300.0, 1500.0),
                dist_pen=random.uniform(0.01, 0.07),
            )
        elif tmpl_idx == 2:
            return BREAKER_TEMPLATES[2].format(
                p3=random.uniform(1200.0, 5000.0),
                double_kill_bonus=random.uniform(4000000.0, 15000000.0),
                dist_sq_pen=random.uniform(0.001, 0.015),
            )
        else:
            return BREAKER_TEMPLATES[3].format(
                b_t3=random.uniform(900.0, 3500.0),
                b_base=random.uniform(6.0, 10.0),
                triple_kill=random.uniform(10000000.0, 30000000.0),
                double_kill=random.uniform(4000000.0, 12000000.0),
                early_choke=random.uniform(60000.0, 250000.0),
                b_dist_sq_pen=random.uniform(0.003, 0.016),
                b_ov_exp=random.uniform(1.2, 1.6),
                b_ov_scale=random.uniform(1.5, 5.0),
            )


# ---------------------------------------------------------------------------
# Main Co-Evolution Loop Plumbing 9x9 & 13x13
# ---------------------------------------------------------------------------
def main(generations: int = 50, islands_count: int = 4, samples_per_island: int = 2):
    print("=" * 96)
    print("🚀 PLUMBING THE SNAKY CONJECTURE: 9x9 & 13x13 MULTI-SCALE CO-EVOLUTION")
    print("   Evaluating Maker vs Breaker with 2-Ply Fork Lookahead & MAP-Elites 3D Grid")
    print("=" * 96)

    # Initial Champions: load latest plumb champions if available, otherwise boost
    curr_maker_fn = (
        load_strategy_from_file("strategies/maker/rank_plumb_latest.py", "priority")
        or load_strategy_from_file("strategies/maker/rank_boost_score_960.00.py", "priority")
    )
    curr_breaker_fn = (
        load_strategy_from_file("strategies/breaker/rank_plumb_latest.py", "breaker_priority")
        or load_strategy_from_file("strategies/breaker/rank_boost_score_1245.00.py", "breaker_priority")
    )

    # MAP-Elites 3D Archives (5x5x5 = 125 niches)
    maker_archive = MapElitesArchive(grid_dims=(5, 5, 5))
    breaker_archive = MapElitesArchive(grid_dims=(5, 5, 5))

    best_maker_score = -float("inf")
    best_maker_code = ""
    best_breaker_score = -float("inf")
    best_breaker_code = ""

    telemetry_log = []

    print("-" * 96)
    print("GEN | ROLE    | SCORE (R4/R6) | 9x9 CLASH (Turns) | 13x13 CLASH (Turns) | 13x13 CELLS | MAP ELITES")
    print("-" * 96)

    for gen in range(1, generations + 1):
        # -----------------------------------------------------------------------
        # 1. Evolve Maker Candidates
        # -----------------------------------------------------------------------
        for _ in range(islands_count * samples_per_island):
            body = HeuristicMutator.mutate_maker()
            fn, code = compile_maker_func(body)
            if not fn:
                continue

            s4, t4, c4, _ = evaluate_candidate_maker(fn, curr_breaker_fn, grid_radius=4)
            s6, t6, c6, _ = evaluate_candidate_maker(fn, curr_breaker_fn, grid_radius=6)
            comp_score = 0.4 * s4 + 0.6 * s6

            class _DummyFn:
                def __init__(self, b): self.body = b
            maker_archive.add(_DummyFn(body), comp_score, {4: s4, 6: s6})

            if comp_score > best_maker_score:
                best_maker_score = comp_score
                best_maker_code = code
                curr_maker_fn = fn

            time.sleep(0.003)

        # -----------------------------------------------------------------------
        # 2. Evolve Breaker Candidates
        # -----------------------------------------------------------------------
        for _ in range(islands_count * samples_per_island):
            body = HeuristicMutator.mutate_breaker()
            fn, code = compile_breaker_func(body)
            if not fn:
                continue

            s4, t4, c4, _ = evaluate_candidate_breaker(fn, curr_maker_fn, grid_radius=4)
            s6, t6, c6, _ = evaluate_candidate_breaker(fn, curr_maker_fn, grid_radius=6)
            comp_score = 0.4 * s4 + 0.6 * s6

            class _DummyFn:
                def __init__(self, b): self.body = b
            breaker_archive.add(_DummyFn(body), comp_score, {4: s4, 6: s6})

            if comp_score > best_breaker_score:
                best_breaker_score = comp_score
                best_breaker_code = code
                curr_breaker_fn = fn

            time.sleep(0.003)

        # -----------------------------------------------------------------------
        # 3. Direct Head-to-Head Clash of Current Champions (R4 and R6)
        # -----------------------------------------------------------------------
        clash_r4 = run_match(curr_maker_fn, curr_breaker_fn, grid_radius=4)
        clash_r6 = run_match(curr_maker_fn, curr_breaker_fn, grid_radius=6)

        w_r4 = "Maker" if clash_r4["maker_won"] else "Breaker"
        w_r6 = "Maker" if clash_r6["maker_won"] else "Breaker"

        clash_r4_str = f"{w_r4} ({clash_r4['turns']:2d}t, {clash_r4['max_cells_in_shape']}/6)"
        clash_r6_str = f"{w_r6} ({clash_r6['turns']:2d}t, {clash_r6['max_cells_in_shape']}/6)"
        cov_str = f"M:{maker_archive.coverage*100:.0f}% B:{breaker_archive.coverage*100:.0f}%"

        print(f"{gen:03d} | DUEL     | M:{best_maker_score:6.1f} B:{best_breaker_score:6.1f} | {clash_r4_str:<17} | {clash_r6_str:<19} | {clash_r6['max_cells_in_shape']}/6 cells  | {cov_str}")

        telemetry_log.append({
            "generation": gen,
            "maker_best_score": best_maker_score,
            "breaker_best_score": best_breaker_score,
            "clash_r4_winner": w_r4,
            "clash_r4_turns": clash_r4["turns"],
            "clash_r4_max_cells": clash_r4["max_cells_in_shape"],
            "clash_r6_winner": w_r6,
            "clash_r6_turns": clash_r6["turns"],
            "clash_r6_max_cells": clash_r6["max_cells_in_shape"],
            "maker_archive_coverage": maker_archive.coverage,
            "breaker_archive_coverage": breaker_archive.coverage,
        })

    print("-" * 96)
    print("✅ CO-EVOLUTION COMPLETE!")
    print(f"[*] Discovered Top Maker Score:   {best_maker_score:.2f}")
    print(f"[*] Discovered Top Breaker Score: {best_breaker_score:.2f}")

    # Save artifacts
    timestamp = int(time.time())
    out_dir = Path(f"outputs/plumb_co_evolution_{timestamp}")
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "plumb_telemetry.json", "w") as f:
        json.dump(telemetry_log, f, indent=2)

    if best_maker_code:
        with open("strategies/maker/rank_plumb_latest.py", "w") as f:
            f.write(best_maker_code)

    if best_breaker_code:
        with open("strategies/breaker/rank_plumb_latest.py", "w") as f:
            f.write(best_breaker_code)

    print(f"[*] Telemetry and discovered strategies saved to {out_dir}/")


if __name__ == "__main__":
    main()
