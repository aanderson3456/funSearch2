"""Snakey Breaker Evolution Game specification for FunSearch.

Maker uses the hardcoded elite 280-point strategy. 
Breaker is evolved by FunSearch to defeat Maker.
"""
from __future__ import annotations

SPECIFICATION = '''"""Snakey Breaker Evolution Game problem specification."""
import itertools
import numpy as np

# Base coordinates of Snakey Hexomino (4-in-a-row bar + 2-cell step head)
_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]

def _get_board_shapes(radius: int = 4):
  """Generates all translational instances of Snaky in D8 within [-radius, radius]^2."""
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
def breaker_priority(
    candidate: tuple[int, int],
    maker_cells: list[tuple[int, int]],
    breaker_cells: list[tuple[int, int]],
    active_shapes: list[tuple[tuple[int, int], ...]],
) -> float:
  """Returns priority for Breaker choosing `candidate` cell.
  
  Higher score means Breaker prefers this cell to block Maker.
  """
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0

  for shape in active_shapes:
    if candidate in shape:
      # Block shapes where Maker is close to winning
      m_count = sum(1 for p in shape if p in m_set)
      score += float(10 ** m_count)
      
  return score


@funsearch.run
def evaluate(grid_radius: int) -> float:
  """Simulates Breaker playing with `breaker_priority` against the Elite Maker."""
  all_shapes = _get_board_shapes(radius=grid_radius)
  
  total_score = 0.0
  
  # --- The Elite 280-point Maker (Sample 7) ---
  def elite_maker(m_cells, b_cells, active):
    m_set, b_set = set(m_cells), set(b_cells)
    candidates = set()
    for s in active:
      for p in s:
        if p not in m_set and p not in b_set:
          candidates.add(p)
          
    if not candidates:
        return (999, 999)
        
    best_move = None
    best_score = -float('inf')
    
    weight_map = {0: 1.0, 1: 5.0, 2: 35.0, 3: 350.0, 4: 50000.0, 5: 100000000.0}
    
    for cand in candidates:
      score = 0.0
      active_count = 0
      for shape in active:
        if cand in shape:
          if any(p in b_set for p in shape):
            continue
          m_count = sum(1 for p in shape if p in m_set)
          score += weight_map.get(m_count, 10.0 ** m_count)
          active_count += 1
          
      score += (active_count ** 1.5) * 2.0
      score -= (cand[0] ** 2 + cand[1] ** 2) * 0.01
      
      if score > best_score:
        best_score = score
        best_move = cand
        
    return best_move

  # Run simulations against the Elite Maker
  m_cells, b_cells = [], []
  maker_won = False
  
  for turn in range(25):  # Max plies
    m_set = set(m_cells)
    b_set = set(b_cells)
    
    # Check if Maker already won
    for s in all_shapes:
      if s.issubset(m_set):
        maker_won = True
        break
    if maker_won:
      break
      
    # Active shapes not blocked by Breaker
    active = [tuple(s) for s in all_shapes if not (s & b_set)]
    if not active:
      break
      
    # Maker moves first
    m_move = elite_maker(m_cells, b_cells, active)
    if m_move == (999, 999):
      break
    m_cells.append(m_move)
    m_set.add(m_move)
    
    # Did Maker win on this move?
    for s in all_shapes:
      if s.issubset(m_set):
        maker_won = True
        break
    if maker_won:
      break
      
    # Breaker candidate moves
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
      
    # Breaker chooses move with highest priority
    best_move = max(
        candidates,
        key=lambda c: breaker_priority(c, m_cells, b_cells, active)
    )
    b_cells.append(best_move)
      
  m_set = set(m_cells)
  
  if maker_won:
    # Breaker failed to stop Maker. Score based on how many turns it delayed Maker.
    # Turn starts at 0, max is 25. If maker wins early, Breaker gets low score.
    # E.g., if maker wins on turn 13, Breaker gets 13 * 10 = 130.
    total_score += float(turn * 10.0)
  else:
    # Breaker completely blocked Maker! Massive win bonus.
    # Plus bonus based on how few cells Maker managed to get in its best shape.
    max_cells_in_shape = max((len(s & m_set) for s in all_shapes), default=0)
    # The fewer cells Maker got, the better the block!
    # Max cells Maker can have without winning is 5.
    block_quality = (5 - max_cells_in_shape) * 100.0
    total_score += 1000.0 + block_quality + (25 - turn) * 10.0

  return total_score
'''

INPUTS = [3, 4]
