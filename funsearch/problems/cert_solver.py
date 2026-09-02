"""Threat-Space Search (TSS) Strategy Tree Solver and Certificate Generator."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import time
from typing import Any

from funsearch.problems.cert_verifier import CertificateVerifier, get_all_orientations, check_win, compute_critical_threat_cells

# Predefined benchmark polyominoes
POLYOMINO_SHAPES: dict[str, list[tuple[int, int]]] = {
    "domino": [(0, 0), (1, 0)],
    "i4": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "i5": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    "straightomino": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    "snakey": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)],  # Numberphile / Sophie MacLean Step Snaky
    "snaky_s": [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (2, 3)],  # Symmetrical S-Hexomino
}


def get_board_shapes(base_shape: list[tuple[int, int]], radius: int = 4) -> list[frozenset[tuple[int, int]]]:
  """Generates all translations of all D8 orientations inside [-radius, radius]^2."""
  orientations = get_all_orientations(base_shape)
  shapes = []
  for ori in orientations:
    for dx in range(-radius, radius + 1):
      for dy in range(-radius, radius + 1):
        translated = tuple(sorted((x + dx, y + dy) for x, y in ori))
        if all(-radius <= x <= radius and -radius <= y <= radius for x, y in translated):
          shapes.append(frozenset(translated))
  return list(set(shapes))


class StrategyTreeSolver:
  """Threat-Space search solver for polyomino achievement games."""

  def __init__(
      self,
      base_shape: list[tuple[int, int]],
      grid_radius: int = 4,
      max_depth: int = 8,
      max_branching: int = 5,
  ) -> None:
    self.base_shape = base_shape
    self.grid_radius = grid_radius
    self.max_depth = max_depth
    self.max_branching = max_branching

    self.orientations = get_all_orientations(base_shape)
    self.all_shapes = get_board_shapes(base_shape, radius=grid_radius)
    self._memo: dict[tuple[frozenset[tuple[int, int]], frozenset[tuple[int, int]], int], Any] = {}

  def solve(
      self,
      maker_cells: list[tuple[int, int]],
      breaker_cells: list[tuple[int, int]],
      depth: int = 0,
  ) -> Any:
    """Recursive threat-space minimax search."""
    m_set = set(maker_cells)
    b_set = set(breaker_cells)

    won, _ = check_win(m_set, self.orientations)
    if won:
      return ("win",)

    if depth >= self.max_depth:
      return None

    # Memoization key: filter out abstract dummy moves > 500
    real_b = frozenset(p for p in breaker_cells if p[0] < 500)
    state_key = (frozenset(maker_cells), real_b, self.max_depth - depth)
    if state_key in self._memo:
      return self._memo[state_key]

    active = [s for s in self.all_shapes if not (s & b_set)]

    # 1. Immediate Win Check (1-threat)
    for s in active:
      diff = s - m_set
      if len(diff) == 1:
        t = list(diff)[0]
        res = ("move", t, [], ("win",))
        self._memo[state_key] = res
        return res

    # 2. Candidate Maker Moves
    candidates = set()
    if not maker_cells:
      candidates.add((0, 0))
    else:
      for s in active:
        if s & m_set:
          for p in s - m_set:
            candidates.add(p)

    if not candidates:
      self._memo[state_key] = None
      return None

    def move_score(p: tuple[int, int]) -> float:
      score = 0.0
      for s in active:
        if p in s:
          m_cnt = len(s & m_set)
          score += float(10 ** m_cnt)
      score -= (abs(p[0]) + abs(p[1])) * 0.1
      return score

    sorted_candidates = sorted(candidates, key=move_score, reverse=True)[: self.max_branching]

    for m in sorted_candidates:
      new_m = maker_cells + [m]
      new_m_set = set(new_m)

      # Check double-threat fork
      t1_after = []
      for s in active:
        diff = s - new_m_set
        if len(diff) == 1:
          t1_after.append(list(diff)[0])
      t1_after = list(set(t1_after))

      if len(t1_after) >= 2:
        tA, tB = t1_after[0], t1_after[1]
        res = ("move", m, [(tA, ("move", tB, [], ("win",)))], ("move", tA, [], ("win",)))
        self._memo[state_key] = res
        return res

      critical_b = set()
      for s in active:
        if m in s:
          for p in s:
            if p not in new_m_set and p not in b_set:
              critical_b.add(p)

      # Solve default infinite complement branch
      dummy_b = (999 + depth, 999 + depth)
      default_tree = self.solve(new_m, breaker_cells + [dummy_b], depth + 1)
      if default_tree is None:
        continue

      # Solve critical branches
      all_ok = True
      branches = []
      for b in sorted(critical_b):
        b_tree = self.solve(new_m, breaker_cells + [b], depth + 1)
        if b_tree is None:
          all_ok = False
          break
        branches.append((b, b_tree))

      if all_ok:
        res = ("move", m, branches, default_tree)
        self._memo[state_key] = res
        return res

    self._memo[state_key] = None
    return None

  def generate_certificate(self) -> dict[str, Any] | None:
    """Solves the game and returns a verified JSON certificate."""
    tree = self.solve([], [])
    if tree is None:
      return None

    cert_data = {
        "polyomino_base": [list(p) for p in self.base_shape],
        "grid_radius": self.grid_radius,
        "max_depth": self.max_depth,
        "strategy_tree": tree,
    }
    return cert_data


def main() -> None:
  parser = argparse.ArgumentParser(description="TSS Strategy Tree Solver & Certificate Generator.")
  parser.add_argument("--polyomino", type=str, default="i5", help="Target polyomino (domino, i4, i5, snakey).")
  parser.add_argument("--radius", type=int, default=4, help="Grid radius.")
  parser.add_argument("--depth", type=int, default=8, help="Max search depth in plies.")
  parser.add_argument("--output", type=str, default=None, help="Output JSON certificate file.")
  args = parser.parse_args()

  poly_key = args.polyomino.lower()
  if poly_key not in POLYOMINO_SHAPES:
    print(f"Unknown polyomino: {args.polyomino}. Available: {list(POLYOMINO_SHAPES.keys())}")
    return

  base_shape = POLYOMINO_SHAPES[poly_key]
  print(f"Solving {args.polyomino} with Threat-Space Search (radius={args.radius}, depth={args.depth})...")

  t0 = time.time()
  solver = StrategyTreeSolver(base_shape=base_shape, grid_radius=args.radius, max_depth=args.depth)
  cert = solver.generate_certificate()
  dt = time.time() - t0

  if cert:
    print(f"Solved successfully in {dt:.3f}s!")
    verifier = CertificateVerifier(base_shape=base_shape)
    report = verifier.verify(cert)
    print(f"Certificate Verification: Valid={report.valid}, Nodes={report.total_nodes}, Leaves={report.total_leaves}, MaxDepth={report.max_depth}")

    if args.output:
      out_path = Path(args.output)
      out_path.parent.mkdir(parents=True, exist_ok=True)
      out_path.write_text(json.dumps(cert, indent=2), encoding="utf-8")
      print(f"Saved certificate to {args.output}")
  else:
    print(f"Search exhausted after {dt:.3f}s: No winning strategy found within depth limit.")


if __name__ == "__main__":
  main()
