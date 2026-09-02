"""Online 1D Bin Packing problem specification for FunSearch."""
from __future__ import annotations

SPECIFICATION = '''"""Online 1D Bin Packing problem specification."""
import numpy as np

@funsearch.evolve
def priority(item: float, remaining_capacities: list[float]) -> list[float]:
  """Returns priorities for placing `item` into each available bin.
  
  Higher priority means the item is placed into that bin first.
  """
  # Baseline Best-Fit heuristic: maximize tightness / minimize remaining capacity after fit
  priorities = []
  for cap in remaining_capacities:
    if cap >= item:
      # Prioritize bin with least remaining space after placing item
      priorities.append(-(cap - item))
    else:
      priorities.append(-1e9)  # Infeasible
  return priorities

@funsearch.run
def evaluate(num_items: int) -> float:
  """Simulates online bin packing on a generated sequence of items and returns negative bins used."""
  # Seeded deterministic sequence of items for evaluation consistency
  rng = np.random.RandomState(42 + num_items)
  items = rng.uniform(0.1, 0.8, size=num_items).tolist()
  
  bin_capacities = [1.0]
  
  for item in items:
    priorities = priority(item, bin_capacities)
    best_bin_idx = int(np.argmax(priorities))
    
    if priorities[best_bin_idx] > -1e8 and bin_capacities[best_bin_idx] >= item:
      bin_capacities[best_bin_idx] -= item
    else:
      # Open a new bin
      bin_capacities.append(1.0 - item)
      
  # Objective: maximize negative number of bins (fewer bins is better)
  return -float(len(bin_capacities))
'''

INPUTS = [50, 100, 200]
