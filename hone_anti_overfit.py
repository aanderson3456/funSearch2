"""Anti-Overfitting Multi-Opponent Co-Honing for Maker and Breaker.

Hones both:
1. Breaker Slayer Lineage -> Robust Grandmaster Breaker
   Evaluated against a battery of 11 diverse Maker challengers (including Cracked Maker,
   Breakthrough Decoy, 15-Turn Fork, Minimax TSS, 2-Ply Lookahead, Parity, etc.)
2. Cracked Maker Lineage -> Robust Grandmaster Maker
   Evaluated against a battery of 10 diverse Breaker challengers (including Patched Slayer,
   Original Slayer, 2-Ply Fork Blocker, 1-Lookahead, Checkerboard Parity, Centripetal, etc.)

Ensures neither strategy overfits to a single opponent's idiosyncrasy.
CPU usage strictly <= 25% (OMP/MKL single-threaded, throttled sleep).
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Any, Callable

# Strictly cap thread usage for CPU <= 25%
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
from test_10x10_experiment import get_grid_shapes, run_match_arbitrary

# ---------------------------------------------------------------------------
# Build Comprehensive Diverse Opponent Batteries
# ---------------------------------------------------------------------------
def build_diverse_maker_battery(grid_radius: int = 4):
    all_shapes = get_board_shapes(grid_radius)
    battery = []

    # 1. Cracked Maker (Turn 10 champion)
    p_cracked = FS2_DIR / "strategies/maker/rank_9x9_cracked_maker.py"
    if p_cracked.exists():
        fn, _ = compile_maker_func(p_cracked.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Cracked Maker (Turn 10)", fn))

    # 2. Breakthrough Decoy Maker (11-Turn anti-smothering)
    p_decoy = FS2_DIR / "strategies/maker/rank_9x9_breakthrough.py"
    if p_decoy.exists():
        fn, _ = compile_maker_func(p_decoy.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Breakthrough Decoy Maker", fn))

    # 3. 15-Turn 3-Way Compound Fork Maker
    p_plumb = FS2_DIR / "strategies/maker/rank_plumb_latest.py"
    if p_plumb.exists():
        fn, _ = compile_maker_func(p_plumb.read_text().split(":\n", 1)[1])
        if fn: battery.append(("15-Turn 3-Way Fork Maker", fn))

    # 4. 2-Ply Compound Threat Lookahead Maker
    def two_ply_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        test_m = m_set | {c}
        c5 = sum(1 for s in active if sum(1 for p in s if p in test_m) == 5)
        if c5 >= 2: return 1e9 * c5
        c4 = sum(1 for s in active if sum(1 for p in s if p in test_m) == 4)
        if c4 >= 3: return 1e7 * c4
        elif c4 == 2: return 1e5 * c4
        overlap = sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s)
        dist = abs(c[0]) + abs(c[1])
        return float(overlap - dist * 0.05)
    battery.append(("2-Ply Compound Lookahead", two_ply_maker))

    # 5. Minimax Threat-Space Deep Search (TSS)
    def minimax_tss_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        score = 0.0
        for s in active:
            if c in s:
                m_cnt = sum(1 for p in s if p in m_set)
                if m_cnt == 4: score += 500000.0
                elif m_cnt == 3: score += 15000.0
                elif m_cnt == 2: score += 500.0
                else: score += 10.0
        score -= (c[0] ** 2 + c[1] ** 2) * 0.01
        return float(score)
    battery.append(("Minimax TSS Search", minimax_tss_maker))

    # 6. 1-Lookahead Greedy Overlap
    def greedy_overlap_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        return float(sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s))
    battery.append(("Greedy Overlap Maker", greedy_overlap_maker))

    # 7. Checkerboard Parity (2x2) Paving
    def checkerboard_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        is_cb = ((c[0] // 2) + (c[1] // 2)) % 2 == 0
        score = sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s)
        return float(score + (15000.0 if is_cb else 0.0))
    battery.append(("Checkerboard Parity (2x2)", checkerboard_maker))

    # 8. Topological (3x3) Paving
    def topo_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        is_ht = ((c[0] // 3) + (c[1] // 3)) % 2 == 0
        score = sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s)
        return float(score + (15000.0 if is_ht else 0.0))
    battery.append(("Topological Paving (3x3)", topo_maker))

    # 9. Centripetal Counter-Oscillator
    def oscillator_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        score = 0.0
        for s in active:
            if c in s:
                m_cnt = sum(1 for p in s if p in m_set)
                score += float(8.0 ** m_cnt)
                if m_cnt == 4: score += 50000.0
        r_sq = c[0] ** 2 + c[1] ** 2
        if 2.0 <= r_sq <= 10.0: score += 6000.0
        return float(score)
    battery.append(("Counter-Oscillator Maker", oscillator_maker))

    # 10. Boost Champion Maker 960.00
    p_m960 = FS2_DIR / "strategies/maker/rank_boost_score_960.00.py"
    if p_m960.exists():
        fn, _ = compile_maker_func(p_m960.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Boost Maker 960.00", fn))

    # 11. Baseline Random Maker
    def random_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        return float(random.random())
    battery.append(("Random Maker Baseline", random_maker))

    return battery


def build_diverse_breaker_battery(grid_radius: int = 4):
    all_shapes = get_board_shapes(grid_radius)
    battery = []

    # 1. Ultimate Breaker Slayer (Original)
    p_ult = FS2_DIR / "strategies/breaker/rank_9x9_ultimate_slayer.py"
    if p_ult.exists():
        fn, _ = compile_breaker_func(p_ult.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Ultimate Slayer Original", fn))

    # 2. Patched Slayer (Dominant 5-threat block)
    p_slayer_base = FS2_DIR / "strategies/breaker/rank_9x9_ultimate_slayer.py"
    if p_slayer_base.exists():
        fn_base = load_strategy_from_file(str(p_slayer_base), "breaker_priority")
        def patched_slayer(c, m_cells, b_cells, active):
            m_set = set(m_cells)
            has_5 = any(sum(1 for p in s if p in m_set) == 5 and c in s for s in active)
            score = fn_base(c, m_cells, b_cells, active)
            if has_5: score += 1e12
            return score
        battery.append(("Patched Ultimate Slayer", patched_slayer))

    # 3. 2-Ply Fork-Blocking Breaker
    def two_ply_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        f4 = sum(1 for s in active if c in s and sum(1 for p in s if p in m_set) == 4)
        if f4 >= 2: return 5e8 * f4
        f3 = sum(1 for s in active if c in s and sum(1 for p in s if p in m_set) == 3)
        if f3 >= 2: return 1e6 * f3
        return float(sum(8 ** sum(1 for p in s if p in m_set) for s in active if c in s))
    battery.append(("2-Ply Fork-Blocker", two_ply_breaker))

    # 4. 1-Lookahead Breaker
    def one_look_ahead_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        return float(sum(1 for s in active if c in s))
    battery.append(("1-Lookahead Breaker", one_look_ahead_breaker))

    # 5. Checkerboard Parity (2x2) Breaker
    def cb_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        is_cb = ((c[0] // 2) + (c[1] // 2)) % 2 == 0
        score = sum(1 for s in active if c in s)
        return float(score + (12000.0 if is_cb else 0.0))
    battery.append(("Checkerboard Breaker", cb_breaker))

    # 6. Topological (3x3) Breaker
    def topo_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        is_ht = ((c[0] // 3) + (c[1] // 3)) % 2 == 0
        score = sum(1 for s in active if c in s)
        return float(score + (12000.0 if is_ht else 0.0))
    battery.append(("Topological (3x3) Breaker", topo_breaker))

    # 7. Centripetal Perimeter Constrictor
    def centripetal_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        score = sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s)
        # Strong centripetal pull toward board center
        dist = abs(c[0]) + abs(c[1])
        score -= dist * 25.0
        return float(score)
    battery.append(("Centripetal Constrictor", centripetal_breaker))

    # 8. 9x9 Breaker Slayer (Prior)
    p_slayer_prior = FS2_DIR / "strategies/breaker/rank_9x9_slayer.py"
    if p_slayer_prior.exists():
        fn, _ = compile_breaker_func(p_slayer_prior.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Prior Slayer Champion", fn))

    # 9. Boost Champion Breaker 1245.00
    p_b1245 = FS2_DIR / "strategies/breaker/rank_boost_score_1245.00.py"
    if p_b1245.exists():
        fn, _ = compile_breaker_func(p_b1245.read_text().split(":\n", 1)[1])
        if fn: battery.append(("Boost Breaker 1245.00", fn))

    # 10. Baseline Random Breaker
    def random_breaker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e12
        return float(random.random())
    battery.append(("Random Breaker Baseline", random_breaker))

    return battery


# ---------------------------------------------------------------------------
# Evolutionary Templates for Robust Champions
# ---------------------------------------------------------------------------
ROBUST_BREAKER_TEMPLATES = [
    # Template A: Multi-Scale Choke with Absolute 5-Threat Dominance & Multi-Layer Smothering
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  # Absolute 5-threat override: must strictly dominate any combination of lower threats
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e14
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
  # Exponential multi-fork choke
  if m_threat_4 >= 2:
    score += {fork4_scale:.1f} * (m_threat_4 ** {fork4_exp:.2f})
  elif m_threat_4 == 1:
    score += {single4_bonus:.1f}
  if m_threat_3 >= 2:
    score += {fork3_scale:.1f} * (m_threat_3 ** 1.5)
  # Smothering gradient: suppress freedom of movement around all maker stones
  if maker_cells:
    min_dist = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    if min_dist <= 1:
      score += {smother_adj:.1f}
    elif min_dist == 2:
      score += {smother_diag:.1f}
  # Parity suppression: contest Maker's parity preference
  if ((candidate[0] // {cb_k:d}) + (candidate[1] // {cb_k:d})) % 2 == 0:
    score += {cb_contest:.1f}
  score += (overlap ** {ov_exp:.2f}) * {ov_scale:.2f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {center_pen:.4f}
  return float(score)""",

    # Template B: Virtual Double-4 Threat Prediction + Centripetal Clamping
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e14
  score = 0.0
  next_b = b_set | {{candidate}}
  # Count active shapes preserved vs killed
  shapes_killed = sum(1 for s in active_shapes if candidate in s)
  c4_killed = 0
  c3_killed = 0
  for s in active_shapes:
    if candidate in s:
      m_c = sum(1 for p in s if p in m_set)
      if m_c == 4: c4_killed += 1
      elif m_c == 3: c3_killed += 1
  score += c4_killed * {c4_val:.1f}
  score += c3_killed * {c3_val:.1f}
  if c4_killed >= 2:
    score += {c4_multi:.1f}
  # Distance to recent Maker move
  if maker_cells:
    last_m = maker_cells[-1]
    d_last = abs(candidate[0] - last_m[0]) + abs(candidate[1] - last_m[1])
    if d_last <= 1: score += {last_adj:.1f}
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {cent_sq:.6f}
  score += float(shapes_killed) * {sk_weight:.2f}
  return float(score)""",
]

ROBUST_MAKER_TEMPLATES = [
    # Template A: Parity Modulation + Deep Compound Fork + Decoy Switching
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  # Immediate win
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e14
  score = 0.0
  next_m = m_set | {{candidate}}
  f5_created = 0
  f4_created = 0
  f3_created = 0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_after = sum(1 for p in shape if p in next_m)
      if m_after == 5: f5_created += 1
      elif m_after == 4: f4_created += 1
      elif m_after == 3: f3_created += 1
  if f5_created >= 2:
    return 1e12 * f5_created  # Lethal double 5-threat fork!
  elif f5_created == 1:
    score += {f5_single:.1f}
  if f4_created >= 3:
    score += {f4_tri:.1f}
  elif f4_created == 2:
    score += {f4_dual:.1f}
  elif f4_created == 1:
    score += {f4_single:.1f}
  score += f3_created * {f3_weight:.1f}
  # Modular Parity alignment
  if ((candidate[0] // {p_mod:d}) + (candidate[1] // {p_mod:d})) % 2 == 0:
    score += {p_bonus:.1f}
  # Decoy evasion: avoid dense breaker clusters
  if breaker_cells:
    min_b = min(abs(candidate[0] - b[0]) + abs(candidate[1] - b[1]) for b in breaker_cells)
    if min_b >= 3: score += {decoy_b:.1f}
    elif min_b <= 1: score -= {smother_evade:.1f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {c_pen:.4f}
  score += (active_count ** 1.35) * {dens_sc:.2f}
  return float(score)""",

    # Template B: Dual-Center Expansion + Orthogonal Dispersion
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e14
  score = 0.0
  threat_4 = 0
  threat_3 = 0
  overlap = 0
  weights = {{0: 1.0, 1: {w1:.1f}, 2: {w2:.1f}, 3: {w3:.1f}, 4: {w4:.1f}}}
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
      if m_cnt == 4: threat_4 += 1
      elif m_cnt == 3: threat_3 += 1
  if threat_4 >= 2: score += {fork4_b:.1f} * (threat_4 ** 2)
  if threat_3 >= 2: score += {fork3_b:.1f} * (threat_3 ** 1.5)
  # Ring distance bonus: develop threats in concentric ring
  r_sq = candidate[0] ** 2 + candidate[1] ** 2
  if {r1:.1f} <= r_sq <= {r2:.1f}:
    score += {ring_b:.1f}
  score += (overlap ** {ov_e:.2f}) * {ov_m:.2f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {dist_m_pen:.4f}
  return float(score)""",
]

def sample_robust_breaker() -> str:
    tmpl_id = random.choice([0, 1])
    if tmpl_id == 0:
        return ROBUST_BREAKER_TEMPLATES[0].format(
            w1=random.uniform(3.0, 8.0),
            w2=random.uniform(25.0, 60.0),
            w3=random.uniform(800.0, 3000.0),
            w4=random.uniform(50000.0, 150000.0),
            fork4_scale=random.uniform(20000000.0, 60000000.0),
            fork4_exp=random.uniform(1.8, 2.3),
            single4_bonus=random.uniform(200000.0, 800000.0),
            fork3_scale=random.uniform(80000.0, 350000.0),
            smother_adj=random.uniform(3000.0, 9000.0),
            smother_diag=random.uniform(1000.0, 4000.0),
            cb_k=random.choice([2, 3]),
            cb_contest=random.uniform(1000.0, 6000.0),
            ov_exp=random.uniform(1.2, 1.55),
            ov_scale=random.uniform(2.0, 6.5),
            center_pen=random.uniform(0.01, 0.05),
        )
    else:
        return ROBUST_BREAKER_TEMPLATES[1].format(
            c4_val=random.uniform(100000.0, 400000.0),
            c3_val=random.uniform(3000.0, 15000.0),
            c4_multi=random.uniform(15000000.0, 50000000.0),
            last_adj=random.uniform(3000.0, 10000.0),
            cent_sq=random.uniform(0.002, 0.015),
            sk_weight=random.uniform(5.0, 25.0),
        )

def sample_robust_maker() -> str:
    tmpl_id = random.choice([0, 1])
    if tmpl_id == 0:
        return ROBUST_MAKER_TEMPLATES[0].format(
            f5_single=random.uniform(1000000.0, 5000000.0),
            f4_tri=random.uniform(15000000.0, 50000000.0),
            f4_dual=random.uniform(2000000.0, 8000000.0),
            f4_single=random.uniform(50000.0, 200000.0),
            f3_weight=random.uniform(2000.0, 8000.0),
            p_mod=random.choice([2, 3]),
            p_bonus=random.uniform(4000.0, 14000.0),
            decoy_b=random.uniform(4000.0, 15000.0),
            smother_evade=random.uniform(3000.0, 12000.0),
            c_pen=random.uniform(0.02, 0.10),
            dens_sc=random.uniform(1.5, 5.0),
        )
    else:
        return ROBUST_MAKER_TEMPLATES[1].format(
            w1=random.uniform(3.0, 8.0),
            w2=random.uniform(25.0, 55.0),
            w3=random.uniform(1000.0, 3000.0),
            w4=random.uniform(40000.0, 120000.0),
            fork4_b=random.uniform(10000000.0, 35000000.0),
            fork3_b=random.uniform(40000.0, 150000.0),
            r1=random.uniform(1.0, 4.0),
            r2=random.uniform(6.0, 14.0),
            ring_b=random.uniform(3000.0, 12000.0),
            ov_e=random.uniform(1.2, 1.5),
            ov_m=random.uniform(2.0, 5.0),
            dist_m_pen=random.uniform(0.02, 0.09),
        )


# ---------------------------------------------------------------------------
# Honing Engines
# ---------------------------------------------------------------------------
def hone_breaker_against_challengers(generations: int = 35):
    print("=" * 100)
    print("🛡️ PHASE 1: HONING BREAKER AGAINST 11 DIVERSE MAKER CHALLENGERS (ANTI-OVERFITTING)")
    print("=" * 100)

    maker_battery = build_diverse_maker_battery(grid_radius=4)
    print(f"[*] Opponent Battery: {len(maker_battery)} distinct Maker architectures:")
    for i, (name, _) in enumerate(maker_battery, 1):
        print(f"    {i:2d}. {name}")
    print("-" * 100)

    best_breaker_score = -float("inf")
    best_breaker_code = ""
    best_breaker_fn = None
    best_denial_rate = 0.0
    best_wins = 0

    print(f"{'GEN':<5} | {'WINS / 11':<10} | {'DENIAL %':<10} | {'AVG TURNS':<10} | {'FITNESS':<10} | {'STATUS'}")
    print("-" * 100)

    for gen in range(1, generations + 1):
        for _ in range(8):
            body = sample_robust_breaker()
            b_fn, b_code = compile_breaker_func(body)
            if not b_fn: continue

            # Evaluate against ALL 11 Makers
            wins = 0
            total_turns = 0
            max_c_all = 0
            for _, m_fn in maker_battery:
                res = run_match(m_fn, b_fn, grid_radius=4)
                if not res["maker_won"]:
                    wins += 1
                total_turns += res["turns"]
                max_c_all = max(max_c_all, res["max_cells_in_shape"])

            denial_rate = wins / len(maker_battery)
            avg_turns = total_turns / len(maker_battery)

            # Fitness: prioritize total wins, then shutdown speed and cell suppression
            fitness = (wins * 2000.0) + ((41 - avg_turns) * 20.0) - (max_c_all * 50.0)

            if fitness > best_breaker_score:
                best_breaker_score = fitness
                best_breaker_code = b_code
                best_breaker_fn = b_fn
                best_denial_rate = denial_rate
                best_wins = wins

            time.sleep(0.002)

        status = "🌟 FLAWLESS 11/11" if best_wins == len(maker_battery) else f"{best_wins}/{len(maker_battery)} DENIED"
        if gen % 5 == 0 or gen == 1:
            print(f"{gen:<5d} | {best_wins:2d} / 11     | {best_denial_rate * 100:5.1f}%    | {avg_turns:5.1f}t     | {best_breaker_score:8.1f}   | {status}")

    # Save Honed Breaker Grandmaster
    save_path = FS2_DIR / "strategies/breaker/rank_9x9_grandmaster_breaker.py"
    save_path.write_text(best_breaker_code)
    print(f"\n[+] Honed Grandmaster Breaker saved to: {save_path}")
    print(f"    Final Multi-Opponent Denial Rate: {best_wins}/{len(maker_battery)} ({best_denial_rate * 100:.1f}%)")
    return best_breaker_fn, save_path


def hone_maker_against_challengers(generations: int = 35):
    print("\n" + "=" * 100)
    print("⚔️ PHASE 2: HONING MAKER AGAINST 10 DIVERSE BREAKER CHALLENGERS (ANTI-OVERFITTING)")
    print("=" * 100)

    breaker_battery = build_diverse_breaker_battery(grid_radius=4)
    print(f"[*] Opponent Battery: {len(breaker_battery)} distinct Breaker architectures:")
    for i, (name, _) in enumerate(breaker_battery, 1):
        print(f"    {i:2d}. {name}")
    print("-" * 100)

    best_maker_score = -float("inf")
    best_maker_code = ""
    best_maker_fn = None
    best_wins = 0
    best_win_rate = 0.0

    print(f"{'GEN':<5} | {'WINS / 10':<10} | {'WIN %':<10} | {'AVG TURNS':<10} | {'FITNESS':<10} | {'STATUS'}")
    print("-" * 100)

    for gen in range(1, generations + 1):
        for _ in range(8):
            body = sample_robust_maker()
            m_fn, m_code = compile_maker_func(body)
            if not m_fn: continue

            wins = 0
            total_turns = 0
            total_c = 0
            for _, b_fn in breaker_battery:
                res = run_match(m_fn, b_fn, grid_radius=4)
                if res["maker_won"]:
                    wins += 1
                total_turns += res["turns"]
                total_c += res["max_cells_in_shape"]

            win_rate = wins / len(breaker_battery)
            avg_turns = total_turns / len(breaker_battery)
            avg_cells = total_c / len(breaker_battery)

            fitness = (wins * 2500.0) + (avg_cells * 100.0) + ((41 - avg_turns) * 15.0)

            if fitness > best_maker_score:
                best_maker_score = fitness
                best_maker_code = m_code
                best_maker_fn = m_fn
                best_wins = wins
                best_win_rate = win_rate

            time.sleep(0.002)

        status = f"PENETRATION {best_wins}/10" if best_wins > 0 else "CONTAINED"
        if gen % 5 == 0 or gen == 1:
            print(f"{gen:<5d} | {best_wins:2d} / 10     | {best_win_rate * 100:5.1f}%    | {avg_turns:5.1f}t     | {best_maker_score:8.1f}   | {status}")

    # Save Honed Maker Grandmaster
    save_path = FS2_DIR / "strategies/maker/rank_9x9_grandmaster_maker.py"
    save_path.write_text(best_maker_code)
    print(f"\n[+] Honed Grandmaster Maker saved to: {save_path}")
    print(f"    Final Multi-Opponent Win Rate: {best_wins}/{len(breaker_battery)} ({best_win_rate * 100:.1f}%)")
    return best_maker_fn, save_path


def cross_validate_grandmasters(m_fn: Callable, b_fn: Callable):
    print("\n" + "=" * 100)
    print("🏆 PHASE 3: CROSS-VALIDATION OF HONED GRANDMASTERS (9x9 & 10x10 TOURNAMENT)")
    print("=" * 100)

    # 1. Duel between Honed Grandmaster Maker vs Honed Grandmaster Breaker on 9x9
    print("[1] Head-to-Head Duel on 9x9 (Radius 4):")
    res_9 = run_match(m_fn, b_fn, grid_radius=4)
    w_9 = "Maker" if res_9["maker_won"] else "Breaker"
    print(f"    Winner: {w_9:<7} | Turns: {res_9['turns']}t | Max Cells: {res_9['max_cells_in_shape']}/6")

    # 2. Duel on 10x10
    print("\n[2] Head-to-Head Duel on 10x10 (100 cells, 432 shapes):")
    shapes_10 = get_grid_shapes(10, 10)
    res_10 = run_match_arbitrary(m_fn, b_fn, shapes_10, max_turns=50)
    w_10 = "Maker" if res_10["maker_won"] else "Breaker"
    print(f"    Winner: {w_10:<7} | Turns: {res_10['turns']}t | Max Cells: {res_10['max_cells_in_shape']}/6")

    # 3. Benchmark Grandmaster Breaker vs Full 11-Maker Battery
    print("\n[3] Full Benchmark: Grandmaster Breaker vs 11 Diverse Makers on 9x9:")
    print(f"    {'Challenger Maker':<32} | {'Result':<8} | {'Turns':<6} | {'Max Cells'}")
    print("    " + "-" * 70)
    makers = build_diverse_maker_battery(grid_radius=4)
    b_wins = 0
    for name, fn in makers:
        res = run_match(fn, b_fn, grid_radius=4)
        r = "DENIED" if not res["maker_won"] else "MAKER WIN"
        if not res["maker_won"]: b_wins += 1
        print(f"    {name:<32} | {r:<8} | {res['turns']:2d}t   | {res['max_cells_in_shape']}/6")
    print(f"    Total Breaker Score: {b_wins}/{len(makers)} ({b_wins/len(makers)*100:.1f}% Total Denial)")

    # 4. Benchmark Grandmaster Maker vs Full 10-Breaker Battery
    print("\n[4] Full Benchmark: Grandmaster Maker vs 10 Diverse Breakers on 9x9:")
    print(f"    {'Challenger Breaker':<32} | {'Result':<8} | {'Turns':<6} | {'Max Cells'}")
    print("    " + "-" * 70)
    breakers = build_diverse_breaker_battery(grid_radius=4)
    m_wins = 0
    for name, fn in breakers:
        res = run_match(m_fn, fn, grid_radius=4)
        r = "MAKER WIN" if res["maker_won"] else "BLOCKED"
        if res["maker_won"]: m_wins += 1
        print(f"    {name:<32} | {r:<8} | {res['turns']:2d}t   | {res['max_cells_in_shape']}/6")
    print(f"    Total Maker Score: {m_wins}/{len(breakers)} ({m_wins/len(breakers)*100:.1f}% Penetration Rate)")


def main():
    t_start = time.time()
    b_fn, b_path = hone_breaker_against_challengers(generations=35)
    m_fn, m_path = hone_maker_against_challengers(generations=35)
    cross_validate_grandmasters(m_fn, b_fn)
    print(f"\nTotal Anti-Overfitting Honing Pipeline Completed in {time.time() - t_start:.2f}s.")

if __name__ == "__main__":
    main()
