"""Structured experiment logging and program persistence."""
from __future__ import annotations

import json
from pathlib import Path
import time
from typing import Any

from funsearch.core.code_manipulation import Function


class ExperimentLogger:
  """Saves experiment progress, best programs, and telemetry to disk."""

  def __init__(self, output_dir: Path | str, problem_name: str) -> None:
    self.output_dir = Path(output_dir)
    self.problem_name = problem_name
    self.run_id = f"{problem_name}_{int(time.time())}"
    self.run_dir = self.output_dir / self.run_id
    self.run_dir.mkdir(parents=True, exist_ok=True)

    self.programs_dir = self.run_dir / "programs"
    self.programs_dir.mkdir(exist_ok=True)

    self.events_file = self.run_dir / "events.jsonl"
    self.best_program_file = self.run_dir / "best_program.py"

  def log_evaluation(
      self,
      iteration: int,
      status: str,
      score: float | None,
      island_id: int | None,
      is_new_best: bool = False,
      scores_per_test: dict[Any, float] | None = None,
  ) -> None:
    """Logs an evaluation event to the JSONL log file."""
    record = {
        "timestamp": time.time(),
        "iteration": iteration,
        "status": status,
        "score": score,
        "island_id": island_id,
        "is_new_best": is_new_best,
        "scores_per_test": {str(k): v for k, v in (scores_per_test or {}).items()},
    }
    with open(self.events_file, "a", encoding="utf-8") as f:
      f.write(json.dumps(record) + "\n")

  def save_best_program(self, program: Function, score: float, iteration: int) -> None:
    """Saves the current best program to best_program.py and an indexed checkpoint."""
    code_content = f"# FunSearch Best Discovered Program\n# Problem: {self.problem_name}\n# Score: {score}\n# Discovered at iteration: {iteration}\n# Timestamp: {time.ctime()}\n\n{str(program)}"
    
    with open(self.best_program_file, "w", encoding="utf-8") as f:
      f.write(code_content)

    ckpt_file = self.programs_dir / f"prog_iter_{iteration}_score_{score:.2f}.py"
    with open(ckpt_file, "w", encoding="utf-8") as f:
      f.write(code_content)
