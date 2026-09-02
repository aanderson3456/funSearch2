"""Unit tests for AST code manipulation routines."""
import pytest
from funsearch.core import code_manipulation


SAMPLE_CODE = '''"""Sample module."""
import numpy as np

@funsearch.evolve
def priority(el: tuple[int, ...], n: int) -> float:
  """Returns priority."""
  return float(sum(el))

@funsearch.run
def evaluate(n: int) -> int:
  return 42
'''


def test_text_to_program():
  prog = code_manipulation.text_to_program(SAMPLE_CODE)
  assert len(prog.functions) == 2
  assert prog.functions[0].name == "priority"
  assert prog.functions[1].name == "evaluate"
  assert "import numpy as np" in prog.preface


def test_yield_decorated():
  evolve_fns = list(code_manipulation.yield_decorated(SAMPLE_CODE, "funsearch", "evolve"))
  run_fns = list(code_manipulation.yield_decorated(SAMPLE_CODE, "funsearch", "run"))
  assert evolve_fns == ["priority"]
  assert run_fns == ["evaluate"]


def test_rename_function_calls():
  code = "def foo():\n  return priority_v1(x) + 2"
  renamed = code_manipulation.rename_function_calls(code, "priority_v1", "priority")
  assert "priority(x)" in renamed
  assert "priority_v1" not in renamed


def test_get_functions_called():
  code = "def foo():\n  a = priority_v0(x)\n  b = bar(y)\n  return a + b"
  calls = code_manipulation.get_functions_called(code)
  assert "priority_v0" in calls
  assert "bar" in calls
