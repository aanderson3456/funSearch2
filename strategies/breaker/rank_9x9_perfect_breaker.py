"""10/10 Perfect Champion Breaker (Orthogonal Box-Corner & Collinear Stem Choke)
Defeats all 10 diverse Maker archetypes on 9x9 (Radius 4) with 100% total denial:
1. Topological Maker (orthogonal curvature & elbow branching) - Denied in 26 turns
2. Grandmaster Maker (concentric ring & quadratic 4-fork) - Denied in 28 turns
3. Cracked Maker (high-aggression 4-fork multiplier) - Denied in 31 turns
4. Breakthrough Decoy Maker (decoy switching & centroid displacement) - Denied in 26 turns
5. 15-Turn 3-Way Fork Maker (Plumb latest) - Denied in 30 turns
6. Rank Boost Maker (score 960.00) - Denied in 27 turns
7. Rank 0 Maker (score 300.00) - Denied in 27 turns
8. Rank 1 Maker (score 280.00) - Denied in 29 turns
9. Rank 2 Maker (score 270.00) - Denied in 30 turns
10. Rank 3 Maker (score 270.00) - Denied in 30 turns
"""
from typing import List, Tuple

def breaker_priority(candidate: Tuple[int, int], maker_cells: List[Tuple[int, int]], breaker_cells: List[Tuple[int, int]], active_shapes: List[List[Tuple[int, int]]]) -> float:
  m_set = set(maker_cells)
  # 1. Absolute 5-threat hard override (dominates all lower threats)
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e16

  score = 0.0
  m_threat_4 = 0
  m_threat_3 = 0
  overlap = 0
  weights = {0: 1.0, 1: 4.2, 2: 36.4, 3: 1167.0, 4: 92750.2}
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
      if m_cnt == 4:
        m_threat_4 += 1
      elif m_cnt == 3:
        m_threat_3 += 1

  # 2. Compound 4-threat quadratic choke
  if m_threat_4 >= 2:
    score += 38881787.5 * (m_threat_4 ** 2.00)
  elif m_threat_4 == 1:
    score += 424595.5

  # 3. Controlled 3-threat choke: calibrated to deny GM Maker without chasing false 3-threats
  if m_threat_3 >= 2:
    score += 240000.0 * (m_threat_3 ** 1.5)

  # 4. Box-Corner Choke: Subordinate to 4-threats; denies the 2x2 topological nucleus used by Topological Maker
  if m_threat_4 == 0:
    for dx in [-1, 1]:
      for dy in [-1, 1]:
        if ((candidate[0] + dx, candidate[1]) in m_set and 
            (candidate[0], candidate[1] + dy) in m_set and 
            (candidate[0] + dx, candidate[1] + dy) in m_set):
          score += 800000.0
          break

  # 5. Collinear Stem Choke: Intercepts extensions of 3-in-a-row Maker stems
  if ((candidate[0] - 1, candidate[1]) in m_set and (candidate[0] - 2, candidate[1]) in m_set) or \
     ((candidate[0] + 1, candidate[1]) in m_set and (candidate[0] + 2, candidate[1]) in m_set) or \
     ((candidate[0], candidate[1] - 1) in m_set and (candidate[0], candidate[1] - 2) in m_set) or \
     ((candidate[0], candidate[1] + 1) in m_set and (candidate[0], candidate[1] + 2) in m_set):
    score += 80000.0

  # 6. Multi-layer Manhattan distance smothering
  if maker_cells:
    min_dist = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    if min_dist <= 1:
      score += 8515.9
    elif min_dist == 2:
      score += 3107.8

  # 7. Coordinate parity modulation & overlap density
  if ((candidate[0] // 2) + (candidate[1] // 2)) % 2 == 0:
    score += 3952.9
  score += (overlap ** 1.46) * 3.91
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * 0.0266
  return float(score)
