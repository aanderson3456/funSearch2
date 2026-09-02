"""Unit tests for ProcessSandbox and Evaluator."""
import pytest
from funsearch.sandbox.base import trim_function_body
from funsearch.sandbox.process_sandbox import ProcessSandbox


def test_trim_function_body():
  raw_code = """  x = 10
  return x * 2

def extra_function():
  pass
"""
  trimmed = trim_function_body(raw_code)
  assert "x = 10" in trimmed
  assert "extra_function" not in trimmed


def test_process_sandbox_success():
  sandbox = ProcessSandbox()
  code = """
def test_fn(x):
  return x ** 2
"""
  res, ok = sandbox.run(code, "test_fn", 5, timeout_seconds=5)
  assert ok is True
  assert res == 25


def test_process_sandbox_timeout():
  sandbox = ProcessSandbox()
  code = """
import time
def infinite_fn(x):
  while True:
    time.sleep(0.1)
  return x
"""
  res, ok = sandbox.run(code, "infinite_fn", 1, timeout_seconds=1)
  assert ok is False
  assert res is None


def test_process_sandbox_exception():
  sandbox = ProcessSandbox()
  code = """
def bad_fn(x):
  raise ValueError("Bad test")
"""
  res, ok = sandbox.run(code, "bad_fn", 1, timeout_seconds=5)
  assert ok is False
  assert res is None
