"""Mock LLM sampler for offline testing, debugging, and baseline evolutionary runs."""
from __future__ import annotations

import random
from funsearch.llm.base import LLM


_SNAKEY_MAKER_SNIPPETS = [
    """  m_set = set(maker_cells)
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
        score += float(10 ** m_cnt) * {weight:.2f}
  if high_threats > 1:
    score += {fork_bonus:.1f}
  score -= (abs(candidate[0]) + abs(candidate[1])) * {center_penalty:.3f}
  return float(score)""",
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += float({base:.1f} ** m_cnt)
  dist_sq = candidate[0] ** 2 + candidate[1] ** 2
  score -= dist_sq * {dist_penalty:.4f}
  return float(score)""",
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  weights = {{0: 1.0, 1: {w1:.1f}, 2: {w2:.1f}, 3: {w3:.1f}, 4: 25000.0, 5: 1000000.0}}
  score = 0.0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** m_cnt)
      active_count += 1
  score += (active_count ** 1.3) * {density:.2f}
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.08
  return float(score)""",
]

_SNAKEY_BREAKER_SNIPPETS = [
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt == len(shape) - 1:
        return 1e9  # Critical: Block immediate win
      score += float({base:.1f} ** m_cnt)
  score -= (abs(candidate[0]) + abs(candidate[1])) * {center:.2f}
  return float(score)""",
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  fork_block_count = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt >= 4:
        return 500000.0
      elif m_cnt == 3:
        fork_block_count += 1
        score += {threat3:.1f}
      else:
        score += float(8 ** m_cnt)
  if fork_block_count > 1:
    score += {anti_fork:.1f}
  score += (10.0 - (candidate[0] ** 2 + candidate[1] ** 2) * 0.05)
  return float(score)""",
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  block_weights = {{0: 1.0, 1: {bw1:.1f}, 2: {bw2:.1f}, 3: {bw3:.1f}, 4: 90000.0, 5: 1e8}}
  score = 0.0
  overlap = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += block_weights.get(m_cnt, 10.0 ** m_cnt)
      overlap += 1
  score += (overlap ** 1.5) * {overlap_w:.2f}
  return float(score)""",
]

_CAP_SET_SNIPPETS = [
    """  score = 0.0
  for i, val in enumerate(el):
    score += (val ** 2) * (i + 1)
  return float(score)""",
    """  score = sum(val * (3 ** i) for i, val in enumerate(el))
  return float(score % 97)""",
]

_BIN_PACKING_SNIPPETS = [
    """  priorities = []
  for cap in remaining_capacities:
    if cap >= item:
      priorities.append(-(cap - item) * 1.2)
    else:
      priorities.append(-1e9)
  return priorities""",
]


class MockLLM(LLM):
  """Deterministic/heuristic mock sampler that yields valid Python function bodies for tests."""

  def __init__(
      self,
      samples_per_prompt: int = 1,
      temperature: float = 0.7,
  ) -> None:
    super().__init__(samples_per_prompt=samples_per_prompt, temperature=temperature)
    self._sample_counter = 0

  def draw_sample(self, prompt: str) -> str:
    """Selects a snippet matching prompt signature and introduces slight variations."""
    self._sample_counter += 1
    c = random.randint(1, 50)

    if "breaker_priority" in prompt:
      tmpl = random.choice(_SNAKEY_BREAKER_SNIPPETS)
      return tmpl.format(
          base=7.0 + random.uniform(0.5, 4.0),
          center=random.uniform(0.05, 0.25),
          threat3=random.uniform(500.0, 3000.0),
          anti_fork=random.uniform(5000.0, 20000.0),
          bw1=random.uniform(3.0, 10.0),
          bw2=random.uniform(25.0, 80.0),
          bw3=random.uniform(250.0, 1200.0),
          overlap_w=random.uniform(1.0, 5.0),
      )
    elif "candidate" in prompt and "maker_cells" in prompt:
      tmpl = random.choice(_SNAKEY_MAKER_SNIPPETS)
      return tmpl.format(
          weight=random.uniform(0.8, 2.5),
          fork_bonus=random.uniform(1000.0, 8000.0),
          center_penalty=random.uniform(0.05, 0.25),
          base=6.0 + random.uniform(0.5, 5.0),
          dist_penalty=random.uniform(0.005, 0.04),
          w1=random.uniform(3.0, 8.0),
          w2=random.uniform(20.0, 60.0),
          w3=random.uniform(200.0, 800.0),
          density=random.uniform(1.0, 4.0),
      )
    elif "remaining_capacities" in prompt:
      snippet = random.choice(_BIN_PACKING_SNIPPETS)
      return snippet.replace("1.2", f"{1.0 + c * 0.05:.2f}")
    else:
      snippet = random.choice(_CAP_SET_SNIPPETS)
      return snippet.replace("97", str(97 + c))
