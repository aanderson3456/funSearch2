"""Snakey (Step Snaky Hexomino) Polyomino Achievement Game specification for FunSearch.

Formalized from Numberphile & Sophie MacLean (Frank Harary 1982 Polyomino Achievement Game).
Maker plays to construct any D8 isometric copy of the Snakey Hexomino:
  [(0,0), (1,0), (2,0), (3,0), (3,1), (4,1)]
against adversarial Breaker responses.
"""
from __future__ import annotations

SPECIFICATION = '''"""Snakey Achievement Game problem specification."""
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
def priority(
    candidate: tuple[int, int],
    maker_cells: list[tuple[int, int]],
    breaker_cells: list[tuple[int, int]],
    active_shapes: list[tuple[tuple[int, int], ...]],
) -> float:
  """Returns priority for Maker choosing `candidate` cell.
  
  Higher score means Maker prefers this cell.
  """
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0

  for shape in active_shapes:
    if candidate in shape:
      # Count how many cells Maker already owns in this shape
      m_count = sum(1 for p in shape if p in m_set)
      # Exponential weighting for advancing close-to-completion shapes
      score += float(10 ** m_count)
      
  # Center proximity bias (prefer compact central development)
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.1
  return score


@funsearch.run
def evaluate(grid_radius: int) -> float:
  """Simulates Maker playing with `priority` against a battery of adversarial Breakers."""
  all_shapes = _get_board_shapes(radius=grid_radius)
  
  total_score = 0.0
  
  # --- Test 1: Play against Anti-Decoy Evolving Breaker ---
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
        
    best_move = None
    best_score = -float('inf')
    
    for cand in candidates:
        score = 0.0
        high_threat_shapes = 0
        for shape in active:
            if cand in shape:
                m_count = sum(1 for p in shape if p in m_set)
                if m_count == len(shape) - 1:
                    return cand  # Must block 1-threats instantly
                if m_count >= 3:
                    high_threat_shapes += 1
                score += float(10 ** m_count)
        
        # Anti-Decoy Fork Destruction
        if high_threat_shapes > 1:
            score += 50000.0
            
        center_bonus = 10.0 - (abs(cand[0]) + abs(cand[1]))
        score += center_bonus
        
        if score > best_score:
            best_score = score
            best_move = cand
            
    return best_move

  # Run simulations against the Evolving Breaker
  for breaker_fn in [evolving_breaker]:
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
        
      # Candidate moves for Maker
      candidates = set()
      for s in active:
        for p in s:
          if p not in m_set and p not in b_set:
            candidates.add(p)
      if not candidates:
        break
        
      # Maker chooses move with highest priority
      best_move = max(
          candidates,
          key=lambda c: priority(c, m_cells, b_cells, active)
      )
      m_cells.append(best_move)
      
      # Breaker responds
      b_move = breaker_fn(best_move, m_cells, b_cells)
      if b_move != (999, 999):
        b_cells.append(b_move)
        
    m_set = set(m_cells)
    # Score based on how close Maker got to forming Snaky
    max_cells_in_shape = max((len(s & m_set) for s in all_shapes), default=0)
    total_score += float(max_cells_in_shape * 10)
    if maker_won:
      # Win bonus inversely proportional to turns taken
      total_score += 100.0 + (25 - turn) * 10.0

  return total_score
'''

INPUTS = [3, 4]
