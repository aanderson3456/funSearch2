"""Sandbox execution environments and Evaluator classes for FunSearch."""

from funsearch.sandbox.base import Sandbox, Evaluator
from funsearch.sandbox.process_sandbox import ProcessSandbox
from funsearch.sandbox.in_process_sandbox import InProcessSandbox

__all__ = ["Sandbox", "Evaluator", "ProcessSandbox", "InProcessSandbox"]
