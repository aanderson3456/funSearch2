# Maker ID: 64
# Longevity Score: 112
# Gens Survived: 2
# Mutations Defeated: 56

def priority(candidate, maker_cells, breaker_cells, active_shapes):
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  weights = {0: 1.0, 1: 4.3, 2: 20.5, 3: 581.6, 4: 25000.0, 5: 1000000.0}
  score = 0.0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** m_cnt)
      active_count += 1
  score += (active_count ** 1.3) * 2.35
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.08
  return float(score)