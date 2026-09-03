# Rank 1 Snakey Maker Strategy
# Fitness Score: 280.00

def priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  """Returns priority for Maker choosing `candidate` cell.

Higher score means Maker prefers this cell."""
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  weights = {0: 1.0, 1: 4.1, 2: 26.9, 3: 507.8, 4: 25000.0, 5: 1000000.0}
  score = 0.0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** m_cnt)
      active_count += 1
  score += (active_count ** 1.3) * 2.97
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.08
  return float(score)


