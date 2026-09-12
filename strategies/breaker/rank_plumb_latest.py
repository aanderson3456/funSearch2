def breaker_priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  m_threat_4 = 0
  m_threat_3 = 0
  overlap = 0
  weights = {0: 1.0, 1: 5.4, 2: 53.4, 3: 1181.6, 4: 72105.1, 5: 10000000.0}
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
      if m_cnt == 4:
        m_threat_4 += 1
      elif m_cnt == 3:
        m_threat_3 += 1
  # Heavily intercept multi-fork convergence points:
  if m_threat_4 >= 2:
    score += 6841965.9 * (m_threat_4 ** 2)
  if m_threat_3 >= 2:
    score += 165844.7 * (m_threat_3 ** 1.5)
  score += (overlap ** 1.4) * 6.27
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * 0.0356
  return float(score)