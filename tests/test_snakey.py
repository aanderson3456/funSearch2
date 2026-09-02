"""Unit tests for Snakey problem specification and Lean 4 transpiler."""
import pytest
from funsearch.core import code_manipulation
from funsearch.problems.snakey import SPECIFICATION, INPUTS
from funsearch.problems.snakey_lean_transpiler import tree_to_lean4, generate_lean_proof_file
from funsearch.sandbox.process_sandbox import ProcessSandbox


def test_snakey_specification_ast():
  evolve_fns = list(code_manipulation.yield_decorated(SPECIFICATION, "funsearch", "evolve"))
  run_fns = list(code_manipulation.yield_decorated(SPECIFICATION, "funsearch", "run"))
  assert evolve_fns == ["priority"]
  assert run_fns == ["evaluate"]


def test_snakey_baseline_evaluation():
  sandbox = ProcessSandbox()
  # Evaluate on radius 3
  res, ok = sandbox.run(SPECIFICATION, "evaluate", 3, timeout_seconds=15)
  assert ok is True
  assert isinstance(res, (int, float))
  assert res > 0.0


def test_lean4_transpiler():
  sample_tree = (
      "move",
      (0, 0),
      [
          ((1, 0), ("move", (0, 1), [], ("win",))),
          ((0, 1), ("move", (1, 0), [], ("win",))),
      ],
      ("win",),
  )
  lean_code = generate_lean_proof_file(sample_tree)
  assert "def snaky_winning_tree : StrategyTree :=" in lean_code
  assert ".move (0, 0) fun b =>" in lean_code
  assert "if b = (1, 0) then" in lean_code
  assert "winning_strategy Snakey_base snaky_winning_tree [] []" in lean_code
