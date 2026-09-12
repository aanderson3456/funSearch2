"""In-process fast Sandbox for trusted code and boost-mode execution."""
from __future__ import annotations

from typing import Any
from absl import logging

from funsearch.sandbox.base import Sandbox


class InProcessSandbox(Sandbox):
  """Executes Python code directly in-process with minimal overhead for boost mode."""

  def run(
      self,
      program: str,
      function_to_run: str,
      test_input: Any,
      timeout_seconds: int = 30,
  ) -> tuple[Any, bool]:
    class _FunSearchStub:
      evolve = staticmethod(lambda fn: fn)
      run = staticmethod(lambda fn: fn)

    namespace: dict[str, Any] = {"funsearch": _FunSearchStub}
    try:
      exec(program, namespace)  # pylint: disable=exec-used
      if function_to_run not in namespace:
        return None, False
      target_fn = namespace[function_to_run]
      output = target_fn(test_input)
      return output, True
    except Exception as e:
      logging.debug(f"InProcess execution error: {e}")
      return None, False
