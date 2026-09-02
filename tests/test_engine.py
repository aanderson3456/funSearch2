"""Integration tests for FunSearchEngine with MockLLM."""
import pytest
from funsearch.core.config import Config, ProgramsDatabaseConfig
from funsearch.engine import FunSearchEngine
from funsearch.llm.mock import MockLLM
from funsearch.problems.cap_set import SPECIFICATION, INPUTS


def test_engine_run_simulation():
  db_config = ProgramsDatabaseConfig(num_islands=2, functions_per_prompt=2)
  config = Config(
      programs_database=db_config,
      samples_per_prompt=2,
      max_iterations=3,
      sandbox_timeout=10,
  )
  llm = MockLLM(samples_per_prompt=2)
  
  # Run on small inputs for fast test
  engine = FunSearchEngine(
      specification=SPECIFICATION,
      inputs=[2, 3],
      config=config,
      llm=llm,
      problem_name="cap_set_test",
      enable_live_ui=False,
  )

  best_prog, best_score = engine.run()
  assert best_score > 0
  assert best_prog is not None
  assert engine.database.total_programs_registered >= 1
