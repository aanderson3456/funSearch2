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

def breaker_priority(
    candidate: tuple[int, int],
    maker_cells: list[tuple[int, int]],
    breaker_cells: list[tuple[int, int]],
    active_shapes: list[frozenset[tuple[int, int]]],
) -> float:
  m_set = set(maker_cells)
  score = 0.0
  
  high_threat_shapes_blocked = 0
  
  for shape in active_shapes:
    if candidate in shape:
      m_count = sum(1 for p in shape if p in m_set)
      if m_count == len(shape) - 1:
          return 1000000.0
          
      if m_count >= 3:
          high_threat_shapes_blocked += 1
          
      score += float(10 ** m_count)
      
  # Anti-Decoy Mutation: Explicitly hunt and destroy Maker's fork attempts
  # before they become inescapable.
  if high_threat_shapes_blocked > 1:
      score += 50000.0
          
  center_bonus = 10.0 - (abs(candidate[0]) + abs(candidate[1]))
  score += center_bonus
  return score

def maker_heuristic(candidate: tuple[int, int], m_cells: list, b_cells: list, active: list) -> float:
  m_set = set(m_cells)
  my_score = 0.0
  threat_1_created = False
  other_shape_advancements = 0
  for shape in active:
    if candidate in shape:
      m_count = sum(1 for p in shape if p in m_set)
      if m_count == len(shape) - 2:
          threat_1_created = True
      elif m_count >= 2:
          other_shape_advancements += 1
      my_score += float(10 ** m_count)
  if threat_1_created and other_shape_advancements > 0:
      my_score += 100000.0
  return my_score - (abs(candidate[0]) + abs(candidate[1])) * 0.1

def maker_priority(
    candidate: tuple[int, int],
    maker_cells: list[tuple[int, int]],
    breaker_cells: list[tuple[int, int]],
    active_shapes: list[frozenset[tuple[int, int]]],
) -> float:
  # 1-Step Lookahead (Minimax)
  m_cells_next = maker_cells + [candidate]
  m_set_next = set(m_cells_next)
  b_set = set(breaker_cells)
  
  # Check if Maker just won
  for shape in active_shapes:
      if shape.issubset(m_set_next):
          return float('inf')
          
  active_for_breaker = [s for s in active_shapes if not (s & b_set)]
  b_candidates = set()
  for s in active_for_breaker:
      for p in s:
          if p not in m_set_next and p not in b_set:
              b_candidates.add(p)
              
  if not b_candidates:
      return maker_heuristic(candidate, maker_cells, breaker_cells, active_shapes)
      
  # Assume Breaker plays its best heuristic move
  best_b_move = max(b_candidates, key=lambda c: breaker_priority(c, m_cells_next, breaker_cells, active_for_breaker))
  
  # Evaluate Maker's position AFTER Breaker's response
  b_cells_next = breaker_cells + [best_b_move]
  b_set_next = set(b_cells_next)
  active_next = [s for s in active_shapes if not (s & b_set_next)]
  
  if not active_next:
      return -float('inf')
      
  # Maker's resulting board value
  board_value = 0.0
  for s in active_next:
      m_count = sum(1 for p in s if p in m_set_next)
      board_value += float(10 ** m_count)
      
  return board_value
