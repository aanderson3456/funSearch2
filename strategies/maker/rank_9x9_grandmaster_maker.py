def priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e14
  score = 0.0
  threat_4 = 0
  threat_3 = 0
  overlap = 0
  weights = {0: 1.0, 1: 5.3, 2: 44.8, 3: 1848.3, 4: 105124.1}
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
      if m_cnt == 4: threat_4 += 1
      elif m_cnt == 3: threat_3 += 1
  if threat_4 >= 2: score += 34598560.2 * (threat_4 ** 2)
  if threat_3 >= 2: score += 66226.7 * (threat_3 ** 1.5)
  # Ring distance bonus: develop threats in concentric ring
  r_sq = candidate[0] ** 2 + candidate[1] ** 2
  if 3.4 <= r_sq <= 8.4:
    score += 8879.8
  score += (overlap ** 1.29) * 2.67
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * 0.0633
  return float(score)