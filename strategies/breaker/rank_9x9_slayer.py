def breaker_priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  m_threat_4 = 0
  m_threat_3 = 0
  overlap = 0
  weights = {0: 1.0, 1: 6.0, 2: 56.2, 3: 1595.3, 4: 53636.5, 5: 10000000.0}
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
    score += 18720339.4 * (m_threat_4 ** 2)
  if m_threat_3 >= 2:
    score += 133591.6 * (m_threat_3 ** 1.5)
  # Smothering proximity to Maker's latest stone
  if maker_cells:
    last_m = maker_cells[-1]
    dx = abs(candidate[0] - last_m[0])
    dy = abs(candidate[1] - last_m[1])
    d_cheb = max(dx, dy)
    if d_cheb <= 1:
      score += 1536.2
    elif d_cheb == 2:
      score += 2178.1
  score += (overlap ** 1.4) * 3.95
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * 0.0390
  return float(score)