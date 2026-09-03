# Breaker ID: 0
# Longevity Score: 7
# Gens Survived: 1
# Mutations Defeated: 7

def breaker_priority(candidate, maker_cells, breaker_cells, active_shapes):
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == len(shape) - 1:
        return 1e9  # Critical: Block immediate win
      score += float(8.3 ** m_cnt)
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.22
  return float(score)