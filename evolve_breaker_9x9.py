"""Evolve Breaker on 9x9 (Radius 4) until Breaker forces a win.

Target: Defeat the reigning 15-turn Maker champion (rank_plumb_latest.py)
and all top Maker variants on 9x9 by total denial (max_cells <= 5).
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
# Advanced Breaker Templates for 9x9 Denial
# ---------------------------------------------------------------------------
BREAKER_TEMPLATES_9X9 = [
    # Template 1: Cluster Smothering + High-Threat Intercept
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
  # Exponential multi-fork choke
  if m_threat_4 >= 2:
    score += {fork4:.1f} * (m_threat_4 ** 2)
  if m_threat_3 >= 2:
    score += {fork3:.1f} * (m_threat_3 ** 1.5)
  # Smothering proximity to Maker's latest stone
  if maker_cells:
    last_m = maker_cells[-1]
    dx = abs(candidate[0] - last_m[0])
    dy = abs(candidate[1] - last_m[1])
    d_cheb = max(dx, dy)
    if d_cheb <= 1:
      score += {adj_bonus:.1f}
    elif d_cheb == 2:
      score += {near_bonus:.1f}
  score += (overlap ** 1.4) * {choke_scale:.2f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {dist_pen:.4f}
  return float(score)""",

    # Template 2: Anticipatory Double-Fork Neutralizer
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  overlap = 0
  double_fork_blocks = 0
  triple_fork_blocks = 0
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt >= 4:
        score += {s4:.1f}
      elif m_cnt == 3:
        score += {s3:.1f}
      else:
        score += float({base:.1f} ** m_cnt)
  # Virtual simulation: if Maker played candidate, would it form a multi-fork?
  test_m = m_set | {{candidate}}
  f5_created = 0
  f4_created = 0
  for shape in active_shapes:
    m_count_after = sum(1 for p in shape if p in test_m)
    if m_count_after == 5:
      f5_created += 1
    elif m_count_after == 4:
      f4_created += 1
  if f5_created >= 2:
    score += {f5_choke:.1f}
  if f4_created >= 3:
    score += {f4_choke:.1f}
  # Center proximity
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {dist_sq_pen:.5f}
  score += overlap * {ov_w:.1f}
  return float(score)""",

    # Template 3: Parity Paving + Choke Hybrid
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  overlap = 0
  threat_4 = 0
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        threat_4 += 1
        score += 80000.0
      elif m_cnt == 3:
        score += {p3:.1f}
      else:
        score += float(7.0 ** m_cnt)
  if threat_4 >= 2:
    score += {f4_block:.1f}
  # 2x2 Checkerboard parity bias
  is_cb = ((candidate[0] // 2) + (candidate[1] // 2)) % 2 == 0
  if is_cb:
    score += {cb_bonus:.1f}
  if maker_cells:
    last_m = maker_cells[-1]
    if abs(candidate[0] - last_m[0]) <= 1 and abs(candidate[1] - last_m[1]) <= 1:
      score += {smother:.1f}
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * {dp:.4f}
  return float(score)""",
]


def mutate_breaker() -> str:
    tmpl = random.choice([0, 1, 2])
    if tmpl == 0:
        return BREAKER_TEMPLATES_9X9[0].format(
            w1=random.uniform(3.0, 7.0),
            w2=random.uniform(25.0, 60.0),
            w3=random.uniform(500.0, 2000.0),
            w4=random.uniform(30000.0, 120000.0),
            fork4=random.uniform(5000000.0, 25000000.0),
            fork3=random.uniform(50000.0, 300000.0),
            adj_bonus=random.uniform(1500.0, 10000.0),
            near_bonus=random.uniform(300.0, 2500.0),
            choke_scale=random.uniform(2.0, 8.0),
            dist_pen=random.uniform(0.01, 0.08),
        )
    elif tmpl == 1:
        return BREAKER_TEMPLATES_9X9[1].format(
            s4=random.uniform(40000.0, 150000.0),
            s3=random.uniform(800.0, 4000.0),
            base=random.uniform(6.0, 11.0),
            f5_choke=random.uniform(10000000.0, 40000000.0),
            f4_choke=random.uniform(500000.0, 3000000.0),
            dist_sq_pen=random.uniform(0.001, 0.015),
            ov_w=random.uniform(2.0, 10.0),
        )
    else:
        return BREAKER_TEMPLATES_9X9[2].format(
            p3=random.uniform(1000.0, 5000.0),
            f4_block=random.uniform(5000000.0, 20000000.0),
            cb_bonus=random.uniform(400.0, 2500.0),
            smother=random.uniform(1500.0, 8000.0),
            dp=random.uniform(0.01, 0.07),
        )


def evaluate_breaker_9x9(b_fn: Callable, maker_battery: list[tuple[str, Callable]]) -> tuple[float, bool, int, int]:
    """Returns (fitness, beat_all_makers, min_turns, max_maker_cells_overall)."""
    total_score = 0.0
    all_won = True
    min_turns = 999
    max_c_overall = 0

    for name, m_fn in maker_battery:
        res = run_match(m_fn, b_fn, grid_radius=4)
        m_won = res["maker_won"]
        turns = res["turns"]
        max_c = res["max_cells_in_shape"]
        max_c_overall = max(max_c_overall, max_c)
        min_turns = min(min_turns, turns)

        if m_won:
            all_won = False
            total_score += float(turns * 10.0) + float((5 - max_c) * 50.0)
        else:
            # Breaker won! Massive fitness bonus
            denial_bonus = (5 - max_c) * 500.0
            total_score += 5000.0 + denial_bonus + float(turns * 20.0)

    avg_score = total_score / len(maker_battery)
    return avg_score, all_won, min_turns, max_c_overall


def main(max_generations: int = 60, samples_per_gen: int = 15):
    print("=" * 96)
    print("🎯 EVOLVING 9x9 BREAKER SLAYER UNTIL TOTAL DENIAL (MAX_CELLS <= 5)")
    print("   Targeting: 15-Turn Maker, Boost 960.00, 2-Ply Fork Maker, Rank 0 Maker")
    print("=" * 96)

    # Compile Maker Battery
    maker_battery = []
    p15 = Path("strategies/maker/rank_plumb_latest.py")
    if p15.exists():
        fn, _ = compile_maker_func(p15.read_text().split(":\n", 1)[1])
        if fn: maker_battery.append(("15-Turn Plumb Maker", fn))

    p_boost = Path("strategies/maker/rank_boost_score_960.00.py")
    if p_boost.exists():
        fn, _ = compile_maker_func(p_boost.read_text().split(":\n", 1)[1])
        if fn: maker_battery.append(("Boost Maker 960.00", fn))

    p_r0 = Path("strategies/maker/rank_0_score_300.00.py")
    if p_r0.exists():
        fn, _ = compile_maker_func(p_r0.read_text().split(":\n", 1)[1])
        if fn: maker_battery.append(("Rank 0 Maker 300.00", fn))

    # 2-Ply Fork Maker
    def two_ply_maker(c, m_cells, b_cells, active):
        m_set = set(m_cells)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5 and c in s:
                return 1e9
        f4 = sum(1 for s in active if c in s and sum(1 for p in s if p in m_set) == 4)
        if f4 >= 2: return 5e8 * f4
        return float(sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s))

    maker_battery.append(("2-Ply Fork Maker", two_ply_maker))
    print(f"[*] Loaded {len(maker_battery)} Maker champions into the test battery.")

    best_score = -float("inf")
    best_code = ""
    best_fn = None
    breaker_won_game = False

    print("-" * 96)
    print("GEN | TOP SCORE | 15-TURN MAKER CLASH | MAX CELLS | OUTCOME    | STATUS")
    print("-" * 96)

    start_time = time.time()
    for gen in range(1, max_generations + 1):
        for _ in range(samples_per_gen):
            body = mutate_breaker()
            b_fn, b_code = compile_breaker_func(body)
            if not b_fn:
                continue

            score, all_won, min_t, max_c = evaluate_breaker_9x9(b_fn, maker_battery)
            if score > best_score:
                best_score = score
                best_code = b_code
                best_fn = b_fn

            time.sleep(0.002)

        # Test against all 4 Makers in the battery
        battery_results = [run_match(m_fn, best_fn, grid_radius=4) for _, m_fn in maker_battery]
        wins = sum(1 for res in battery_results if not res["maker_won"])
        r_15 = battery_results[0]
        w_15 = "Maker" if r_15["maker_won"] else "Breaker"
        max_15 = r_15["max_cells_in_shape"]
        t_15 = r_15["turns"]

        status = f"{wins}/{len(maker_battery)} Wins"
        clash_str = f"{w_15} ({t_15:2d}t, {max_15}/6)"

        print(f"{gen:03d} | {best_score:9.1f} | {clash_str:<19} | {max_15}/6 cells  | {status:<10} | {'🏆 TOTAL SWEEP!' if wins == len(maker_battery) else 'evolving...'}")

        if wins == len(maker_battery):
            print("\n" + "🎉" * 40)
            print("🚀 BREAKER HAS WON AGAINST ALL MAKERS ON 9x9! TOTAL DENIAL ACHIEVED!")
            print("🎉" * 40 + "\n")
            breaker_won_game = True
            break

    # Save champion
    out_file = Path("strategies/breaker/rank_9x9_slayer.py")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(best_code)
    print(f"[*] Discovered Breaker Slayer saved to: {out_file}")

    # Detailed Benchmark against all battery members
    print("\n" + "=" * 96)
    print("📊 FINAL VERIFICATION: DISCOVERED BREAKER VS ALL 4 MAKER CHAMPIONS ON 9x9")
    print("=" * 96)
    for name, m_fn in maker_battery:
        res = run_match(m_fn, best_fn, grid_radius=4)
        winner = "Maker" if res["maker_won"] else "Breaker"
        verdict = "BREAKER WIN (DENIED)" if not res["maker_won"] else "Maker Win"
        print(f"{name:<25} | Winner: {winner:<7} | Turns: {res['turns']:2d} | Max Cells: {res['max_cells_in_shape']}/6 | {verdict}")


if __name__ == "__main__":
    main()
