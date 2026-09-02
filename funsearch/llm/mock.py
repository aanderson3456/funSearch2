"""Mock LLM sampler for offline testing, debugging, and baseline evolutionary runs."""
from __future__ import annotations

import random
from funsearch.llm.base import LLM


_SNAKEY_SNIPPETS = [
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += float(10 ** m_cnt) * 1.5
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.15
  return float(score)""",
    """  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += float(7 ** m_cnt)
  # Manhattan center bias
  score -= (candidate[0] ** 2 + candidate[1] ** 2) * 0.02
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

    if "candidate" in prompt and "maker_cells" in prompt:
      snippet = random.choice(_SNAKEY_SNIPPETS)
      return snippet.replace("1.5", f"{1.0 + c * 0.1:.2f}")
    elif "remaining_capacities" in prompt:
      snippet = random.choice(_BIN_PACKING_SNIPPETS)
      return snippet.replace("1.2", f"{1.0 + c * 0.05:.2f}")
    else:
      snippet = random.choice(_CAP_SET_SNIPPETS)
      return snippet.replace("97", str(97 + c))
