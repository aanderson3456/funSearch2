"""Unit and soundness tests for 5-Straightomino (I5) and Certificate Verifier."""
from __future__ import annotations

import pytest

from funsearch.core.code_manipulation import text_to_program
from funsearch.problems.cert_solver import StrategyTreeSolver, POLYOMINO_SHAPES
from funsearch.problems.cert_verifier import CertificateVerifier, get_all_orientations, check_win
from funsearch.problems.straightomino import SPECIFICATION


def test_straightomino_specification():
  """Tests that straightomino specification parses cleanly."""
  program = text_to_program(SPECIFICATION)
  assert "priority" in [f.name for f in program.functions]
  assert "evaluate" in [f.name for f in program.functions]


def test_domino_cert_solving_and_verification():
  """Solves domino and verifies sound certificate."""
  base_shape = POLYOMINO_SHAPES["domino"]
  solver = StrategyTreeSolver(base_shape=base_shape, grid_radius=2, max_depth=4)
  cert = solver.generate_certificate()
  assert cert is not None

  verifier = CertificateVerifier(base_shape=base_shape)
  report = verifier.verify(cert)
  assert report.valid is True
  assert report.total_nodes > 0
  assert len(report.errors) == 0


def test_i4_cert_solving_and_verification():
  """Solves I4 (4-straightomino) and verifies sound certificate."""
  base_shape = POLYOMINO_SHAPES["i4"]
  solver = StrategyTreeSolver(base_shape=base_shape, grid_radius=3, max_depth=6, max_branching=4)
  cert = solver.generate_certificate()
  assert cert is not None

  verifier = CertificateVerifier(base_shape=base_shape)
  report = verifier.verify(cert)
  assert report.valid is True
  assert report.total_nodes > 0
  assert len(report.errors) == 0


def test_cert_verifier_rejects_invalid_leaf():
  """Ensures verifier rejects a tree claiming win when Maker does not have the shape."""
  base_shape = [(0, 0), (1, 0), (2, 0)]  # 3-straight
  # Fraudulent tree: Maker plays (0,0), (1,0) and claims win without (2,0)
  bad_tree = ("move", (0, 0), [], ("move", (1, 0), [], ("win",)))

  verifier = CertificateVerifier(base_shape=base_shape)
  report = verifier.verify({"strategy_tree": bad_tree})
  assert report.valid is False
  assert any("Invalid leaf node" in err for err in report.errors)


def test_cert_verifier_rejects_collision():
  """Ensures verifier rejects a tree where Maker plays on an occupied square."""
  base_shape = [(0, 0), (1, 0)]
  # Collision: Maker plays (0,0) twice
  bad_tree = ("move", (0, 0), [], ("move", (0, 0), [], ("win",)))

  verifier = CertificateVerifier(base_shape=base_shape)
  report = verifier.verify({"strategy_tree": bad_tree})
  assert report.valid is False
  assert any("Collision" in err for err in report.errors)


def test_cert_verifier_rejects_missing_critical_branches():
  """Ensures verifier rejects incomplete branching when no default branch exists."""
  base_shape = [(0, 0), (1, 0)]
  # Incomplete: Maker plays (0,0) and has no default branch and no critical branch
  bad_tree = ("move", (0, 0), [], None)

  verifier = CertificateVerifier(base_shape=base_shape)
  report = verifier.verify({"strategy_tree": bad_tree})
  assert report.valid is False
  assert any("Missing critical threat" in err for err in report.errors)
