# Breaker ID: 158
# Longevity Score: 112
# Gens Survived: 2
# Mutations Defeated: 56

def breaker_priority(candidate, maker_cells, breaker_cells, active_shapes):
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  block_weights = {0: 1.0, 1: 5.0, 2: 49.3, 3: 934.6, 4: 90000.0, 5: 1e8}
  score = 0.0
  overlap = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += block_weights.get(m_cnt, 10.0 ** m_cnt)
      overlap += 1
  score += (overlap ** 1.5) * 3.98
  return float(score)