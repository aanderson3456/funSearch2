"""Two-Phase 9x9 Duel Evolution: Maker Breakthrough -> Breaker Counter-Adaptation.

Phase 1: Evolve Maker to break through the 9x9 Breaker Slayer (rank_9x9_slayer.py)
         using multi-cluster decoys and anti-smothering dispersion.
Phase 2: Evolve Breaker to counter-adapt against the new Maker breakthrough
         using global cluster tracking and dual-focal choking.
Phase 3: Tournament verification of the newly evolved 9x9 champions.
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
# Phase 1 Maker Templates: Cracking the Smothering Defense
# ---------------------------------------------------------------------------
MAKER_TEMPLATES_9X9 = [
    # Template 1: Dual-Cluster Decoy Flanker
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
        score += 70000.0
      elif m_cnt == 3:
        t3_count += 1
        score += {t3_score:.1f}
      else:
        score += float({base:.1f} ** m_cnt)
  # Decoy switching: reward placing stones away from recent Breaker blocks
  if breaker_cells:
    last_b = breaker_cells[-1]
    dist_from_b = abs(candidate[0] - last_b[0]) + abs(candidate[1] - last_b[1])
    if dist_from_b >= 3:
      score += {decoy_bonus:.1f}
  if t4_count >= 3:
    score += {tri_fork:.1f}
  elif t4_count == 2:
    score += {dual_fork:.1f}
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {dist_sq_pen:.6f}
  score += (active_count ** {dens_exp:.2f}) * {dens_scale:.1f}
  return float(score)""",

    # Template 2: Asymmetric Perimeter Arc + Stealth 4-Branching
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
    score += {fork_4:.1f} * (threat_4 ** 2)
  if threat_3 >= 2:
    score += {fork_3:.1f} * (threat_3 ** 1.5)
  # Anti-smothering: penalize being trapped by adjacent Breaker stones
  adj_b = sum(1 for b in breaker_cells if abs(candidate[0] - b[0]) <= 1 and abs(candidate[1] - b[1]) <= 1)
  score -= adj_b * {adj_b_pen:.1f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {center_pen:.4f}
  score += (active_count ** 1.4) * {dens_m:.1f}
  return float(score)""",

    # Template 3: Virtual Multi-Threat Lookahead
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  next_m = m_set | {{candidate}}
  f5_created = 0
  f4_created = 0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_after = sum(1 for p in shape if p in next_m)
      if m_after == 5:
        f5_created += 1
        score += 80000.0
      elif m_after == 4:
        f4_created += 1
        score += {s4:.1f}
      else:
        score += float({base_v:.1f} ** m_after)
  if f5_created >= 2:
    score += {double_win:.1f}
  if f4_created >= 3:
    score += {triple_threat:.1f}
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {d_sq_p:.6f}
  return float(score)""",
]

# ---------------------------------------------------------------------------
# Phase 2 Breaker Templates: Countering Decoys with Global Choking
# ---------------------------------------------------------------------------
BREAKER_TEMPLATES_9X9 = [
    # Template 1: Global Cluster Tracking + Anti-Decoy Smothering
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
  if m_threat_4 >= 2:
    score += {fork4:.1f} * (m_threat_4 ** 2)
  if m_threat_3 >= 2:
    score += {fork3:.1f} * (m_threat_3 ** 1.5)
  # Global tracking: bonus for smothering ANY maker stone with >= 3 shape overlaps
  if maker_cells:
    min_dist_to_maker = min((abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells), default=99)
    if min_dist_to_maker <= 1:
      score += {smother_close:.1f}
    elif min_dist_to_maker == 2:
      score += {smother_mid:.1f}
  score += (overlap ** 1.4) * {choke_scale:.2f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {dist_pen:.4f}
  return float(score)""",

    # Template 2: Quadratic Anti-Perimeter Wall + Decoy Neutralizer
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  overlap = 0
  threat_4 = 0
  threat_3 = 0
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        threat_4 += 1
        score += 85000.0
      elif m_cnt == 3:
        threat_3 += 1
        score += {s3:.1f}
      else:
        score += float({base:.1f} ** m_cnt)
  if threat_4 >= 2:
    score += {f4_choke:.1f} * (threat_4 ** 2)
  if threat_3 >= 3:
    score += {tri_3_choke:.1f}
  # Quadratic perimeter patrol
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {dist_sq_pen:.6f}
  # Anti-decoy parity
  is_cb = ((candidate[0] // 2) + (candidate[1] // 2)) % 2 == 0
  if is_cb:
    score += {parity_bonus:.1f}
  score += (overlap ** {ov_exp:.2f}) * {ov_scale:.1f}
  return float(score)""",
]


def mutate_maker_9x9() -> str:
    tmpl = random.choice([0, 1, 2])
    if tmpl == 0:
        return MAKER_TEMPLATES_9X9[0].format(
            t3_score=random.uniform(800.0, 2500.0),
            base=random.uniform(6.0, 10.5),
            decoy_bonus=random.uniform(2000.0, 15000.0),
            tri_fork=random.uniform(10000000.0, 30000000.0),
            dual_fork=random.uniform(2000000.0, 8000000.0),
            dist_sq_pen=random.uniform(0.002, 0.012),
            dens_exp=random.uniform(1.2, 1.7),
            dens_scale=random.uniform(4.0, 12.0),
        )
    elif tmpl == 1:
        return MAKER_TEMPLATES_9X9[1].format(
            w1=random.uniform(3.0, 7.0),
            w2=random.uniform(20.0, 50.0),
            w3=random.uniform(500.0, 1500.0),
            w4=random.uniform(30000.0, 90000.0),
            fork_4=random.uniform(3000000.0, 15000000.0),
            fork_3=random.uniform(40000.0, 200000.0),
            adj_b_pen=random.uniform(500.0, 3500.0),
            center_pen=random.uniform(0.01, 0.08),
            dens_m=random.uniform(2.0, 8.0),
        )
    else:
        return MAKER_TEMPLATES_9X9[2].format(
            s4=random.uniform(15000.0, 50000.0),
            base_v=random.uniform(6.0, 9.5),
            double_win=random.uniform(10000000.0, 40000000.0),
            triple_threat=random.uniform(2000000.0, 10000000.0),
            d_sq_p=random.uniform(0.003, 0.015),
        )


def mutate_breaker_9x9() -> str:
    tmpl = random.choice([0, 1])
    if tmpl == 0:
        return BREAKER_TEMPLATES_9X9[0].format(
            w1=random.uniform(3.0, 6.5),
            w2=random.uniform(25.0, 60.0),
            w3=random.uniform(600.0, 2200.0),
            w4=random.uniform(40000.0, 130000.0),
            fork4=random.uniform(10000000.0, 35000000.0),
            fork3=random.uniform(80000.0, 350000.0),
            smother_close=random.uniform(1500.0, 6000.0),
            smother_mid=random.uniform(800.0, 3000.0),
            choke_scale=random.uniform(2.0, 8.0),
            dist_pen=random.uniform(0.01, 0.07),
        )
    else:
        return BREAKER_TEMPLATES_9X9[1].format(
            s3=random.uniform(900.0, 3500.0),
            base=random.uniform(6.0, 10.5),
            f4_choke=random.uniform(12000000.0, 40000000.0),
            tri_3_choke=random.uniform(100000.0, 500000.0),
            dist_sq_pen=random.uniform(0.002, 0.014),
            parity_bonus=random.uniform(500.0, 3000.0),
            ov_exp=random.uniform(1.2, 1.6),
            ov_scale=random.uniform(2.0, 8.0),
        )


# ---------------------------------------------------------------------------
# Execution Pipeline
# ---------------------------------------------------------------------------
def run_duel_9x9(maker_gens: int = 25, breaker_gens: int = 25):
    print("=" * 96)
    print("⚔️ 9x9 TWO-PHASE DUEL EVOLUTION: MAKER BREAKTHROUGH -> BREAKER COUNTER-ATTACK")
    print("=" * 96)

    # 1. Load reigning champions
    p_slayer = Path("strategies/breaker/rank_9x9_slayer.py")
    slayer_b_fn = load_strategy_from_file(str(p_slayer), "breaker_priority")
    print(f"[*] Loaded 9x9 Breaker Slayer champion: {p_slayer}")

    # =======================================================================
    # PHASE 1: EVOLVE MAKER TO PENETRATE 9x9 BREAKER SLAYER
    # =======================================================================
    print("\n" + "-" * 96)
    print("PHASE 1: EVOLVING MAKER TO PENETRATE 9x9 BREAKER SLAYER")
    print("-" * 96)
    print("GEN | TOP MAKER SCORE | VS SLAYER (Turns) | MAX CELLS | OUTCOME    | STATUS")
    print("-" * 96)

    best_maker_score = -float("inf")
    best_maker_code = ""
    best_maker_fn = None
    maker_breakthrough = False

    for gen in range(1, maker_gens + 1):
        for _ in range(12):
            body = mutate_maker_9x9()
            fn, code = compile_maker_func(body)
            if not fn:
                continue

            res = run_match(fn, slayer_b_fn, grid_radius=4)
            m_won = res["maker_won"]
            max_c = res["max_cells_in_shape"]
            turns = res["turns"]

            score = float(max_c * 50.0)
            if m_won:
                score += 5000.0 + float((40 - min(turns, 40)) * 50.0)
            else:
                score += float(turns * 10.0)

            if score > best_maker_score:
                best_maker_score = score
                best_maker_code = code
                best_maker_fn = fn

            time.sleep(0.002)

        r_check = run_match(best_maker_fn, slayer_b_fn, grid_radius=4)
        w_check = "Maker" if r_check["maker_won"] else "Breaker"
        t_check = r_check["turns"]
        c_check = r_check["max_cells_in_shape"]
        status = "BREAKTHROUGH! 🏆" if r_check["maker_won"] else "Denied (5/6)"

        print(f"{gen:03d} | {best_maker_score:15.1f} | {w_check:<7} ({t_check:2d}t)       | {c_check}/6 cells  | {status:<12} | {'MAKER WINS!' if r_check['maker_won'] else 'searching...'}")

        if r_check["maker_won"]:
            print("\n" + "🔥" * 40)
            print(f"🚀 MAKER BREAKTHROUGH ON 9x9 ACHIEVED AT GEN {gen}!")
            print(f"   Maker forced a win against Breaker Slayer in {t_check} turns (6/6 cells)!")
            print("🔥" * 40 + "\n")
            maker_breakthrough = True
            break

    # Save Maker Breakthrough
    out_m = Path("strategies/maker/rank_9x9_breakthrough.py")
    out_m.write_text(best_maker_code)
    print(f"[*] Saved Phase 1 Maker Champion to: {out_m}")

    # =======================================================================
    # PHASE 2: EVOLVE BREAKER TO COUNTER-ADAPT AND CRUSH THE NEW MAKER
    # =======================================================================
    print("\n" + "-" * 96)
    print("PHASE 2: EVOLVING BREAKER TO COUNTER-ADAPT AND CRUSH NEW MAKER")
    print("-" * 96)
    print("GEN | TOP BREAKER SCORE | VS NEW MAKER (Turns) | MAX CELLS | OUTCOME    | STATUS")
    print("-" * 96)

    target_m_fn = best_maker_fn
    best_breaker_score = -float("inf")
    best_breaker_code = ""
    best_breaker_fn = None
    breaker_counter_won = False

    for gen in range(1, breaker_gens + 1):
        for _ in range(12):
            body = mutate_breaker_9x9()
            fn, code = compile_breaker_func(body)
            if not fn:
                continue

            res = run_match(target_m_fn, fn, grid_radius=4)
            m_won = res["maker_won"]
            max_c = res["max_cells_in_shape"]
            turns = res["turns"]

            score = 0.0
            if not m_won:
                score += 5000.0 + float((5 - max_c) * 500.0) + float(turns * 20.0)
            else:
                score += float(turns * 10.0) + float((5 - max_c) * 50.0)

            if score > best_breaker_score:
                best_breaker_score = score
                best_breaker_code = code
                best_breaker_fn = fn

            time.sleep(0.002)

        r_check_b = run_match(target_m_fn, best_breaker_fn, grid_radius=4)
        w_check_b = "Maker" if r_check_b["maker_won"] else "Breaker"
        t_check_b = r_check_b["turns"]
        c_check_b = r_check_b["max_cells_in_shape"]
        status_b = "DENIED! 🛡️" if not r_check_b["maker_won"] else "Penetrated"

        print(f"{gen:03d} | {best_breaker_score:17.1f} | {w_check_b:<7} ({t_check_b:2d}t)         | {c_check_b}/6 cells  | {status_b:<12} | {'BREAKER RE-CLAIMS 9x9!' if not r_check_b['maker_won'] else 'adapting...'}")

        if not r_check_b["maker_won"]:
            print("\n" + "🛡️" * 40)
            print(f"🚀 BREAKER COUNTER-ADAPTATION SUCCESSFUL AT GEN {gen}!")
            print(f"   Breaker held New Maker to {c_check_b}/6 cells in {t_check_b} turns!")
            print("🛡️" * 40 + "\n")
            breaker_counter_won = True
            break

    # Save Ultimate Breaker
    out_b = Path("strategies/breaker/rank_9x9_ultimate_slayer.py")
    out_b.write_text(best_breaker_code)
    print(f"[*] Saved Phase 2 Ultimate Breaker Champion to: {out_b}")

    # =======================================================================
    # PHASE 3: COMPREHENSIVE TOURNAMENT
    # =======================================================================
    print("\n" + "=" * 96)
    print("🏆 FINAL TOURNAMENT MATRIX: 9x9 EVOLUTIONARY TITANS")
    print("=" * 96)
    matchups = [
        ("New Breakthrough Maker vs New Ultimate Breaker", best_maker_fn, best_breaker_fn),
        ("New Breakthrough Maker vs Breaker Slayer (Prior)", best_maker_fn, slayer_b_fn),
        ("15-Turn Maker vs New Ultimate Breaker", load_strategy_from_file("strategies/maker/rank_plumb_latest.py", "priority"), best_breaker_fn),
        ("Boost Maker (960.00) vs New Ultimate Breaker", load_strategy_from_file("strategies/maker/rank_boost_score_960.00.py", "priority"), best_breaker_fn),
    ]

    print(f"{'Matchup':<50} | Winner | Turns | Max Cells | Verdict")
    print("-" * 96)
    for name, mf, bf in matchups:
        if not mf or not bf:
            continue
        res = run_match(mf, bf, grid_radius=4)
        winner = "Maker" if res["maker_won"] else "Breaker"
        verdict = "TOTAL DENIAL (Breaker Win)" if not res["maker_won"] else "MAKER WIN (6/6)"
        print(f"{name:<50} | {winner:<6} | {res['turns']:2d}t   | {res['max_cells_in_shape']}/6     | {verdict}")


if __name__ == "__main__":
    run_duel_9x9()
