"""FunSearch evolutionary engine coordinator."""
from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
import time
from typing import Any, Callable

from absl import logging

from funsearch.core import code_manipulation
from funsearch.core import config as config_lib
from funsearch.core.programs_database import ProgramsDatabase
from funsearch.llm.base import LLM, Sampler
from funsearch.sandbox.base import Evaluator
from funsearch.sandbox.process_sandbox import ProcessSandbox
from funsearch.ui.live_dashboard import LiveDashboard
from funsearch.ui.logger import ExperimentLogger


def _extract_function_names(specification: str) -> tuple[str, str]:
  """Returns the name of the function to evolve and of the function to run."""
  run_functions = list(code_manipulation.yield_decorated(specification, "funsearch", "run"))
  if len(run_functions) != 1:
    raise ValueError(f"Expected 1 function decorated with `@funsearch.run`, found {len(run_functions)}")
  
  evolve_functions = list(code_manipulation.yield_decorated(specification, "funsearch", "evolve"))
  if len(evolve_functions) != 1:
    raise ValueError(f"Expected 1 function decorated with `@funsearch.evolve`, found {len(evolve_functions)}")
  
  return evolve_functions[0], run_functions[0]


class FunSearchEngine:
  """Coordinates the evolutionary program search process."""

  def __init__(
      self,
      specification: str,
      inputs: Sequence[Any],
      config: config_lib.Config,
      llm: LLM,
      problem_name: str = "custom",
      enable_live_ui: bool = True,
  ) -> None:
    self.specification = specification
    self.inputs = inputs
    self.config = config
    self.llm = llm
    self.problem_name = problem_name
    self.enable_live_ui = enable_live_ui

    self.function_to_evolve, self.function_to_run = _extract_function_names(specification)
    self.template = code_manipulation.text_to_program(specification)

    self.database = ProgramsDatabase(
        config.programs_database, self.template, self.function_to_evolve
    )
    self.logger = ExperimentLogger(config.output_dir, problem_name)
    self.sandbox = ProcessSandbox()

    self.dashboard: LiveDashboard | None = None
    if self.enable_live_ui:
      self.dashboard = LiveDashboard(
          problem_name=problem_name,
          model_name=getattr(llm, "model_name", type(llm).__name__),
          database=self.database,
          max_iterations=config.max_iterations,
      )

    self.evaluators: list[Evaluator] = []
    for _ in range(config.num_evaluators):
      self.evaluators.append(
          Evaluator(
              database=self.database,
              template=self.template,
              function_to_evolve=self.function_to_evolve,
              function_to_run=self.function_to_run,
              inputs=self.inputs,
              sandbox=self.sandbox,
              timeout_seconds=config.sandbox_timeout,
              on_evaluation_callback=self._on_evaluation,
          )
      )

    self.sampler = Sampler(
        database=self.database,
        evaluators=self.evaluators,
        llm=self.llm,
    )

    self._iteration = 0

  def _on_evaluation(self, event: dict[str, Any]) -> None:
    """Dispatches evaluation event to UI and logger."""
    if self.dashboard:
      self.dashboard.on_evaluation(event)

    status = event.get("status", "unknown")
    score = event.get("score")
    is_new_best = event.get("is_new_best", False)
    island_id = event.get("island_id")
    scores_per_test = event.get("scores_per_test")

    self.logger.log_evaluation(
        iteration=self._iteration,
        status=status,
        score=score,
        island_id=island_id,
        is_new_best=is_new_best,
        scores_per_test=scores_per_test,
    )

    if is_new_best and "function" in event:
      self.logger.save_best_program(event["function"], score, self._iteration)

  def run(self) -> tuple[code_manipulation.Function | None, float]:
    """Runs the main evolutionary search loop."""
    if self.dashboard:
      self.dashboard.start()

    try:
      # Step 0: Evaluate the initial seed program
      initial_fn = self.template.get_function(self.function_to_evolve)
      self.evaluators[0].analyse(initial_fn.body, island_id=None, version_generated=None)

      if self.dashboard:
        self.dashboard.log_event(
            f"Seed baseline initialized with score = {self.database.global_best_score:.2f}",
            style="bold yellow",
            emoji="🌱",
        )

      # Main search loop
      while True:
        self._iteration += 1
        if self.dashboard:
          self.dashboard.step(self._iteration)

        if self.config.max_iterations and self._iteration > self.config.max_iterations:
          break

        # Draw prompt, sample from LLM, and evaluate
        self.sampler.step()

    except KeyboardInterrupt:
      logging.info("FunSearch interrupted by user.")
    finally:
      if self.dashboard:
        self.dashboard.stop()

    return self.database.global_best_program, self.database.global_best_score
