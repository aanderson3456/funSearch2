# Breaker ID: 385
# Longevity Score: 110
# Gens Survived: 2
# Mutations Defeated: 55

def breaker_priority(candidate, maker_cells, breaker_cells, active_shapes):
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  block_weights = {0: 1.0, 1: 6.1, 2: 75.6, 3: 1136.9, 4: 90000.0, 5: 1e8}
  score = 0.0
  overlap = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += block_weights.get(m_cnt, 10.0 ** m_cnt)
      overlap += 1
  score += (overlap ** 1.5) * 4.82
  return float(score)