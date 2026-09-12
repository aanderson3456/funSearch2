def breaker_priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  # Absolute 5-threat override: must strictly dominate any combination of lower threats
  for s in active_shapes:
    if candidate in s and sum(1 for p in s if p in m_set) == 5:
      return 1e14
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
  # Exponential multi-fork choke
  if m_threat_4 >= 2:
    score += 38881787.5 * (m_threat_4 ** 2.00)
  elif m_threat_4 == 1:
    score += 424595.5
  if m_threat_3 >= 2:
    score += 337028.8 * (m_threat_3 ** 1.5)
  # Smothering gradient: suppress freedom of movement around all maker stones
  if maker_cells:
    min_dist = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
    if min_dist <= 1:
      score += 8515.9
    elif min_dist == 2:
      score += 3107.8
  # Parity suppression: contest Maker's parity preference
  if ((candidate[0] // 2) + (candidate[1] // 2)) % 2 == 0:
    score += 3952.9
  score += (overlap ** 1.46) * 3.91
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * 0.0266
  return float(score)