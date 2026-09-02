"""Base class for Language Models and Samplers in FunSearch."""
from __future__ import annotations

import abc
from collections.abc import Collection, Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from funsearch.core.programs_database import ProgramsDatabase, Prompt
  from funsearch.sandbox.base import Evaluator


class LLM(abc.ABC):
  """Abstract language model interface for program completion."""

  def __init__(self, samples_per_prompt: int = 1, temperature: float = 0.7) -> None:
    self.samples_per_prompt = samples_per_prompt
    self.temperature = temperature

  @abc.abstractmethod
  def draw_sample(self, prompt: str) -> str:
    """Draws a single code continuation sample from the model given `prompt`."""
    pass

  def draw_samples(self, prompt: str) -> Collection[str]:
    """Draws multiple code continuation samples for a single prompt."""
    return [self.draw_sample(prompt) for _ in range(self.samples_per_prompt)]


class Sampler:
  """Worker that draws prompts from the ProgramsDatabase and queries the LLM."""

  def __init__(
      self,
      database: ProgramsDatabase,
      evaluators: Sequence[Evaluator],
      llm: LLM,
  ) -> None:
    self._database = database
    self._evaluators = evaluators
    self._llm = llm

  def step(self) -> list[tuple[str, int, int]]:
    """Draws one prompt, generates samples, and submits them to evaluators.

    Returns:
      A list of tuples (sample_code, island_id, version_generated).
    """
    prompt = self._database.get_prompt()
    samples = self._llm.draw_samples(prompt.code)
    results = []
    for sample in samples:
      evaluator = self._evaluators[0] if len(self._evaluators) == 1 else self._evaluators[
          hash(sample) % len(self._evaluators)
      ]
      evaluator.analyse(sample, prompt.island_id, prompt.version_generated)
      results.append((sample, prompt.island_id, prompt.version_generated))
    return results
