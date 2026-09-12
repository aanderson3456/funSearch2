def breaker_priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  m_threat_4 = 0
  m_threat_3 = 0
  overlap = 0
  weights = {0: 1.0, 1: 6.3, 2: 36.6, 3: 1999.0, 4: 112940.2, 5: 10000000.0}
  for shape in active_shapes:
    if candidate in shape:
      overlap += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
      if m_cnt == 4:
        m_threat_4 += 1
      elif m_cnt == 3:
        m_threat_3 += 1
  if m_threat_4 >= 2:
    score += 20883429.3 * (m_threat_4 ** 2)
  if m_threat_3 >= 2:
    score += 115441.8 * (m_threat_3 ** 1.5)
  # Global tracking: bonus for smothering ANY maker stone with >= 3 shape overlaps
  if maker_cells:
    min_dist_to_maker = min((abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells), default=99)
    if min_dist_to_maker <= 1:
      score += 4144.4
    elif min_dist_to_maker == 2:
      score += 1909.5
  score += (overlap ** 1.4) * 3.68
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * 0.0337
  return float(score)