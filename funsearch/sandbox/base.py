"""Abstract Sandbox and Evaluator for FunSearch."""
from __future__ import annotations

import abc
import ast
from collections.abc import Sequence
import copy
from typing import Any, Callable

from absl import logging

from funsearch.core import code_manipulation
from funsearch.core.programs_database import ProgramsDatabase


class _FunctionLineVisitor(ast.NodeVisitor):
  """Visitor that finds the last line number of a function with a given name."""

  def __init__(self, target_function_name: str) -> None:
    self._target_function_name = target_function_name
    self._function_end_line: int | None = None

  def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
    if node.name == self._target_function_name:
      self._function_end_line = getattr(node, 'end_lineno', None)
    self.generic_visit(node)

  @property
  def function_end_line(self) -> int | None:
    return self._function_end_line


def trim_function_body(generated_code: str) -> str:
  """Extracts the body of the generated function, trimming syntax errors & anything after it."""
  if not generated_code:
    return ''

  import textwrap

  text = generated_code.strip('\n\r')

  # If the LLM included a markdown python block, extract only that block
  import re
  match = re.search(r'```(?:python|py)?\n(.*?)\n```', text, re.DOTALL)
  if match:
    text = match.group(1).strip('\n\r')
  else:
    # Fallback to stripping if wrapped entirely in code block
    if text.lstrip().startswith('```'):
      lines = text.splitlines()
      text = '\n'.join(lines[1:-1] if lines[-1].strip().startswith('```') else lines[1:])
      text = text.strip('\n\r')

  # If the LLM re-included a function definition header at the beginning (def foo(...):)
  first_line = next((l.strip() for l in text.splitlines() if l.strip()), '')
  if first_line.startswith('def '):
    try:
      tree = ast.parse(text)
      for node in tree.body:
        if isinstance(node, ast.FunctionDef):
          code_lines = text.splitlines()
          body_start = node.body[0].lineno
          if ast.get_docstring(node) and len(node.body) > 1:
            body_start = node.body[1].lineno
          end_lineno = getattr(node, 'end_lineno', len(code_lines))
          body_lines = code_lines[body_start - 1 : end_lineno]
          body_text = '\n'.join(body_lines)
          dedented = textwrap.dedent(body_text)
          indented = '\n'.join(('  ' + l if l.strip() else '') for l in dedented.splitlines())
          return indented + '\n\n'
    except Exception:
      pass

  # Align first non-empty line indentation if under-indented relative to subsequent lines
  code_lines = text.splitlines()
  non_empty_indices = [i for i, l in enumerate(code_lines) if l.strip()]
  if len(non_empty_indices) >= 2:
    first_idx, second_idx = non_empty_indices[0], non_empty_indices[1]
    first_indent = len(code_lines[first_idx]) - len(code_lines[first_idx].lstrip(' '))
    second_indent = len(code_lines[second_idx]) - len(code_lines[second_idx].lstrip(' '))
    if first_indent < second_indent:
      code_lines[first_idx] = (' ' * second_indent) + code_lines[first_idx].lstrip(' ')
    text = '\n'.join(code_lines)

  # Normalize indentation uniformly using dedent
  dedented = textwrap.dedent(text)
  indented = '\n'.join(('  ' + l if l.strip() else '') for l in dedented.splitlines())

  code = f'def fake_function_header():\n{indented}'
  tree = None

  while tree is None:
    try:
      tree = ast.parse(code)
    except SyntaxError as e:
      lines = code.splitlines()
      if e.lineno is None or e.lineno > len(lines):
        code = '\n'.join(lines[:-1])
      else:
        code = '\n'.join(lines[: e.lineno - 1])
      if not code or code.strip() == 'def fake_function_header():':
        return ''

  visitor = _FunctionLineVisitor('fake_function_header')
  visitor.visit(tree)
  end_line = visitor.function_end_line or len(code.splitlines())
  body_lines = code.splitlines()[1:end_line]
  return '\n'.join(body_lines) + '\n\n'


def sample_to_program(
    generated_code: str,
    version_generated: int | None,
    template: code_manipulation.Program,
    function_to_evolve: str,
) -> tuple[code_manipulation.Function, str]:
  """Returns the compiled generated function and the full runnable program."""
  body = trim_function_body(generated_code)
  if version_generated is not None:
    body = code_manipulation.rename_function_calls(
        body,
        f'{function_to_evolve}_v{version_generated}',
        function_to_evolve,
    )

  program = copy.deepcopy(template)
  evolved_function = program.get_function(function_to_evolve)
  evolved_function.body = body
  return evolved_function, str(program)


def calls_ancestor(program: str, function_to_evolve: str) -> bool:
  """Returns whether the generated function is calling an earlier version."""
  for name in code_manipulation.get_functions_called(program):
    if name.startswith(f'{function_to_evolve}_v'):
      return True
  return False


class Sandbox(abc.ABC):
  """Abstract sandbox for executing generated code."""

  @abc.abstractmethod
  def run(
      self,
      program: str,
      function_to_run: str,
      test_input: Any,
      timeout_seconds: int,
  ) -> tuple[Any, bool]:
    """Executes `function_to_run(test_input)` in the program environment.

    Returns:
      (output, success_bool)
    """
    pass


class Evaluator:
  """Evaluator that coordinates AST trimming, sandbox execution, and DB registration."""

  def __init__(
      self,
      database: ProgramsDatabase,
      template: code_manipulation.Program,
      function_to_evolve: str,
      function_to_run: str,
      inputs: Sequence[Any],
      sandbox: Sandbox,
      timeout_seconds: int = 30,
      on_evaluation_callback: Callable[[dict[str, Any]], None] | None = None,
  ) -> None:
    self._database = database
    self._template = template
    self._function_to_evolve = function_to_evolve
    self._function_to_run = function_to_run
    self._inputs = inputs
    self._sandbox = sandbox
    self._timeout_seconds = timeout_seconds
    self._on_evaluation_callback = on_evaluation_callback

  def analyse(
      self,
      sample: str,
      island_id: int | None,
      version_generated: int | None,
  ) -> tuple[code_manipulation.Function | None, dict[Any, float] | None]:
    """Compiles the sample into a program and executes it on test inputs."""
    new_function, program = sample_to_program(
        sample, version_generated, self._template, self._function_to_evolve
    )

    if not new_function.body.strip():
      print("\n======== SYNTAX ERROR: EMPTY BODY AFTER TRIM ========\n")
      print("RAW LLM OUTPUT:\n", sample)
      print("=====================================================\n")
      if self._on_evaluation_callback:
        self._on_evaluation_callback({
            "status": "syntax_error",
            "score": None,
            "island_id": island_id,
            "sample": sample,
        })
      return None, None

    scores_per_test = {}
    success = True
    for current_input in self._inputs:
      test_output, runs_ok = self._sandbox.run(
          program, self._function_to_run, current_input, self._timeout_seconds
      )
      if (
          runs_ok
          and not calls_ancestor(program, self._function_to_evolve)
          and test_output is not None
      ):
        if not isinstance(test_output, (int, float)):
          runs_ok = False
          success = False
          break
        scores_per_test[current_input] = float(test_output)
      else:
        success = False
        break

    if success and scores_per_test:
      is_new_best = self._database.register_program(new_function, island_id, scores_per_test)
      score = scores_per_test[list(scores_per_test.keys())[-1]]
      if self._on_evaluation_callback:
        self._on_evaluation_callback({
            "status": "success",
            "score": score,
            "is_new_best": is_new_best,
            "island_id": island_id,
            "function": new_function,
            "scores_per_test": scores_per_test,
        })
      return new_function, scores_per_test
    else:
      print("\n======== EXEC ERROR ========\n")
      print("RAW LLM OUTPUT:\n", sample)
      print("=====================================================\n")
      if self._on_evaluation_callback:
        self._on_evaluation_callback({
            "status": "exec_error",
            "score": None,
            "island_id": island_id,
            "sample": sample,
        })
      return None, None
