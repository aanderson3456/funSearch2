"""Configuration dataclasses for FunSearch experiments."""
from __future__ import annotations

import dataclasses
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class ProgramsDatabaseConfig:
  """Configuration of the Programs Database and Islands model.

  Attributes:
    functions_per_prompt: Number of previous programs to include in prompts (usually 2).
    num_islands: Number of islands to maintain as a diversity mechanism.
    reset_period: How often (in seconds) the weakest islands should be reset.
    cluster_sampling_temperature_init: Initial temperature for softmax sampling
        of clusters within an island.
    cluster_sampling_temperature_period: Period of linear decay of the cluster
        sampling temperature.
  """
  functions_per_prompt: int = 2
  num_islands: int = 10
  reset_period: int = 4 * 60 * 60  # 4 hours default
  cluster_sampling_temperature_init: float = 0.1
  cluster_sampling_temperature_period: int = 30_000


@dataclasses.dataclass(frozen=True)
class Config:
  """Configuration of a FunSearch experiment run.

  Attributes:
    programs_database: Configuration of the evolutionary database.
    num_samplers: Number of independent Samplers.
    num_evaluators: Number of independent program Evaluators.
    samples_per_prompt: How many candidate programs to sample per prompt.
    sandbox_timeout: Maximum execution timeout in seconds per evaluation.
    max_iterations: Maximum total iterations to run (None for infinite).
    model_name: Default LLM model identifier (e.g., 'gemini-3.7-flash', 'gemini-2.5-flash').
    temperature: LLM sampling temperature.
    output_dir: Directory where discovered programs and logs are saved.
  """
  programs_database: ProgramsDatabaseConfig = dataclasses.field(
      default_factory=ProgramsDatabaseConfig)
  num_samplers: int = 1
  num_evaluators: int = 4
  samples_per_prompt: int = 4
  sandbox_timeout: int = 30
  max_iterations: int | None = None
  model_name: str = "gemini-3.7-flash"
  temperature: float = 0.7
  output_dir: Path | str = "./outputs"
