# Maker ID: 2
# Longevity Score: 14
# Gens Survived: 1
# Mutations Defeated: 14

def priority(candidate, maker_cells, breaker_cells, active_shapes):
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += float(6.5 ** m_cnt)
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * 0.0073
  return float(score)