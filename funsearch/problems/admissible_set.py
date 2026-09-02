"""Admissible Set problem specification for FunSearch."""
from __future__ import annotations

SPECIFICATION = '''"""Admissible Set problem specification."""
import itertools
import numpy as np

@funsearch.evolve
def priority(w: tuple[int, ...], z: tuple[int, ...], n: int) -> float:
  """Returns the priority with which to add pair (w, z) to the admissible set."""
  # Baseline heuristic
  return -float(sum(w) + sum(z))

@funsearch.run
def evaluate(n: int) -> int:
  """Greedily builds an admissible set in (Z_3)^n x (Z_3)^n and returns its size."""
  all_vecs = list(itertools.product(range(3), repeat=n))
  pairs = []
  for w in all_vecs:
    for z in all_vecs:
      # Filter for valid pairs where sum(w_i * z_i) != 0 mod 3 or disjoint support
      if any((w[i] != 0 and z[i] != 0 and w[i] == z[i]) for i in range(n)):
        continue
      pairs.append((w, z))

  priorities = [priority(w, z, n) for w, z in pairs]
  sorted_indices = np.argsort(priorities)[::-1]
  
  admissible_set = []
  for idx in sorted_indices:
    cand_w, cand_z = pairs[idx]
    # Check admissible condition against all already chosen pairs
    valid = True
    for w, z in admissible_set:
      # Check condition: for any two distinct pairs (w_i, z_i) and (w_j, z_j), w_i + z_j != 0 mod 3
      diff1 = all((cand_w[k] + z[k]) % 3 == 0 for k in range(n))
      diff2 = all((w[k] + cand_z[k]) % 3 == 0 for k in range(n))
      if diff1 or diff2:
        valid = False
        break
    if valid:
      admissible_set.append((cand_w, cand_z))
      
  return len(admissible_set)
'''

INPUTS = [2, 3]
