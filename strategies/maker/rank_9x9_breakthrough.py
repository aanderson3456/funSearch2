def priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  threat_4 = 0
  threat_3 = 0
  active_count = 0
  weights = {0: 1.0, 1: 6.7, 2: 35.8, 3: 806.8, 4: 31757.2, 5: 10000000.0}
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
      if m_cnt == 4:
        threat_4 += 1
      elif m_cnt == 3:
        threat_3 += 1
  if threat_4 >= 2:
    score += 8006334.3 * (threat_4 ** 2)
  if threat_3 >= 2:
    score += 182923.5 * (threat_3 ** 1.5)
  # Anti-smothering: penalize being trapped by adjacent Breaker stones
  adj_b = sum(1 for b in breaker_cells if abs(candidate[0] - b[0]) <= 1 and abs(candidate[1] - b[1]) <= 1)
  score -= adj_b * 2162.6
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * 0.0534
  score += (active_count ** 1.4) * 5.9
  return float(score)