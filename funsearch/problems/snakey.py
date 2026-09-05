"""Specification."""
from __future__ import annotations

SPECIFICATION = '''"""Snakey Achievement Game problem specification."""
import itertools
import numpy as np

_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]

def _get_board_shapes(radius: int = 4):
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
  return list(set(shapes))

@funsearch.evolve
def priority(
    candidate: tuple[int, int],
    maker_cells: list[tuple[int, int]],
    breaker_cells: list[tuple[int, int]],
    active_shapes: list[tuple[tuple[int, int], ...]],
) -> float:
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
  return float(score)

@funsearch.run
def evaluate(grid_radius: int) -> float:
  all_shapes = _get_board_shapes(radius=grid_radius)
  
  total_score = 0.0
  
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
        
    def breaker_priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
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
      return float(score)

    return max(candidates, key=lambda c: breaker_priority(c, m_cells, b_cells, active))
    
  def checkerboard_breaker(last_maker_move, m_cells, b_cells):
    m_set, b_set = set(m_cells), set(b_cells)
    active = [s for s in all_shapes if not (s & b_set)]
    candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
    if not candidates: return (999, 999)
    def is_cb(p): return ((p[0] // 2) + (p[1] // 2)) % 2 == 0
    cb_cands = [c for c in candidates if is_cb(c)]
    if cb_cands:
      return max(cb_cands, key=lambda c: sum(1 for s in active if c in s))
    return max(candidates, key=lambda c: sum(1 for s in active if c in s))
    
  def one_look_ahead_breaker(last_maker_move, m_cells, b_cells):
    m_set, b_set = set(m_cells), set(b_cells)
    active = [s for s in all_shapes if not (s & b_set)]
    candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
    if not candidates: return (999, 999)
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
    if not candidates: return (999, 999)
    def is_ht(p): return ((p[0] // 3) + (p[1] // 3)) % 2 == 0
    ht_cands = [c for c in candidates if is_ht(c)]
    if ht_cands:
      return max(ht_cands, key=lambda c: sum(1 for s in active if c in s))
    return max(candidates, key=lambda c: sum(1 for s in active if c in s))

  ensemble = [evolving_breaker, checkerboard_breaker, one_look_ahead_breaker, higher_topo_paving_breaker]
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
        
      best_move = max(candidates, key=lambda c: priority(c, m_cells, b_cells, active))
      m_cells.append(best_move)
      
      b_move = breaker_fn(best_move, m_cells, b_cells)
      if b_move != (999, 999):
        b_cells.append(b_move)
        
    m_set = set(m_cells)
    max_cells_in_shape = max((len(s & m_set) for s in all_shapes), default=0)
    total_score += float(max_cells_in_shape * 10)
    if maker_won:
      total_score += 100.0 + (max_turns - turn) * 10.0

  return total_score / len(ensemble)
'''
INPUTS = [3, 4]
