"""Topological Snaky Maker Strategy (Bipartite Homology & Winding Curvature)"""
from typing import List, Tuple

def score_candidate_maker(candidate: Tuple[int, int], maker_cells: List[Tuple[int, int]], breaker_cells: List[Tuple[int, int]], active_shapes: List[List[Tuple[int, int]]]) -> float:
  m_set = set(maker_cells)
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
        score += 61048.3
      elif m_cnt == 3:
        t3_count += 1
        score += 2955.5
      else:
        score += float(10.8 ** m_cnt)
  # Topological Winding: reward orthogonal elbow connectivity to prevent collinear blocking
  has_horizontal_neighbor = (candidate[0] + 1, candidate[1]) in m_set or (candidate[0] - 1, candidate[1]) in m_set
  has_vertical_neighbor = (candidate[0], candidate[1] + 1) in m_set or (candidate[0], candidate[1] - 1) in m_set
  if has_horizontal_neighbor and has_vertical_neighbor:
    score += 19534.9  # Snaky elbow vertex
  elif has_horizontal_neighbor or has_vertical_neighbor:
    score += 5781.0  # Snaky 4-stem extension
  if t4_count >= 2:
    score += 42745381.8 * (t4_count ** 2)
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * 0.0286
  score += (active_count ** 1.3) * 6.9
  return float(score)
