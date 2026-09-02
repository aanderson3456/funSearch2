"""A programs database that implements the evolutionary algorithm with the Islands model."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
import copy
import dataclasses
import time
from typing import Any

from absl import logging
import numpy as np
import scipy.special

from funsearch.core import code_manipulation
from funsearch.core import config as config_lib

Signature = tuple[float, ...]
ScoresPerTest = Mapping[Any, float]


def _softmax(logits: np.ndarray, temperature: float) -> np.ndarray:
  """Returns the tempered softmax of 1D finite `logits`."""
  if not np.all(np.isfinite(logits)):
    non_finites = set(logits[~np.isfinite(logits)])
    raise ValueError(f'`logits` contains non-finite value(s): {non_finites}')
  if not np.issubdtype(logits.dtype, np.floating):
    logits = np.array(logits, dtype=np.float32)

  result = scipy.special.softmax(logits / temperature, axis=-1)
  # Ensure probabilities sum to 1
  index = np.argmax(result)
  result[index] = 1 - np.sum(result[0:index]) - np.sum(result[index + 1 :])
  return result


def _reduce_score(scores_per_test: ScoresPerTest) -> float:
  """Reduces per-test scores into a single scalar score (e.g. mean or final test score)."""
  if not scores_per_test:
    return -float('inf')
  # DeepMind default: returns score on the last (usually largest/hardest) test case
  return scores_per_test[list(scores_per_test.keys())[-1]]


def _get_signature(scores_per_test: ScoresPerTest) -> Signature:
  """Represents test scores as a canonical signature."""
  return tuple(scores_per_test[k] for k in sorted(scores_per_test.keys()))


@dataclasses.dataclass(frozen=True)
class Prompt:
  """A prompt produced by the ProgramsDatabase, to be sent to Samplers."""
  code: str
  version_generated: int
  island_id: int


@dataclasses.dataclass
class Cluster:
  """A cluster of programs with identical signature (behavior)."""
  score: float
  programs: list[code_manipulation.Function] = dataclasses.field(default_factory=list)

  def register_program(self, program: code_manipulation.Function) -> None:
    self.programs.append(program)

  @property
  def num_programs(self) -> int:
    return len(self.programs)


class Island:
  """An isolated population (deme) of programs."""

  def __init__(
      self,
      template: code_manipulation.Program,
      function_to_evolve: str,
      functions_per_prompt: int,
      cluster_sampling_temperature_init: float = 0.1,
      cluster_sampling_temperature_period: int = 30_000,
  ) -> None:
    self._template = template
    self._function_to_evolve = function_to_evolve
    self._functions_per_prompt = functions_per_prompt
    self._cluster_sampling_temperature_init = cluster_sampling_temperature_init
    self._cluster_sampling_temperature_period = cluster_sampling_temperature_period

    self._clusters: dict[Signature, Cluster] = {}
    self._num_programs: int = 0

  @property
  def num_programs(self) -> int:
    return self._num_programs

  @property
  def num_clusters(self) -> int:
    return len(self._clusters)

  @property
  def temperature(self) -> float:
    period = self._cluster_sampling_temperature_period
    ratio = (self._num_programs % period) / period
    return self._cluster_sampling_temperature_init * (1.0 - ratio)

  def register_program(
      self,
      program: code_manipulation.Function,
      scores_per_test: ScoresPerTest,
  ) -> None:
    """Registers a program into the island's clusters."""
    signature = _get_signature(scores_per_test)
    score = _reduce_score(scores_per_test)
    if signature not in self._clusters:
      self._clusters[signature] = Cluster(score=score)
    self._clusters[signature].register_program(program)
    self._num_programs += 1

  def get_prompt(self) -> tuple[str, int]:
    """Samples programs and constructs a prompt."""
    signatures = list(self._clusters.keys())
    if not signatures:
      base_fn = self._template.get_function(self._function_to_evolve)
      return self._build_prompt([base_fn], 1), 1

    cluster_scores = np.array([self._clusters[s].score for s in signatures])

    # Softmax sample clusters
    temp = max(self.temperature, 1e-6)
    probs = _softmax(cluster_scores, temp)
    
    num_to_sample = min(self._functions_per_prompt, len(signatures))
    chosen_indices = np.random.choice(
        len(signatures), size=num_to_sample, replace=False, p=probs
    )

    chosen_programs: list[code_manipulation.Function] = []
    for idx in chosen_indices:
      sig = signatures[idx]
      cluster = self._clusters[sig]
      # Sample a program favoring shorter lengths
      lengths = np.array([len(p.body) for p in cluster.programs])
      len_probs = _softmax(-lengths, 1.0)
      prog_idx = np.random.choice(len(cluster.programs), p=len_probs)
      chosen_programs.append(cluster.programs[prog_idx])

    # Sort chosen programs by score ascending
    chosen_programs.sort(key=lambda p: self._clusters[_get_signature_from_prog(p, self._clusters)].score)

    version_generated = len(chosen_programs)
    return self._build_prompt(chosen_programs, version_generated), version_generated

  def _build_prompt(
      self,
      programs: list[code_manipulation.Function],
      version_generated: int,
  ) -> str:
    """Constructs prompt string with versions _v0, _v1, ... and the target _v{N}."""
    prompt_prog = copy.deepcopy(self._template)
    target_fn = prompt_prog.get_function(self._function_to_evolve)
    fn_idx = prompt_prog.find_function_index(self._function_to_evolve)

    # Insert versioned predecessor functions
    versioned_funcs = []
    for i, prog in enumerate(programs):
      v_func = copy.deepcopy(prog)
      v_func.name = f"{self._function_to_evolve}_v{i}"
      versioned_funcs.append(v_func)

    # The function to be completed
    prompt_target = copy.deepcopy(target_fn)
    prompt_target.name = f"{self._function_to_evolve}_v{version_generated}"
    prompt_target.body = ""  # LLM will complete the body

    prompt_prog.functions = (
        prompt_prog.functions[:fn_idx]
        + versioned_funcs
        + [prompt_target]
        + prompt_prog.functions[fn_idx + 1 :]
    )

    prompt_str = str(prompt_prog)
    # Cut off anything after the target function header
    target_header = f"def {self._function_to_evolve}_v{version_generated}"
    cutoff = prompt_str.find(target_header)
    if cutoff != -1:
      end_of_header = prompt_str.find(":\n", cutoff)
      if end_of_header != -1:
        if prompt_target.docstring:
          end_of_doc = prompt_str.find('"""\n', end_of_header)
          if end_of_doc != -1:
            prompt_str = prompt_str[: end_of_doc + 4]
          else:
            prompt_str = prompt_str[: end_of_header + 2]
        else:
          prompt_str = prompt_str[: end_of_header + 2]

    return prompt_str


def _get_signature_from_prog(
    prog: code_manipulation.Function, clusters: dict[Signature, Cluster]
) -> Signature:
  for sig, cl in clusters.items():
    if prog in cl.programs:
      return sig
  return list(clusters.keys())[0]


class ProgramsDatabase:
  """Maintains multiple islands of evolved programs."""

  def __init__(
      self,
      config: config_lib.ProgramsDatabaseConfig,
      template: code_manipulation.Program,
      function_to_evolve: str,
  ) -> None:
    self._config = config
    self._template = template
    self._function_to_evolve = function_to_evolve

    self._islands: list[Island] = [
        Island(
            template,
            function_to_evolve,
            config.functions_per_prompt,
            config.cluster_sampling_temperature_init,
            config.cluster_sampling_temperature_period,
        )
        for _ in range(config.num_islands)
    ]

    self._best_score_per_island: list[float] = [-float('inf')] * config.num_islands
    self._best_program_per_island: list[code_manipulation.Function | None] = [None] * config.num_islands
    self._best_scores_per_test_per_island: list[ScoresPerTest | None] = [None] * config.num_islands

    self._global_best_score: float = -float('inf')
    self._global_best_program: code_manipulation.Function | None = None
    self._global_best_scores_per_test: ScoresPerTest | None = None

    self._total_programs_evaluated: int = 0
    self._total_programs_registered: int = 0
    self._last_reset_time: float = time.time()

  @property
  def total_programs_registered(self) -> int:
    return self._total_programs_registered

  @property
  def global_best_score(self) -> float:
    return self._global_best_score

  @property
  def global_best_program(self) -> code_manipulation.Function | None:
    return self._global_best_program

  @property
  def islands(self) -> list[Island]:
    return self._islands

  @property
  def best_score_per_island(self) -> list[float]:
    return self._best_score_per_island

  def get_prompt(self) -> Prompt:
    """Selects an island at random and returns a constructed prompt."""
    island_id = np.random.randint(len(self._islands))
    code, version_generated = self._islands[island_id].get_prompt()
    return Prompt(code=code, version_generated=version_generated, island_id=island_id)

  def register_program(
      self,
      program: code_manipulation.Function,
      island_id: int | None,
      scores_per_test: ScoresPerTest,
  ) -> bool:
    """Registers a program into the database. Returns True if this is a new global best."""
    score = _reduce_score(scores_per_test)
    self._total_programs_registered += 1
    is_new_global_best = False

    if island_id is None:
      # Register in all islands (initial seed program)
      for i in range(len(self._islands)):
        self._register_in_island(program, i, scores_per_test, score)
    else:
      self._register_in_island(program, island_id, scores_per_test, score)

    if score > self._global_best_score:
      self._global_best_score = score
      self._global_best_program = program
      self._global_best_scores_per_test = scores_per_test
      is_new_global_best = True

    # Check for island resets
    if time.time() - self._last_reset_time > self._config.reset_period:
      self._reset_islands()

    return is_new_global_best

  def _register_in_island(
      self,
      program: code_manipulation.Function,
      island_id: int,
      scores_per_test: ScoresPerTest,
      score: float,
  ) -> None:
    self._islands[island_id].register_program(program, scores_per_test)
    if score > self._best_score_per_island[island_id]:
      self._best_score_per_island[island_id] = score
      self._best_program_per_island[island_id] = program
      self._best_scores_per_test_per_island[island_id] = scores_per_test

  def _reset_islands(self) -> None:
    """Resets the bottom 50% islands by copying the top 50%."""
    indices = np.argsort(self._best_score_per_island)
    num_reset = len(self._islands) // 2
    bottom_indices = indices[:num_reset]
    top_indices = indices[num_reset:]

    for bottom_idx in bottom_indices:
      donor_idx = np.random.choice(top_indices)
      self._islands[bottom_idx] = copy.deepcopy(self._islands[donor_idx])
      self._best_score_per_island[bottom_idx] = self._best_score_per_island[donor_idx]
      self._best_program_per_island[bottom_idx] = copy.deepcopy(self._best_program_per_island[donor_idx])
      self._best_scores_per_test_per_island[bottom_idx] = copy.deepcopy(self._best_scores_per_test_per_island[donor_idx])

    self._last_reset_time = time.time()
    logging.info(f"Islands reset complete. Bottom {num_reset} replaced.")
