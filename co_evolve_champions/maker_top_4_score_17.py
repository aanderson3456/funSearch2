# Maker ID: 7
# Longevity Score: 17
# Gens Survived: 1
# Mutations Defeated: 17

def priority(candidate, maker_cells, breaker_cells, active_shapes):
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += float(10.8 ** m_cnt)
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * 0.0203
  return float(score)