# Maker ID: 3
# Longevity Score: 8
# Gens Survived: 1
# Mutations Defeated: 8

def priority(candidate, maker_cells, breaker_cells, active_shapes):
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  high_threats = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt >= 4:
        score += 50000.0
      elif m_cnt == 3:
        high_threats += 1
        score += 800.0
      else:
        score += float(10 ** m_cnt) * 2.26
  if high_threats > 1:
    score += 3567.1
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.189
  return float(score)