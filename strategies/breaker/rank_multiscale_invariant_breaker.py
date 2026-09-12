"""Multi-Scale Translation-Invariant Breaker Strategy (Scale-Free Topology)"""
from typing import List, Tuple

def breaker_priority(candidate: Tuple[int, int], maker_cells: List[Tuple[int, int]], breaker_cells: List[Tuple[int, int]], active_shapes: List[List[Tuple[int, int]]]) -> float:
  m_set = set(maker_cells)
  # 1. Absolute 5-threat hard override
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e16

  score = 0.0
  m_threat_4 = 0
  m_threat_3 = 0
  overlap = 0
  weights = {0: 1.0, 1: 3.7, 2: 43.6, 3: 1726.3, 4: 99921.1}
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
    score += 59000172.3 * (m_threat_4 ** 2.0)
  elif m_threat_4 == 1:
    score += 619470.5

  # 3. Controlled 3-threat choke
  if m_threat_3 >= 2:
    score += 330405.3 * (m_threat_3 ** 1.5)

  # 4. Scale-Free 2x2 Box-Corner Choke (Subordinate to 4-threats)
  if m_threat_4 == 0:
    for dx in [-1, 1]:
      for dy in [-1, 1]:
        if ((candidate[0] + dx, candidate[1]) in m_set and 
            (candidate[0], candidate[1] + dy) in m_set and 
            (candidate[0] + dx, candidate[1] + dy) in m_set):
          score += 1093831.1
          break

  # 5. Scale-Free Collinear Stem Choke (stops 3-in-a-row straight runners)
  if ((candidate[0] - 1, candidate[1]) in m_set and (candidate[0] - 2, candidate[1]) in m_set) or \
     ((candidate[0] + 1, candidate[1]) in m_set and (candidate[0] + 2, candidate[1]) in m_set) or \
     ((candidate[0], candidate[1] - 1) in m_set and (candidate[0], candidate[1] - 2) in m_set) or \
     ((candidate[0], candidate[1] + 1) in m_set and (candidate[0], candidate[1] + 2) in m_set):
    score += 77343.7

  # 6. Relative Pairwise Smothering Kernel (translation-invariant relative distance)
  if maker_cells:
    min_dist = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    if min_dist <= 1:
      score += 10577.3
    elif min_dist == 2:
      score += 2676.7
    elif min_dist >= 5:
      score -= 7705.1

  score += (overlap ** 1.39) * 5.5
  return float(score)
