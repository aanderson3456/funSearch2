# Rank 7 Snakey Breaker Strategy
# Fitness Score: 1010.00

def breaker_priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  """Returns priority for Breaker choosing `candidate` cell.

Higher score means Breaker prefers this cell to block Maker."""
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  block_weights = {0: 1.0, 1: 9.3, 2: 89.8, 3: 328.4, 4: 80151.0, 5: 1e8}
  score = 0.0
  overlap = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += block_weights.get(m_cnt, 10.0 ** m_cnt)
      overlap += 1
  score += (overlap ** 1.57) * 1.82
  return float(score)


