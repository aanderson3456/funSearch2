def priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  threat_4 = 0
  threat_3 = 0
  active_count = 0
  weights = {0: 1.0, 1: 6.3, 2: 34.5, 3: 1510.3, 4: 66977.3, 5: 10000000.0}
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
    score += 17728396.7 * (threat_4 ** 2)
  if threat_3 >= 2:
    score += 55464.4 * (threat_3 ** 1.5)
  # Parity modulation: align with 2x2 grid blocks
  is_parity = ((candidate[0] // 3) + (candidate[1] // 3)) % 2 == 0
  if is_parity:
    score += 7478.8
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * 0.0755
  score += (active_count ** 1.4) * 2.8
  return float(score)