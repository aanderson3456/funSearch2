"""Tools for manipulating Python code via AST.

Implements two primary representations:
- Function: encapsulates name, args, body, return_type, and docstring.
- Program: encapsulates a preface (imports/globals) and a sequence of Functions.
"""
from __future__ import annotations

import ast
from collections.abc import Iterator, MutableSet, Sequence
import dataclasses
import io
import tokenize
from typing import Any


@dataclasses.dataclass
class Function:
  """A parsed Python function."""

  name: str
  args: str
  body: str
  return_type: str | None = None
  docstring: str | None = None

  def __str__(self) -> str:
    return_type = f' -> {self.return_type}' if self.return_type else ''
    function = f'def {self.name}({self.args}){return_type}:\n'
    if self.docstring:
      new_line = '\n' if self.body else ''
      function += f'  """{self.docstring}"""{new_line}'
    # Guarantee proper indentation for every line in the function body
    body_lines = []
    for line in self.body.splitlines():
      if line.strip():
        if not line.startswith((' ', '\t')):
          body_lines.append('  ' + line)
        else:
          body_lines.append(line)
      else:
        body_lines.append('')
    body_str = '\n'.join(body_lines)
    function += body_str + '\n\n'
    return function

  def __setattr__(self, name: str, value: Any) -> None:
    if name == 'body' and isinstance(value, str):
      value = value.strip('\n')
    if name == 'docstring' and value is not None and isinstance(value, str):
      if '"""' in value:
        value = value.strip().replace('"""', '')
    super().__setattr__(name, value)


@dataclasses.dataclass
class Program:
  """A parsed Python program."""

  preface: str
  functions: list[Function]

  def __str__(self) -> str:
    program = f'{self.preface}\n' if self.preface else ''
    program += '\n'.join([str(f) for f in self.functions])
    return program

  def find_function_index(self, function_name: str) -> int:
    """Returns the index of input function name."""
    function_names = [f.name for f in self.functions]
    count = function_names.count(function_name)
    if count == 0:
      raise ValueError(
          f'function {function_name} does not exist in program:\n{str(self)}'
      )
    if count > 1:
      raise ValueError(
          f'function {function_name} exists more than once in program:\n'
          f'{str(self)}'
      )
    return function_names.index(function_name)

  def get_function(self, function_name: str) -> Function:
    index = self.find_function_index(function_name)
    return self.functions[index]


def text_to_program(text: str) -> Program:
  """Converts a Python source text into a Program object."""
  tree = ast.parse(text)
  lines = text.splitlines()
  
  functions: list[Function] = []
  first_func_line: int | None = None
  
  for node in tree.body:
    if isinstance(node, ast.FunctionDef):
      if first_func_line is None:
        first_func_line = node.lineno
      
      args_match = ast.unparse(node.args)
      docstring = ast.get_docstring(node)
      
      # Extract body lines
      body_start = node.body[0].lineno if node.body else node.lineno
      if docstring and len(node.body) > 1:
        body_start = node.body[1].lineno

      end_lineno = getattr(node, 'end_lineno', len(lines))
      if (
          docstring
          and len(node.body) == 1
          and isinstance(node.body[0], ast.Expr)
          and isinstance(node.body[0].value, ast.Constant)
      ):
        body_str = "  pass"
      else:
        body_lines = lines[body_start - 1 : end_lineno]
        body_str = '\n'.join(body_lines)

      return_type = None
      if node.returns:
        return_type = ast.unparse(node.returns)

      functions.append(
          Function(
              name=node.name,
              args=args_match,
              body=body_str,
              return_type=return_type,
              docstring=docstring,
          )
      )

  if first_func_line is not None and first_func_line > 1:
    preface = '\n'.join(lines[: first_func_line - 1])
  else:
    preface = ''

  return Program(preface=preface.strip(), functions=functions)


def text_to_function(text: str) -> Function:
  """Parses a single function definition."""
  program = text_to_program(text)
  if len(program.functions) != 1:
    raise ValueError(f'Expected exactly 1 function, got {len(program.functions)}')
  return program.functions[0]


def yield_decorated(
    specification: str, module_name: str, decorator_name: str
) -> Iterator[str]:
  """Yields function names with `@module_name.decorator_name` decorator."""
  tree = ast.parse(specification)
  for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
      for decorator in node.decorator_list:
        if isinstance(decorator, ast.Attribute):
          if (
              isinstance(decorator.value, ast.Name)
              and decorator.value.id == module_name
              and decorator.attr == decorator_name
          ):
            yield node.name
        elif isinstance(decorator, ast.Name) and decorator.id == decorator_name:
          yield node.name


def rename_function_calls(code: str, old_name: str, new_name: str) -> str:
  """Renames function calls within a body of code."""
  try:
    tree = ast.parse(code)
  except SyntaxError:
    return code.replace(old_name, new_name)

  class CallRenamer(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call) -> ast.AST:
      if isinstance(node.func, ast.Name) and node.func.id == old_name:
        node.func.id = new_name
      self.generic_visit(node)
      return node

  renamer = CallRenamer()
  new_tree = renamer.visit(tree)
  ast.fix_missing_locations(new_tree)
  return ast.unparse(new_tree)


def get_functions_called(code: str) -> list[str]:
  """Returns names of all functions called within code."""
  try:
    tree = ast.parse(code)
  except SyntaxError:
    return []

  called = []
  for node in ast.walk(tree):
    if isinstance(node, ast.Call):
      if isinstance(node.func, ast.Name):
        called.append(node.func.id)
      elif isinstance(node.func, ast.Attribute):
        called.append(node.func.attr)
  return called
