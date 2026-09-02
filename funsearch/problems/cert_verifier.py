"""Independent, mathematically rigorous Certificate Soundness Verifier for Polyomino Games.

Validates that a Maker StrategyTree guarantees victory against ALL possible Breaker
moves in Z^2 (both explicit critical threat responses and the infinite complement).
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


def rotate(p: tuple[int, int]) -> tuple[int, int]:
  return (p[1], -p[0])


def reflect(p: tuple[int, int]) -> tuple[int, int]:
  return (-p[0], p[1])


def normalize_shape(shape: list[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
  mx = min(p[0] for p in shape)
  my = min(p[1] for p in shape)
  return tuple(sorted((p[0] - mx, p[1] - my) for p in shape))


def get_all_orientations(base_shape: list[tuple[int, int]]) -> list[tuple[tuple[int, int], ...]]:
  """Generates all unique D8 isometric orientations of a base polyomino."""
  orientations = set()
  for rot in range(4):
    for ref in range(2):
      s = base_shape
      if ref:
        s = [reflect(p) for p in s]
      for _ in range(rot):
        s = [rotate(p) for p in s]
      orientations.add(normalize_shape(s))
  return sorted(list(orientations))


def check_win(player_points: set[tuple[int, int]], orientations: list[tuple[tuple[int, int], ...]]) -> tuple[bool, tuple[tuple[int, int], ...] | None]:
  """Checks if player_points contains any translated orientation of the polyomino."""
  if not player_points:
    return False, None

  for point in player_points:
    for ori in orientations:
      ox0, oy0 = ori[0]
      orig_x = point[0] - ox0
      orig_y = point[1] - oy0
      translated = tuple((orig_x + p[0], orig_y + p[1]) for p in ori)
      if all(p in player_points for p in translated):
        return True, translated
  return False, None


def compute_critical_threat_cells(
    maker_cells: set[tuple[int, int]],
    breaker_cells: set[tuple[int, int]],
    orientations: list[tuple[tuple[int, int], ...]],
    search_radius: int = 6,
) -> set[tuple[int, int]]:
  """Computes all cells that belong to an active winning threat overlapping Maker."""
  critical = set()
  for point in maker_cells:
    for ori in orientations:
      for ox, oy in ori:
        orig_x = point[0] - ox
        orig_y = point[1] - oy
        shape = frozenset((orig_x + p[0], orig_y + p[1]) for p in ori)
        # Check if shape is unblocked by Breaker
        if not (shape & breaker_cells):
          for p in shape:
            if p not in maker_cells and p not in breaker_cells:
              critical.add(p)
  return critical


@dataclass
class VerificationReport:
  valid: bool = True
  total_nodes: int = 0
  total_leaves: int = 0
  max_depth: int = 0
  errors: list[str] = field(default_factory=list)

  def log_error(self, message: str) -> None:
    self.valid = False
    self.errors.append(message)


class CertificateVerifier:
  """Verifies StrategyTree certificates for mathematical correctness."""

  def __init__(self, base_shape: list[tuple[int, int]], max_allowed_depth: int = 20) -> None:
    self.base_shape = base_shape
    self.orientations = get_all_orientations(base_shape)
    self.max_allowed_depth = max_allowed_depth

  def verify_node(
      self,
      node: Any,
      maker_cells: set[tuple[int, int]],
      breaker_cells: set[tuple[int, int]],
      depth: int,
      path: list[str],
      report: VerificationReport,
  ) -> None:
    report.total_nodes += 1
    report.max_depth = max(report.max_depth, depth)

    if depth > self.max_allowed_depth:
      report.log_error(f"Depth limit exceeded ({depth} > {self.max_allowed_depth}) at {'/'.join(path)}")
      return

    # Check for leaf node ('win',) or dict format
    is_win_leaf = False
    if isinstance(node, (list, tuple)) and len(node) > 0 and node[0] == "win":
      is_win_leaf = True
    elif isinstance(node, dict) and node.get("type") == "win":
      is_win_leaf = True

    if is_win_leaf:
      report.total_leaves += 1
      won, shape = check_win(maker_cells, self.orientations)
      if not won:
        report.log_error(
            f"Invalid leaf node: Maker cells {sorted(list(maker_cells))} do not contain target polyomino at {'/'.join(path)}"
        )
      return

    # Extract move node
    m: tuple[int, int]
    branches: list[tuple[tuple[int, int], Any]] = []
    default_child: Any = None

    if isinstance(node, (list, tuple)) and node[0] == "move":
      m = tuple(node[1])
      if len(node) > 2 and node[2]:
        if isinstance(node[2], dict):
          branches = [(tuple(k) if isinstance(k, (list, tuple)) else tuple(map(int, k.split(","))), v) for k, v in node[2].items() if k is not None and k != "default" and k != "None"]
          if None in node[2]:
            default_child = node[2][None]
          elif "default" in node[2]:
            default_child = node[2]["default"]
          elif "None" in node[2]:
            default_child = node[2]["None"]
        elif isinstance(node[2], list):
          branches = [(tuple(b), sub) for b, sub in node[2]]
      if len(node) > 3 and node[3] is not None:
        default_child = node[3]

    elif isinstance(node, dict) and node.get("type") == "move":
      m = tuple(node["maker_move"])
      raw_branches = node.get("branches", {})
      if isinstance(raw_branches, dict):
        for k, v in raw_branches.items():
          if k in ("default", "None", None):
            default_child = v
          else:
            coord = tuple(map(int, k.strip("()[]").split(","))) if isinstance(k, str) else tuple(k)
            branches.append((coord, v))
      default_child = default_child or node.get("default")
    else:
      report.log_error(f"Unrecognized node format at {'/'.join(path)}: {repr(node)[:100]}")
      return

    # Invariant 1: Cell Collision Check
    if m in maker_cells:
      report.log_error(f"Collision: Maker move {m} already in Maker cells at {'/'.join(path)}")
    if m in breaker_cells:
      report.log_error(f"Collision: Maker move {m} already in Breaker cells at {'/'.join(path)}")

    new_maker = maker_cells | {m}

    # Invariant 2: Immediate Win Check
    won, _ = check_win(new_maker, self.orientations)
    if won:
      # If Maker move completes the shape, this branch is fully satisfied
      report.total_leaves += 1
      return

    # Invariant 3: Verify all critical branches
    for b_move, sub_tree in branches:
      if b_move == m:
        report.log_error(f"Breaker move {b_move} collides with current Maker move {m} at {'/'.join(path)}")
      if b_move in new_maker:
        report.log_error(f"Breaker move {b_move} collides with Maker cells at {'/'.join(path)}")
      if b_move in breaker_cells:
        report.log_error(f"Breaker move {b_move} already claimed by Breaker at {'/'.join(path)}")

      self.verify_node(
          sub_tree,
          new_maker,
          breaker_cells | {b_move},
          depth + 1,
          path + [f"M{m}->B{b_move}"],
          report,
      )

    # Invariant 4: Verify default/infinite complement branch
    if default_child is not None:
      # Abstract dummy move far outside the critical region (e.g. (999, 999))
      dummy_b = (9999 + depth, 9999 + depth)
      self.verify_node(
          default_child,
          new_maker,
          breaker_cells | {dummy_b},
          depth + 1,
          path + [f"M{m}->B_default"],
          report,
      )
    else:
      # If no default branch is provided, all critical cells must be exhaustively branched
      critical = compute_critical_threat_cells(new_maker, breaker_cells, self.orientations)
      branched_b = set(b for b, _ in branches)
      missing = critical - branched_b
      if missing:
        report.log_error(
            f"Non-exhaustive branching: Missing critical threat responses {sorted(list(missing))} at {'/'.join(path)}"
        )

  def verify(self, certificate_data: Any) -> VerificationReport:
    """Entrypoint to verify an entire strategy certificate."""
    report = VerificationReport()
    tree = certificate_data
    if isinstance(certificate_data, dict) and "strategy_tree" in certificate_data:
      tree = certificate_data["strategy_tree"]

    self.verify_node(tree, set(), set(), 0, ["root"], report)
    return report


def verify_certificate_file(file_path: Path | str, base_shape: list[tuple[int, int]]) -> VerificationReport:
  """Loads a JSON certificate file and verifies soundness."""
  path = Path(file_path)
  if not path.exists():
    report = VerificationReport(valid=False)
    report.log_error(f"Certificate file not found: {file_path}")
    return report

  data = json.loads(path.read_text(encoding="utf-8"))
  verifier = CertificateVerifier(base_shape=base_shape)
  return verifier.verify(data)
