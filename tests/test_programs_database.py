"""Unit tests for ProgramsDatabase and Island model."""
import pytest
from funsearch.core import code_manipulation
from funsearch.core.config import ProgramsDatabaseConfig
from funsearch.core.programs_database import ProgramsDatabase, _softmax


SAMPLE_CODE = '''@funsearch.evolve
def priority(x: int) -> float:
  return float(x * 2)

@funsearch.run
def evaluate(n: int) -> int:
  return int(priority(n))
'''


def test_softmax():
  import numpy as np
  logits = np.array([1.0, 2.0, 3.0])
  probs = _softmax(logits, 1.0)
  assert np.isclose(np.sum(probs), 1.0)
  assert probs[2] > probs[1] > probs[0]


def test_programs_database_registration():
  prog = code_manipulation.text_to_program(SAMPLE_CODE)
  fn = prog.get_function("priority")
  config = ProgramsDatabaseConfig(num_islands=4, functions_per_prompt=2)
  db = ProgramsDatabase(config, prog, "priority")

  # Register baseline seed
  is_best = db.register_program(fn, island_id=None, scores_per_test={1: 2.0, 2: 4.0})
  assert is_best is True
  assert db.global_best_score == 4.0
  assert db.total_programs_registered == 1

  # Sample prompt
  prompt = db.get_prompt()
  assert "priority_v0" in prompt.code
  assert "priority_v1" in prompt.code
