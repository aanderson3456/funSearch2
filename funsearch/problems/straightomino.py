"""5-Straightomino (I5) Polyomino Achievement Game specification for FunSearch.

Formalized in Lean 4 (Frank Harary 1982 Polyomino Achievement Game).
Maker plays to construct any isometric copy of the 5-Straightomino:
  [(0,0), (1,0), (2,0), (3,0), (4,0)]
against adversarial Breaker responses.
"""
from __future__ import annotations

SPECIFICATION = '''"""5-Straightomino (I5) Achievement Game problem specification."""
import itertools
import numpy as np

# Base coordinates of 5-Straightomino (I5)
_BASE_I5 = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]


def _get_board_shapes(radius: int = 4):
  """Generates all translational and rotational instances of I5 in D8 within [-radius, radius]^2."""
  orientations = [
      [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],  # Horizontal
      [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],  # Vertical
  ]

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

  # --- Breaker 1: Harary's 1x2 Domino Paving Involution Breaker ---
  def paving_breaker(last_maker_move, m_cells, b_cells):
    x, y = last_maker_move
    partner = (x + 1, y) if x % 2 == 0 else (x - 1, y)
    if partner not in set(m_cells) and partner not in set(b_cells):
      return partner
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      cand = (x + dx, y + dy)
      if cand not in set(m_cells) and cand not in set(b_cells) and abs(cand[0]) <= grid_radius and abs(cand[1]) <= grid_radius:
        return cand
    return (999, 999)

  # --- Breaker 2: Greedy Threat Blocker ---
  def greedy_threat_breaker(last_maker_move, m_cells, b_cells):
    m_set, b_set = set(m_cells), set(b_cells)
    active = [s for s in all_shapes if not (s & b_set)]

    # Priority 1: Block immediate 1-threats
    threat_1_cells = []
    for s in active:
      diff = s - m_set
      if len(diff) == 1:
        threat_1_cells.append(list(diff)[0])
    if threat_1_cells:
      return threat_1_cells[0]

    # Priority 2: Maximize intersection with active Maker threats
    block_scores = {}
    for s in active:
      m_cnt = len(s & m_set)
      for p in s - m_set:
        block_scores[p] = block_scores.get(p, 0) + (5 ** m_cnt)
    if block_scores:
      return max(block_scores.keys(), key=lambda p: block_scores[p])
    return (999, 999)

  # Run simulations against both Breakers
  for breaker_fn in [paving_breaker, greedy_threat_breaker]:
    m_cells, b_cells = [], []
    maker_won = False

    for turn in range(10):  # Max plies
      m_set = set(m_cells)
      b_set = set(b_cells)

      # Check if Maker already won
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

      best_move = max(
          candidates,
          key=lambda c: priority(c, m_cells, b_cells, active)
      )
      m_cells.append(best_move)

      b_move = breaker_fn(best_move, m_cells, b_cells)
      if b_move != (999, 999):
        b_cells.append(b_move)

    m_set = set(m_cells)
    max_cells = max((len(s & m_set) for s in all_shapes), default=0)
    total_score += float(max_cells * 10)
    if max_cells == 5:
      total_score += 100.0 + (10 - turn) * 10.0

  return total_score
'''

INPUTS = [3, 4]
