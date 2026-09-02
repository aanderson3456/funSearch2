"""Cap Set problem specification for FunSearch."""
from __future__ import annotations

SPECIFICATION = '''"""Cap Set problem specification in (Z_3)^n."""
import itertools
import numpy as np

@funsearch.evolve
def priority(el: tuple[int, ...], n: int) -> float:
  """Returns the priority with which to add element `el` to the cap set."""
  # Initial baseline: simple linear norm
  return -float(sum(el))

@funsearch.run
def evaluate(n: int) -> int:
  """Constructs a cap set greedily according to `priority` and returns its size."""
  # Generate all elements of (Z_3)^n
  elements = list(itertools.product(range(3), repeat=n))
  
  # Compute priorities
  priorities = [priority(el, n) for el in elements]
  
  # Sort elements by descending priority
  sorted_indices = np.argsort(priorities)[::-1]
  sorted_elements = [elements[i] for i in sorted_indices]
  
  cap_set = []
  cap_set_lookup = set()
  
  for el in sorted_elements:
    # Check if adding `el` would create a 3-element arithmetic progression with existing points
    # In Z_3, x + y + z = 0 mod 3 <=> z = (-x - y) mod 3 = (2x + 2y) mod 3
    valid = True
    for other in cap_set:
      third = tuple((3 - (el[i] + other[i]) % 3) % 3 for i in range(n))
      if third in cap_set_lookup:
        valid = False
        break
    if valid:
      cap_set.append(el)
      cap_set_lookup.add(el)
      
  return len(cap_set)
'''

# Standard dimensions to evaluate on (e.g. n=3, 4, 5 for fast/standard runs)
INPUTS = [3, 4, 5]
