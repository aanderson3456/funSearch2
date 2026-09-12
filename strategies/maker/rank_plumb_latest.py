def priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  t4_count = 0
  t3_count = 0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      active_count += 1
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == 4:
        t4_count += 1
        score += 65000.0
      elif m_cnt == 3:
        t3_count += 1
        score += 962.0
      else:
        score += float(9.3 ** m_cnt)
  # 3-Way compound threat bonus: Breaker can block at most 1, leaving >= 2 open!
  if t4_count >= 3:
    score += 8620662.7
  elif t4_count == 2:
    score += 3350866.7
  if t3_count >= 3:
    score += 95501.0
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * 0.007473
  score += (active_count ** 1.59) * 9.6
  return float(score)