# Breaker ID: 5
# Longevity Score: 4
# Gens Survived: 1
# Mutations Defeated: 4

def breaker_priority(candidate, maker_cells, breaker_cells, active_shapes):
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  block_weights = {0: 1.0, 1: 4.9, 2: 36.9, 3: 264.0, 4: 90000.0, 5: 1e8}
  score = 0.0
  overlap = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += block_weights.get(m_cnt, 10.0 ** m_cnt)
      overlap += 1
  score += (overlap ** 1.5) * 3.67
  return float(score)