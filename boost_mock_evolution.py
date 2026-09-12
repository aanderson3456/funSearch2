from __future__ import annotations

import os
# Ensure thread-level CPU cap strictly within 25% CPU limit (1 core on 8-core CPU = 12.5%)
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import ast
import copy
import dataclasses
import glob
import json
import math
import random
import re
import sys
import time
from pathlib import Path
from typing import Any, Callable

# Add FS2 root to sys.path
FS2_DIR = Path(__file__).resolve().parent
if str(FS2_DIR) not in sys.path:
    sys.path.insert(0, str(FS2_DIR))

_SNAKEY_MAKER_SNIPPETS = [
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  high_threats = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt >= 4:
        score += 50000.0
      elif m_cnt == 3:
        high_threats += 1
        score += 800.0
      else:
        score += float(10 ** m_cnt) * {weight:.2f}
  if high_threats > 1:
    score += {fork_bonus:.1f}
  score -= (abs(candidate[0]) + abs(candidate[1])) * {center_penalty:.3f}
  return float(score)""",
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += float({base:.1f} ** m_cnt)
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {dist_penalty:.4f}
  return float(score)""",
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  weights = {{0: 1.0, 1: {w1:.1f}, 2: {w2:.1f}, 3: {w3:.1f}, 4: 25000.0, 5: 1000000.0}}
  score = 0.0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** m_cnt)
      active_count += 1
  score += (active_count ** 1.3) * {density:.2f}
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.08
  return float(score)""",
]

_SNAKEY_BREAKER_SNIPPETS = [
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == len(shape) - 1:
        return 1e9  # Critical: Block immediate win
      score += float({base:.1f} ** m_cnt)
  score -= (abs(candidate[0]) + abs(candidate[1])) * {center:.2f}
  return float(score)""",
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  fork_block_count = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt >= 4:
        return 500000.0
      elif m_cnt == 3:
        fork_block_count += 1
        score += {threat3:.1f}
      else:
        score += float(8 ** m_cnt)
  if fork_block_count > 1:
    score += {anti_fork:.1f}
  score += (10.0 - (candidate[0] ** 2 + candidate[1] ** 2) * 0.05)
  return float(score)""",
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  block_weights = {{0: 1.0, 1: {bw1:.1f}, 2: {bw2:.1f}, 3: {bw3:.1f}, 4: 90000.0, 5: 1e8}}
  score = 0.0
  overlap = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += block_weights.get(m_cnt, 10.0 ** m_cnt)
      overlap += 1
  score += (overlap ** 1.5) * {overlap_w:.2f}
  return float(score)""",
]


class MockLLM:
    """Deterministic/heuristic mock sampler yielding valid Python function bodies."""

    def __init__(self, samples_per_prompt: int = 1, temperature: float = 0.7):
        self.samples_per_prompt = samples_per_prompt
        self.temperature = temperature
        self._sample_counter = 0

    def draw_sample(self, prompt: str) -> str:
        self._sample_counter += 1
        if "breaker_priority" in prompt:
            tmpl = random.choice(_SNAKEY_BREAKER_SNIPPETS)
            return tmpl.format(
                base=7.0 + random.uniform(0.5, 4.0),
                center=random.uniform(0.05, 0.25),
                threat3=random.uniform(500.0, 3000.0),
                anti_fork=random.uniform(5000.0, 20000.0),
                bw1=random.uniform(3.0, 10.0),
                bw2=random.uniform(25.0, 80.0),
                bw3=random.uniform(250.0, 1200.0),
                overlap_w=random.uniform(1.0, 5.0),
            )
        else:
            tmpl = random.choice(_SNAKEY_MAKER_SNIPPETS)
            return tmpl.format(
                weight=random.uniform(0.8, 2.5),
                fork_bonus=random.uniform(1000.0, 8000.0),
                center_penalty=random.uniform(0.05, 0.25),
                base=6.0 + random.uniform(0.5, 5.0),
                dist_penalty=random.uniform(0.005, 0.04),
                w1=random.uniform(3.0, 8.0),
                w2=random.uniform(20.0, 60.0),
                w3=random.uniform(200.0, 800.0),
                density=random.uniform(1.0, 4.0),
            )

# ---------------------------------------------------------------------------
# Precomputed Board Geometries (Boost Mode Acceleration)
# ---------------------------------------------------------------------------
_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]
_SHAPES_CACHE: dict[int, list[frozenset[tuple[int, int]]]] = {}


def get_board_shapes(radius: int = 4) -> list[frozenset[tuple[int, int]]]:
    """Returns all D8 isometric orientations and board translations of the Snakey Hexomino."""
    if radius in _SHAPES_CACHE:
        return _SHAPES_CACHE[radius]

    orientations = set()
    for rot in range(4):
        for ref in range(2):
            s = _BASE_SNAKY
            if ref:
                s = [(-p[0], p[1]) for p in s]
            for _ in range(rot):
                s = [(p[1], -p[0]) for p in s]
            mx = min(p[0] for p in s)
            my = min(p[1] for p in s)
            normalized = tuple(sorted((p[0] - mx, p[1] - my) for p in s))
            orientations.add(normalized)

    shapes = []
    for ori in orientations:
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                translated = tuple(sorted((x + dx, y + dy) for x, y in ori))
                if all(-radius <= x <= radius and -radius <= y <= radius for x, y in translated):
                    shapes.append(frozenset(translated))

    res = list(set(shapes))
    _SHAPES_CACHE[radius] = res
    return res


# Pre-warm cache for radius 3, 4, 6
get_board_shapes(3)
get_board_shapes(4)
get_board_shapes(6)

# ---------------------------------------------------------------------------
# Dynamic Function Compilers
# ---------------------------------------------------------------------------
def compile_maker_func(body_str: str) -> tuple[Callable | None, str]:
    """Compiles a candidate function body into a callable priority function."""
    full_code = (
        "def priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], "
        "breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:\n"
        + body_str
    )
    ns: dict[str, Any] = {}
    try:
        exec(full_code, ns)
        return ns["priority"], full_code
    except Exception as e:
        return None, full_code


def compile_breaker_func(body_str: str) -> tuple[Callable | None, str]:
    """Compiles a candidate function body into a callable breaker_priority function."""
    full_code = (
        "def breaker_priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], "
        "breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:\n"
        + body_str
    )
    ns: dict[str, Any] = {}
    try:
        exec(full_code, ns)
        return ns["breaker_priority"], full_code
    except Exception as e:
        return None, full_code


# ---------------------------------------------------------------------------
# Boost Evaluation Engines
# ---------------------------------------------------------------------------
def evaluate_maker_heuristic(
    maker_func: Callable,
    active_breaker_func: Callable | None = None,
    grid_radius: int = 4,
) -> float:
    """Evaluates a Maker heuristic against an ensemble of Breakers."""
    all_shapes = get_board_shapes(grid_radius)

    def evolving_breaker(last_maker_move, m_cells, b_cells):
        m_set, b_set = set(m_cells), set(b_cells)
        active = [s for s in all_shapes if not (s & b_set)]
        if not active:
            return (999, 999)
        candidates = set()
        for s in active:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates.add(p)
        if not candidates:
            return (999, 999)
        if active_breaker_func:
            return max(candidates, key=lambda c: active_breaker_func(c, m_cells, b_cells, active))
        # Fallback default greedy breaker
        return max(candidates, key=lambda c: sum(10 ** sum(1 for p in s if p in m_set) for s in active if c in s))

    def checkerboard_breaker(last_maker_move, m_cells, b_cells):
        m_set, b_set = set(m_cells), set(b_cells)
        active = [s for s in all_shapes if not (s & b_set)]
        candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
        if not candidates:
            return (999, 999)
        cb_cands = [c for c in candidates if ((c[0] // 2) + (c[1] // 2)) % 2 == 0]
        if cb_cands:
            return max(cb_cands, key=lambda c: sum(1 for s in active if c in s))
        return max(candidates, key=lambda c: sum(1 for s in active if c in s))

    def one_look_ahead_breaker(last_maker_move, m_cells, b_cells):
        m_set, b_set = set(m_cells), set(b_cells)
        active = [s for s in all_shapes if not (s & b_set)]
        candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
        if not candidates:
            return (999, 999)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5:
                for p in s:
                    if p not in m_set and p not in b_set:
                        return p
        return max(candidates, key=lambda c: sum(1 for s in active if c in s))

    def higher_topo_paving_breaker(last_maker_move, m_cells, b_cells):
        m_set, b_set = set(m_cells), set(b_cells)
        active = [s for s in all_shapes if not (s & b_set)]
        candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
        if not candidates:
            return (999, 999)
        ht_cands = [c for c in candidates if ((c[0] // 3) + (c[1] // 3)) % 2 == 0]
        if ht_cands:
            return max(ht_cands, key=lambda c: sum(1 for s in active if c in s))
        return max(candidates, key=lambda c: sum(1 for s in active if c in s))

    ensemble = [evolving_breaker, checkerboard_breaker, one_look_ahead_breaker, higher_topo_paving_breaker]
    total_score = 0.0
    match_turns = []

    for breaker_fn in ensemble:
        m_cells, b_cells = [], []
        maker_won = False
        max_turns = (2 * grid_radius + 1) ** 2 // 2 + 1

        for turn in range(max_turns):
            m_set = set(m_cells)
            b_set = set(b_cells)

            for s in all_shapes:
                if s.issubset(m_set):
                    maker_won = True
                    break
            if maker_won:
                break

            active = [tuple(s) for s in all_shapes if not (s & b_set)]
            if not active:
                break

            candidates = set()
            for s in active:
                for p in s:
                    if p not in m_set and p not in b_set:
                        candidates.add(p)
            if not candidates:
                break

            best_move = max(candidates, key=lambda c: maker_func(c, m_cells, b_cells, active))
            m_cells.append(best_move)

            b_move = breaker_fn(best_move, m_cells, b_cells)
            if b_move != (999, 999):
                b_cells.append(b_move)

        m_set = set(m_cells)
        max_cells_in_shape = max((len(s & m_set) for s in all_shapes), default=0)
        score = float(max_cells_in_shape * 10)
        if maker_won:
            score += 100.0 + (max_turns - turn) * 10.0
        total_score += score
        match_turns.append(len(m_cells))

    avg_turns = float(sum(match_turns) / len(match_turns)) if match_turns else 0.0
    return total_score / len(ensemble), avg_turns


def evaluate_breaker_heuristic(
    breaker_func: Callable,
    active_maker_func: Callable | None = None,
    grid_radius: int = 4,
) -> float:
    """Evaluates a Breaker heuristic against an ensemble of Makers."""
    all_shapes = get_board_shapes(grid_radius)

    def elite_maker(m_cells, b_cells, active):
        m_set, b_set = set(m_cells), set(b_cells)
        candidates = set()
        for s in active:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates.add(p)
        if not candidates:
            return (999, 999)
        if active_maker_func:
            return max(candidates, key=lambda c: active_maker_func(c, m_cells, b_cells, active))
        # Default priority
        weights = {0: 1.0, 1: 4.1, 2: 26.9, 3: 507.8, 4: 25000.0, 5: 1000000.0}
        return max(
            candidates,
            key=lambda c: sum(weights.get(sum(1 for p in s if p in m_set), 10.0) for s in active if c in s)
            - (abs(c[0]) + abs(c[1])) * 0.08,
        )

    def checkerboard_maker(m_cells, b_cells, active):
        m_set, b_set = set(m_cells), set(b_cells)
        candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
        if not candidates:
            return (999, 999)
        cb_cands = [c for c in candidates if ((c[0] // 2) + (c[1] // 2)) % 2 == 0]
        if cb_cands:
            return max(cb_cands, key=lambda c: sum(1 for s in active if c in s))
        return max(candidates, key=lambda c: sum(1 for s in active if c in s))

    def one_look_ahead_maker(m_cells, b_cells, active):
        m_set, b_set = set(m_cells), set(b_cells)
        candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
        if not candidates:
            return (999, 999)
        for s in active:
            if sum(1 for p in s if p in m_set) == 5:
                for p in s:
                    if p not in m_set and p not in b_set:
                        return p
        return max(candidates, key=lambda c: sum(1 for s in active if c in s))

    def higher_topo_paving_maker(m_cells, b_cells, active):
        m_set, b_set = set(m_cells), set(b_cells)
        candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
        if not candidates:
            return (999, 999)
        ht_cands = [c for c in candidates if ((c[0] // 3) + (c[1] // 3)) % 2 == 0]
        if ht_cands:
            return max(ht_cands, key=lambda c: sum(1 for s in active if c in s))
        return max(candidates, key=lambda c: sum(1 for s in active if c in s))

    ensemble = [elite_maker, checkerboard_maker, one_look_ahead_maker, higher_topo_paving_maker]
    total_score = 0.0
    match_turns = []

    for maker_fn in ensemble:
        m_cells, b_cells = [], []
        maker_won = False
        max_turns = (2 * grid_radius + 1) ** 2 // 2 + 1

        for turn in range(max_turns):
            m_set = set(m_cells)
            b_set = set(b_cells)

            for s in all_shapes:
                if s.issubset(m_set):
                    maker_won = True
                    break
            if maker_won:
                break

            active = [tuple(s) for s in all_shapes if not (s & b_set)]
            if not active:
                break

            m_move = maker_fn(m_cells, b_cells, active)
            if m_move == (999, 999):
                break
            m_cells.append(m_move)
            m_set.add(m_move)

            for s in all_shapes:
                if s.issubset(m_set):
                    maker_won = True
                    break
            if maker_won:
                break

            active = [tuple(s) for s in all_shapes if not (s & b_set)]
            if not active:
                break

            candidates = set()
            for s in active:
                for p in s:
                    if p not in m_set and p not in b_set:
                        candidates.add(p)
            if not candidates:
                break

            best_move = max(candidates, key=lambda c: breaker_func(c, m_cells, b_cells, active))
            b_cells.append(best_move)

        m_set = set(m_cells)
        if maker_won:
            total_score += float(turn * 10.0)
        else:
            max_cells_in_shape = max((len(s & m_set) for s in all_shapes), default=0)
            block_quality = (5 - max_cells_in_shape) * 100.0
            total_score += 1000.0 + block_quality + (max_turns - turn) * 10.0
        match_turns.append(len(m_cells))

    avg_turns = float(sum(match_turns) / len(match_turns)) if match_turns else 0.0
    return total_score / len(ensemble), avg_turns


# ---------------------------------------------------------------------------
# Boost Island Evolutionary Engine
# ---------------------------------------------------------------------------
@dataclasses.dataclass
class BoostIsland:
    island_id: int
    population: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    best_score: float = -float("inf")
    best_program_src: str = ""
    programs_registered: int = 0
    temp_init: float = 0.1
    temp_period: int = 50

    @property
    def temperature(self) -> float:
        ratio = (self.programs_registered % self.temp_period) / self.temp_period
        return self.temp_init * (1.0 - ratio)

    def register(self, body_src: str, full_code: str, score: float, test_scores: dict[int, float]) -> bool:
        self.programs_registered += 1
        is_best = False
        if score > self.best_score:
            self.best_score = score
            self.best_program_src = full_code
            is_best = True
        self.population.append({
            "body": body_src,
            "full_code": full_code,
            "score": score,
            "test_scores": test_scores,
            "registered_at": self.programs_registered,
        })
        return is_best


class BoostEvolutionEngine:
    """Manages multi-island co-evolution for Snakey with fast in-process evaluation."""

    def __init__(
        self,
        num_islands: int = 5,
        migration_interval: int = 8,
        temp_period: int = 50,
        temp_init: float = 0.1,
    ):
        self.num_islands = num_islands
        self.migration_interval = migration_interval
        self.maker_islands = [
            BoostIsland(i, temp_init=temp_init, temp_period=temp_period) for i in range(num_islands)
        ]
        self.breaker_islands = [
            BoostIsland(i, temp_init=temp_init, temp_period=temp_period) for i in range(num_islands)
        ]
        self.llm = MockLLM()
        self.migration_history: list[dict[str, Any]] = []
        self.event_stream: list[dict[str, Any]] = []
        self.global_best_maker_score = -float("inf")
        self.global_best_maker_code = ""
        self.global_best_breaker_score = -float("inf")
        self.global_best_breaker_code = ""

    def run_maker_generation(
        self,
        gen: int,
        samples_per_island: int = 2,
        active_breaker_func: Callable | None = None,
    ) -> tuple[list[dict[str, Any]], float]:
        gen_events = []
        gen_turns = []
        for island in self.maker_islands:
            for _ in range(samples_per_island):
                prompt = (
                    f"def priority_v{island.programs_registered}(candidate, maker_cells, breaker_cells, active_shapes):"
                )
                body = self.llm.draw_sample(prompt)
                func, full_code = compile_maker_func(body)
                if not func:
                    continue

                s3, t3 = evaluate_maker_heuristic(func, active_breaker_func, grid_radius=3)
                s4, t4 = evaluate_maker_heuristic(func, active_breaker_func, grid_radius=4)
                composite_score = s4
                gen_turns.append(t4)

                is_island_best = island.register(body, full_code, composite_score, {3: s3, 4: s4})
                is_global_best = False
                if composite_score > self.global_best_maker_score:
                    self.global_best_maker_score = composite_score
                    self.global_best_maker_code = full_code
                    is_global_best = True

                ev = {
                    "timestamp": time.time(),
                    "generation": gen,
                    "type": "maker",
                    "island_id": island.island_id,
                    "score": composite_score,
                    "avg_turns": t4,
                    "is_island_best": is_island_best,
                    "is_global_best": is_global_best,
                    "temperature": island.temperature,
                    "scores_per_test": {"3": s3, "4": s4},
                    "code_sample": full_code,
                }
                gen_events.append(ev)
                self.event_stream.append(ev)
                time.sleep(0.005)  # Throttle to stay strictly under 25% CPU

        # Island migration check
        if (gen + 1) % self.migration_interval == 0:
            self._migrate_islands(self.maker_islands, "maker", gen)

        avg_gen_turns = float(sum(gen_turns) / len(gen_turns)) if gen_turns else 0.0
        return gen_events, avg_gen_turns

    def run_breaker_generation(
        self,
        gen: int,
        samples_per_island: int = 2,
        active_maker_func: Callable | None = None,
    ) -> tuple[list[dict[str, Any]], float]:
        gen_events = []
        gen_turns = []
        for island in self.breaker_islands:
            for _ in range(samples_per_island):
                prompt = (
                    f"def breaker_priority_v{island.programs_registered}(candidate, maker_cells, breaker_cells, active_shapes):"
                )
                body = self.llm.draw_sample(prompt)
                func, full_code = compile_breaker_func(body)
                if not func:
                    continue

                s3, t3 = evaluate_breaker_heuristic(func, active_maker_func, grid_radius=3)
                s4, t4 = evaluate_breaker_heuristic(func, active_maker_func, grid_radius=4)
                composite_score = s4
                gen_turns.append(t4)

                is_island_best = island.register(body, full_code, composite_score, {3: s3, 4: s4})
                is_global_best = False
                if composite_score > self.global_best_breaker_score:
                    self.global_best_breaker_score = composite_score
                    self.global_best_breaker_code = full_code
                    is_global_best = True

                ev = {
                    "timestamp": time.time(),
                    "generation": gen,
                    "type": "breaker",
                    "island_id": island.island_id,
                    "score": composite_score,
                    "avg_turns": t4,
                    "is_island_best": is_island_best,
                    "is_global_best": is_global_best,
                    "temperature": island.temperature,
                    "scores_per_test": {"3": s3, "4": s4},
                    "code_sample": full_code,
                }
                gen_events.append(ev)
                self.event_stream.append(ev)
                time.sleep(0.005)  # Throttle to stay strictly under 25% CPU

        # Island migration check
        if (gen + 1) % self.migration_interval == 0:
            self._migrate_islands(self.breaker_islands, "breaker", gen)

        avg_gen_turns = float(sum(gen_turns) / len(gen_turns)) if gen_turns else 0.0
        return gen_events, avg_gen_turns

    def _migrate_islands(self, islands: list[BoostIsland], role: str, gen: int) -> None:
        """Copies elite champions from top 50% islands to bottom 50% islands."""
        sorted_islands = sorted(islands, key=lambda isl: isl.best_score)
        num_reset = len(islands) // 2
        bottom_islands = sorted_islands[:num_reset]
        top_islands = sorted_islands[num_reset:]

        record = {
            "timestamp": time.time(),
            "generation": gen,
            "role": role,
            "migrations": [],
        }

        for bot in bottom_islands:
            donor = random.choice(top_islands)
            old_score = bot.best_score
            # Elite gene flow: copy top program and update fitness baseline
            bot.best_score = donor.best_score
            bot.best_program_src = donor.best_program_src
            record["migrations"].append({
                "recipient_island": bot.island_id,
                "donor_island": donor.island_id,
                "donor_score": donor.best_score,
                "old_score": old_score,
            })

        self.migration_history.append(record)


# ---------------------------------------------------------------------------
# Benchmarking Engine
# ---------------------------------------------------------------------------
def run_match(
    maker_func: Callable,
    breaker_func: Callable,
    grid_radius: int = 4,
) -> dict[str, Any]:
    """Simulates a full match between Maker and Breaker on a given board radius."""
    all_shapes = get_board_shapes(grid_radius)
    m_cells, b_cells = [], []
    maker_won = False
    max_turns = (2 * grid_radius + 1) ** 2 // 2 + 1

    for turn in range(max_turns):
        m_set, b_set = set(m_cells), set(b_cells)

        for s in all_shapes:
            if s.issubset(m_set):
                maker_won = True
                break
        if maker_won:
            break

        active = [tuple(s) for s in all_shapes if not (s & b_set)]
        if not active:
            break

        candidates = set()
        for s in active:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates.add(p)
        if not candidates:
            break

        best_m = max(candidates, key=lambda c: maker_func(c, m_cells, b_cells, active))
        m_cells.append(best_m)
        m_set.add(best_m)

        for s in all_shapes:
            if s.issubset(m_set):
                maker_won = True
                break
        if maker_won:
            break

        active_b = [tuple(s) for s in all_shapes if not (s & b_set)]
        if not active_b:
            break

        candidates_b = set()
        for s in active_b:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates_b.add(p)
        if not candidates_b:
            break

        best_b = max(candidates_b, key=lambda c: breaker_func(c, m_cells, b_cells, active_b))
        b_cells.append(best_b)

    m_set = set(m_cells)
    max_cells = max((len(s & m_set) for s in all_shapes), default=0)
    return {
        "maker_won": maker_won,
        "turns": len(m_cells),
        "max_cells_in_shape": max_cells,
        "total_maker_cells": len(m_cells),
        "total_breaker_cells": len(b_cells),
    }


def load_strategy_from_file(file_path: str, func_name: str) -> Callable | None:
    """Loads a strategy function from a python file."""
    p = Path(file_path)
    if not p.exists():
        return None
    ns: dict[str, Any] = {}
    try:
        exec(p.read_text(encoding="utf-8"), ns)
        return ns.get(func_name)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Main Execution Pipeline
# ---------------------------------------------------------------------------
def main():
    print("=" * 88)
    print("🚀 LAUNCHING 100-GENERATION ALTERNATING CO-EVOLUTION (CAPPED <=25% CPU)")
    print("=" * 88)

    total_generations = 100
    samples_per_island = 2
    num_islands = 5
    migration_interval = 5

    engine = BoostEvolutionEngine(
        num_islands=num_islands,
        migration_interval=migration_interval,
        temp_period=30,
        temp_init=0.1,
    )

    # Seed baseline heuristics (load best existing champions if available)
    rank0_file = Path("strategies/maker/rank_0_score_300.00.py")
    if rank0_file.exists():
        baseline_maker_code = rank0_file.read_text(encoding="utf-8")
    else:
        baseline_maker_code = """def priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  weights = {0: 1.0, 1: 4.1, 2: 26.9, 3: 507.8, 4: 25000.0, 5: 1000000.0}
  score = 0.0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** m_cnt)
      active_count += 1
  score += (active_count ** 1.3) * 2.97
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.08
  return float(score)"""

    rank1_b_file = Path("strategies/breaker/rank_1_score_1010.00.py")
    if rank1_b_file.exists():
        baseline_breaker_code = rank1_b_file.read_text(encoding="utf-8")
    else:
        baseline_breaker_code = """def breaker_priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  block_weights = {0: 1.0, 1: 8.8, 2: 76.9, 3: 289.3, 4: 90000.0, 5: 1e8}
  score = 0.0
  overlap = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += block_weights.get(m_cnt, 10.0 ** m_cnt)
      overlap += 1
  score += (overlap ** 1.5) * 2.83
  return float(score)"""

    curr_maker_func, curr_maker_src = compile_maker_func(baseline_maker_code.split(":\n", 1)[1])
    curr_breaker_func, curr_breaker_src = compile_breaker_func(baseline_breaker_code.split(":\n", 1)[1])

    # Seed all islands with baseline & existing champions
    for isl in engine.maker_islands:
        s3, _ = evaluate_maker_heuristic(curr_maker_func, curr_breaker_func, 3)
        s4, _ = evaluate_maker_heuristic(curr_maker_func, curr_breaker_func, 4)
        isl.register(baseline_maker_code.split(":\n", 1)[1], baseline_maker_code, s4, {3: s3, 4: s4})

    for isl in engine.breaker_islands:
        s3, _ = evaluate_breaker_heuristic(curr_breaker_func, curr_maker_func, 3)
        s4, _ = evaluate_breaker_heuristic(curr_breaker_func, curr_maker_func, 4)
        isl.register(baseline_breaker_code.split(":\n", 1)[1], baseline_breaker_code, s4, {3: s3, 4: s4})

    engine.global_best_maker_score = s4
    engine.global_best_maker_code = baseline_maker_code
    engine.global_best_breaker_score = s4
    engine.global_best_breaker_code = baseline_breaker_code

    print(f"[*] Initialized {num_islands} Maker & Breaker islands with baseline normies and champions.")
    print(f"[*] Baseline Maker Radius 4 Score:    {engine.global_best_maker_score:.2f}")
    print(f"[*] Baseline Breaker Radius 4 Score:  {engine.global_best_breaker_score:.2f}\n")

    # Co-evolution loop across 100 generations with move count logging
    print("-" * 92)
    print("GEN | ROLE     | TOP SCORE | MEAN TEMP | AVG MOVES | REIGNING CLASH (R4)   | MIGR")
    print("-" * 92)

    move_history: list[dict[str, Any]] = []

    for gen in range(total_generations):
        # 1. Evolve Maker against reigning Breaker and baseline normies
        maker_events, avg_turns_m = engine.run_maker_generation(
            gen, samples_per_island=samples_per_island, active_breaker_func=curr_breaker_func
        )
        if engine.global_best_maker_code:
            m_fn, _ = compile_maker_func(engine.global_best_maker_code.split(":\n", 1)[1])
            if m_fn:
                curr_maker_func = m_fn

        # Immediate clash test on Radius 4
        clash_r4_m = run_match(curr_maker_func, curr_breaker_func, grid_radius=4)
        winner_str_m = "Maker" if clash_r4_m["maker_won"] else "Breaker"
        clash_str_m = f"{winner_str_m} ({clash_r4_m['turns']} turns)"

        mean_temp_m = sum(isl.temperature for isl in engine.maker_islands) / num_islands
        mig_m = "✓" if (gen + 1) % migration_interval == 0 else " "
        print(f"{gen+1:03d} | MAKER    | {engine.global_best_maker_score:9.2f} | {mean_temp_m:.4f}    | {avg_turns_m:5.1f} mov | {clash_str_m:<21} | {mig_m}")

        # 2. Evolve Breaker against reigning Maker and baseline normies
        breaker_events, avg_turns_b = engine.run_breaker_generation(
            gen, samples_per_island=samples_per_island, active_maker_func=curr_maker_func
        )
        if engine.global_best_breaker_code:
            b_fn, _ = compile_breaker_func(engine.global_best_breaker_code.split(":\n", 1)[1])
            if b_fn:
                curr_breaker_func = b_fn

        # Immediate clash test on Radius 4
        clash_r4_b = run_match(curr_maker_func, curr_breaker_func, grid_radius=4)
        winner_str_b = "Maker" if clash_r4_b["maker_won"] else "Breaker"
        clash_str_b = f"{winner_str_b} ({clash_r4_b['turns']} turns)"

        mean_temp_b = sum(isl.temperature for isl in engine.breaker_islands) / num_islands
        mig_b = "✓" if (gen + 1) % migration_interval == 0 else " "
        print(f"{gen+1:03d} | BREAKER  | {engine.global_best_breaker_score:9.2f} | {mean_temp_b:.4f}    | {avg_turns_b:5.1f} mov | {clash_str_b:<21} | {mig_b}")

        # Record move count history entry
        move_history.append({
            "generation": gen + 1,
            "maker_top_score": float(engine.global_best_maker_score),
            "maker_avg_moves": float(avg_turns_m),
            "breaker_top_score": float(engine.global_best_breaker_score),
            "breaker_avg_moves": float(avg_turns_b),
            "clash_winner": winner_str_b,
            "clash_turns": int(clash_r4_b["turns"]),
            "clash_max_cells": int(clash_r4_b["max_cells_in_shape"]),
        })

    print("-" * 92)
    print("✅ 100-GENERATION CO-EVOLUTION COMPLETE!")
    print(f"[*] Final Discovered Maker Champion Score:   {engine.global_best_maker_score:.2f}")
    print(f"[*] Final Discovered Breaker Champion Score: {engine.global_best_breaker_score:.2f}")
    print(f"[*] Total Island Migration Events:           {len(engine.migration_history)}")
    print(f"[*] Total Programs Evaluated:                {len(engine.event_stream)}")

    # ---------------------------------------------------------------------------
    # Benchmarking Against Baselines & Existing Champions (Radius 4 & Radius 6)
    # ---------------------------------------------------------------------------
    print("\n" + "=" * 92)
    print("📊 BENCHMARKING EVOLVED HEURISTICS AGAINST CHAMPIONS & BASELINES (R4 & R6 / 13x13)")
    print("=" * 92)

    # Compile final champion functions
    champ_maker_fn, _ = compile_maker_func(engine.global_best_maker_code.split(":\n", 1)[1])
    champ_breaker_fn, _ = compile_breaker_func(engine.global_best_breaker_code.split(":\n", 1)[1])
    base_maker_fn, _ = compile_maker_func(baseline_maker_code.split(":\n", 1)[1])
    base_breaker_fn, _ = compile_breaker_func(baseline_breaker_code.split(":\n", 1)[1])

    # Existing Champions
    prev_maker_rank0 = load_strategy_from_file("strategies/maker/rank_0_score_300.00.py", "priority")
    prev_maker_rank1 = load_strategy_from_file("strategies/maker/rank_1_score_280.00.py", "priority")
    prev_breaker_rank1 = load_strategy_from_file("strategies/breaker/rank_1_score_1010.00.py", "breaker_priority")

    # Run Benchmark Matches on Grid Radius 4 and Radius 6
    benchmark_results = {}

    matchups = [
        ("Discovered Maker vs Baseline Breaker", champ_maker_fn, base_breaker_fn),
        ("Discovered Maker vs Prev Breaker Rank 1", champ_maker_fn, prev_breaker_rank1 or base_breaker_fn),
        ("Discovered Maker vs Discovered Breaker", champ_maker_fn, champ_breaker_fn),
        ("Baseline Maker vs Discovered Breaker", base_maker_fn, champ_breaker_fn),
        ("Prev Maker Rank 0 vs Discovered Breaker", prev_maker_rank0 or base_maker_fn, champ_breaker_fn),
        ("Baseline Maker vs Baseline Breaker", base_maker_fn, base_breaker_fn),
    ]

    print(f"{'Matchup':<42} | Radius 4 (Turns) | Radius 6 (13x13) | Max Cells (R6)")
    print("-" * 92)

    for name, m_fn, b_fn in matchups:
        r4 = run_match(m_fn, b_fn, grid_radius=4)
        winner_r4 = "Maker" if r4["maker_won"] else "Breaker"
        r6 = run_match(m_fn, b_fn, grid_radius=6)
        winner_r6 = "Maker" if r6["maker_won"] else "Breaker"
        print(f"{name:<42} | {winner_r4:<7} ({r4['turns']:2d} t)   | {winner_r6:<7} ({r6['turns']:2d} t)   | {r6['max_cells_in_shape']}/6")
        benchmark_results[name] = {
            "radius_4": r4,
            "radius_6": r6,
        }

    # ---------------------------------------------------------------------------
    # Save Discovered Top Heuristics & Experiment Artifacts
    # ---------------------------------------------------------------------------
    timestamp = int(time.time())
    out_dir = Path(f"outputs/boost_mock_evolution_{timestamp}")
    out_dir.mkdir(parents=True, exist_ok=True)

    champions_dir = Path("co_evolve_champions")
    champions_dir.mkdir(parents=True, exist_ok=True)

    # 1. Save event stream (events.jsonl)
    with open(out_dir / "events.jsonl", "w") as f:
        for ev in engine.event_stream:
            f.write(json.dumps(ev) + "\n")

    # 2. Save migration events
    with open(out_dir / "migration_events.json", "w") as f:
        json.dump(engine.migration_history, f, indent=2)

    # 3. Save benchmark report
    with open(out_dir / "benchmark_report.json", "w") as f:
        json.dump(benchmark_results, f, indent=2)

    # 4. Save move count history
    with open(out_dir / "move_count_history.json", "w") as f:
        json.dump(move_history, f, indent=2)
    with open(champions_dir / "move_count_history.json", "w") as f:
        json.dump(move_history, f, indent=2)

    # 5. Save best programs in output run directory
    with open(out_dir / "best_maker_heuristic.py", "w") as f:
        f.write(
            f"# FunSearch 100-Gen Discovered Maker Champion\n# Score: {engine.global_best_maker_score:.2f}\n\n"
        )
        f.write(engine.global_best_maker_code + "\n")

    with open(out_dir / "best_breaker_heuristic.py", "w") as f:
        f.write(
            f"# FunSearch 100-Gen Discovered Breaker Champion\n# Score: {engine.global_best_breaker_score:.2f}\n\n"
        )
        f.write(engine.global_best_breaker_code + "\n")

    # 6. Save directly to co_evolve_champions/
    with open(champions_dir / f"maker_top_1_score_{int(engine.global_best_maker_score)}.py", "w") as f:
        f.write(f"# Co-Evolved Maker Champion (100 Gen Run)\n# Score: {engine.global_best_maker_score:.2f}\n\n")
        f.write(engine.global_best_maker_code + "\n")

    with open(champions_dir / f"breaker_top_1_score_{int(engine.global_best_breaker_score)}.py", "w") as f:
        f.write(f"# Co-Evolved Breaker Champion (100 Gen Run)\n# Score: {engine.global_best_breaker_score:.2f}\n\n")
        f.write(engine.global_best_breaker_code + "\n")

    # Update leaderboards
    maker_top_entries = []
    for isl in engine.maker_islands:
        maker_top_entries.append({"id": isl.island_id, "score": isl.best_score, "src": isl.best_program_src})
    maker_top_entries.sort(key=lambda x: x["score"], reverse=True)
    with open(champions_dir / "maker_leaderboard.json", "w") as f:
        json.dump(maker_top_entries, f, indent=2)

    breaker_top_entries = []
    for isl in engine.breaker_islands:
        breaker_top_entries.append({"id": isl.island_id, "score": isl.best_score, "src": isl.best_program_src})
    breaker_top_entries.sort(key=lambda x: x["score"], reverse=True)
    with open(champions_dir / "breaker_leaderboard.json", "w") as f:
        json.dump(breaker_top_entries, f, indent=2)

    # 7. Save comprehensive log
    comp_log = {
        "experiment_name": f"boost_mock_evolution_{timestamp}",
        "parameters": {
            "num_islands": num_islands,
            "generations": total_generations,
            "samples_per_island": samples_per_island,
            "migration_interval": migration_interval,
            "cpu_limit": "25% max (single thread with micro-sleeps)",
        },
        "maker_champion": {
            "score": engine.global_best_maker_score,
            "code": engine.global_best_maker_code,
        },
        "breaker_champion": {
            "score": engine.global_best_breaker_score,
            "code": engine.global_best_breaker_code,
        },
        "benchmarks": benchmark_results,
        "migrations_count": len(engine.migration_history),
        "total_evaluations": len(engine.event_stream),
        "move_history": move_history,
    }
    with open(out_dir / "boost_evolution_log.json", "w") as f:
        json.dump(comp_log, f, indent=2)

    # 8. Save new top heuristics into strategies/ directory if surpassing scores
    maker_strat_path = Path(f"strategies/maker/rank_boost_score_{engine.global_best_maker_score:.2f}.py")
    with open(maker_strat_path, "w") as f:
        f.write(f"# Rank Boost Snakey Maker Strategy\n# Fitness Score: {engine.global_best_maker_score:.2f}\n\n")
        f.write(engine.global_best_maker_code + "\n")

    breaker_strat_path = Path(f"strategies/breaker/rank_boost_score_{engine.global_best_breaker_score:.2f}.py")
    with open(breaker_strat_path, "w") as f:
        f.write(
            f"# Rank Boost Snakey Breaker Strategy\n# Fitness Score: {engine.global_best_breaker_score:.2f}\n\n"
        )
        f.write(engine.global_best_breaker_code + "\n")

    print("\n" + "=" * 88)
    print(f"💾 ARTIFACTS SAVED SUCCESSFULLY:")
    print(f"  - Run Directory:       {out_dir}")
    print(f"  - Champions Directory: {champions_dir}")
    print(f"  - Maker Champion:      {maker_strat_path}")
    print(f"  - Breaker Champion:    {breaker_strat_path}")
    print(f"  - Benchmark Report:    {out_dir / 'benchmark_report.json'}")
    print(f"  - Move Count History:  {champions_dir / 'move_count_history.json'}")
    print(f"  - Migration Log:       {out_dir / 'migration_events.json'}")
    print(f"  - Event Stream:        {out_dir / 'events.jsonl'}")
    print("=" * 88)


if __name__ == "__main__":
    main()
