"""Multi-process isolated Sandbox for running untrusted evolved code."""
from __future__ import annotations

import multiprocessing as mp
import sys
import traceback
from typing import Any

from absl import logging

from funsearch.sandbox.base import Sandbox


def _worker_target(
    program: str,
    function_to_run: str,
    test_input: Any,
    result_queue: mp.Queue,
) -> None:
  """Target function for isolated worker process."""
  try:
    # Execute the program in a fresh global namespace with funsearch stubs
    class _FunSearchStub:
      evolve = staticmethod(lambda fn: fn)
      run = staticmethod(lambda fn: fn)

    namespace: dict[str, Any] = {"funsearch": _FunSearchStub}
    exec(program, namespace)  # pylint: disable=exec-used

    if function_to_run not in namespace:
      result_queue.put((None, False, f"Function '{function_to_run}' not found in program."))
      return

    target_fn = namespace[function_to_run]
    output = target_fn(test_input)
    result_queue.put((output, True, None))
  except Exception as e:  # pylint: disable=broad-except
    result_queue.put((None, False, f"{type(e).__name__}: {str(e)}"))


class ProcessSandbox(Sandbox):
  """Executes Python code in an isolated sub-process with timeout and exception containment."""

  def __init__(self, use_fork: bool = True) -> None:
    # Use spawn or fork context depending on platform
    try:
      self._ctx = mp.get_context("fork" if sys.platform != "win32" and use_fork else "spawn")
    except Exception:
      self._ctx = mp.get_context()

  def run(
      self,
      program: str,
      function_to_run: str,
      test_input: Any,
      timeout_seconds: int = 30,
  ) -> tuple[Any, bool]:
    """Runs `function_to_run(test_input)` within an isolated process."""
    result_queue: mp.Queue = self._ctx.Queue()
    process = self._ctx.Process(
        target=_worker_target,
        args=(program, function_to_run, test_input, result_queue),
    )

    process.start()
    process.join(timeout=float(timeout_seconds))

    if process.is_alive():
      # Process timed out
      process.terminate()
      process.join(timeout=1.0)
      if process.is_alive():
        process.kill()
      return None, False

    if not result_queue.empty():
      output, success, err_msg = result_queue.get()
      if not success and err_msg:
        logging.debug(f"Execution failed: {err_msg}")
      return output, success

    return None, False
