import subprocess
import time
import json
import os
import glob
import re

SNAKEY_TEMPLATE = '''"""Snakey Achievement Game problem specification."""
import itertools
import numpy as np

_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]

def _get_board_shapes(radius: int = 4):
  orientations = set()
  for rot in range(4):
    for ref in range(2):
      s = _BASE_SNAKY
      if ref:
        s = [(-p[0], p[1]) for p in s]
      for _ in range(rot):
        s = [(p[1], -p[0]) for p in s]
      mx = min(p[0] for p in s)
      my = min(p[1] for p in s)
      normalized = tuple(sorted((p[0] - mx, p[1] - my) for p in s))
      orientations.add(normalized)

  shapes = []
  for ori in orientations:
    for dx in range(-radius, radius + 1):
      for dy in range(-radius, radius + 1):
        translated = tuple(sorted((x + dx, y + dy) for x, y in ori))
        if all(-radius <= x <= radius and -radius <= y <= radius for x, y in translated):
          shapes.append(frozenset(translated))
  return list(set(shapes))

@funsearch.evolve
def priority(
    candidate: tuple[int, int],
    maker_cells: list[tuple[int, int]],
    breaker_cells: list[tuple[int, int]],
    active_shapes: list[tuple[tuple[int, int], ...]],
) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  weights = {0: 1.0, 1: 4.1, 2: 26.9, 3: 507.8, 4: 25000.0, 5: 1000000.0}
  score = 0.0
  active_count = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += weights.get(m_cnt, 10.0 ** m_cnt)
      active_count += 1
  score += (active_count ** 1.3) * 2.97
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.08
  return float(score)

@funsearch.run
def evaluate(grid_radius: int) -> float:
  all_shapes = _get_board_shapes(radius=grid_radius)
  
  total_score = 0.0
  
  def evolving_breaker(last_maker_move, m_cells, b_cells):
    m_set, b_set = set(m_cells), set(b_cells)
    active = [s for s in all_shapes if not (s & b_set)]
    if not active:
        return (999, 999)
        
    candidates = set()
    for s in active:
      for p in s:
        if p not in m_set and p not in b_set:
          candidates.add(p)
          
    if not candidates:
        return (999, 999)
        
{breaker_strategy_indented}

    return max(candidates, key=lambda c: breaker_priority(c, m_cells, b_cells, active))
    
  def checkerboard_breaker(last_maker_move, m_cells, b_cells):
    m_set, b_set = set(m_cells), set(b_cells)
    active = [s for s in all_shapes if not (s & b_set)]
    candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
    if not candidates: return (999, 999)
    def is_cb(p): return ((p[0] // 2) + (p[1] // 2)) % 2 == 0
    cb_cands = [c for c in candidates if is_cb(c)]
    if cb_cands:
      return max(cb_cands, key=lambda c: sum(1 for s in active if c in s))
    return max(candidates, key=lambda c: sum(1 for s in active if c in s))
    
  def one_look_ahead_breaker(last_maker_move, m_cells, b_cells):
    m_set, b_set = set(m_cells), set(b_cells)
    active = [s for s in all_shapes if not (s & b_set)]
    candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
    if not candidates: return (999, 999)
    for s in active:
      if sum(1 for p in s if p in m_set) == 5:
        for p in s:
          if p not in m_set and p not in b_set:
            return p
    return max(candidates, key=lambda c: sum(1 for s in active if c in s))
    
  def higher_topo_paving_breaker(last_maker_move, m_cells, b_cells):
    m_set, b_set = set(m_cells), set(b_cells)
    active = [s for s in all_shapes if not (s & b_set)]
    candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
    if not candidates: return (999, 999)
    def is_ht(p): return ((p[0] // 3) + (p[1] // 3)) % 2 == 0
    ht_cands = [c for c in candidates if is_ht(c)]
    if ht_cands:
      return max(ht_cands, key=lambda c: sum(1 for s in active if c in s))
    return max(candidates, key=lambda c: sum(1 for s in active if c in s))

  ensemble = [evolving_breaker, checkerboard_breaker, one_look_ahead_breaker, higher_topo_paving_breaker]
  for breaker_fn in ensemble:
    m_cells, b_cells = [], []
    maker_won = False
    
    max_turns = (2 * grid_radius + 1) ** 2 // 2 + 1
    for turn in range(max_turns):
      m_set = set(m_cells)
      b_set = set(b_cells)
      
      for s in all_shapes:
        if s.issubset(m_set):
          maker_won = True
          break
      if maker_won:
        break
        
      active = [tuple(s) for s in all_shapes if not (s & b_set)]
      if not active:
        break
        
      candidates = set()
      for s in active:
        for p in s:
          if p not in m_set and p not in b_set:
            candidates.add(p)
      if not candidates:
        break
        
      best_move = max(candidates, key=lambda c: priority(c, m_cells, b_cells, active))
      m_cells.append(best_move)
      
      b_move = breaker_fn(best_move, m_cells, b_cells)
      if b_move != (999, 999):
        b_cells.append(b_move)
        
    m_set = set(m_cells)
    max_cells_in_shape = max((len(s & m_set) for s in all_shapes), default=0)
    total_score += float(max_cells_in_shape * 10)
    if maker_won:
      total_score += 100.0 + (max_turns - turn) * 10.0

  return total_score / len(ensemble)
'''

SNAKEY_BREAKER_TEMPLATE = '''"""Snakey Breaker Evolution Game problem specification."""
import itertools
import numpy as np

_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]

def _get_board_shapes(radius: int = 4):
  orientations = set()
  for rot in range(4):
    for ref in range(2):
      s = _BASE_SNAKY
      if ref:
        s = [(-p[0], p[1]) for p in s]
      for _ in range(rot):
        s = [(p[1], -p[0]) for p in s]
      mx = min(p[0] for p in s)
      my = min(p[1] for p in s)
      normalized = tuple(sorted((p[0] - mx, p[1] - my) for p in s))
      orientations.add(normalized)

  shapes = []
  for ori in orientations:
    for dx in range(-radius, radius + 1):
      for dy in range(-radius, radius + 1):
        translated = tuple(sorted((x + dx, y + dy) for x, y in ori))
        if all(-radius <= x <= radius and -radius <= y <= radius for x, y in translated):
          shapes.append(frozenset(translated))
  return list(set(shapes))

@funsearch.evolve
def breaker_priority(
    candidate: tuple[int, int],
    maker_cells: list[tuple[int, int]],
    breaker_cells: list[tuple[int, int]],
    active_shapes: list[tuple[tuple[int, int], ...]],
) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_count = sum(1 for p in shape if p in m_set)
      score += float(10 ** m_count)
  return score

@funsearch.run
def evaluate(grid_radius: int) -> float:
  all_shapes = _get_board_shapes(radius=grid_radius)
  
  total_score = 0.0
  
  def elite_maker(m_cells, b_cells, active):
    m_set, b_set = set(m_cells), set(b_cells)
    candidates = set()
    for s in active:
      for p in s:
        if p not in m_set and p not in b_set:
          candidates.add(p)
          
    if not candidates:
        return (999, 999)
        
{maker_strategy_indented}

    return max(candidates, key=lambda c: priority(c, m_cells, b_cells, active))

  def checkerboard_maker(m_cells, b_cells, active):
    m_set, b_set = set(m_cells), set(b_cells)
    candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
    if not candidates: return (999, 999)
    def is_cb(p): return ((p[0] // 2) + (p[1] // 2)) % 2 == 0
    cb_cands = [c for c in candidates if is_cb(c)]
    if cb_cands:
      return max(cb_cands, key=lambda c: sum(1 for s in active if c in s))
    return max(candidates, key=lambda c: sum(1 for s in active if c in s))
    
  def one_look_ahead_maker(m_cells, b_cells, active):
    m_set, b_set = set(m_cells), set(b_cells)
    candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
    if not candidates: return (999, 999)
    for s in active:
      if sum(1 for p in s if p in m_set) == 5:
        for p in s:
          if p not in m_set and p not in b_set:
            return p
    return max(candidates, key=lambda c: sum(1 for s in active if c in s))
    
  def higher_topo_paving_maker(m_cells, b_cells, active):
    m_set, b_set = set(m_cells), set(b_cells)
    candidates = [p for s in active for p in s if p not in m_set and p not in b_set]
    if not candidates: return (999, 999)
    def is_ht(p): return ((p[0] // 3) + (p[1] // 3)) % 2 == 0
    ht_cands = [c for c in candidates if is_ht(c)]
    if ht_cands:
      return max(ht_cands, key=lambda c: sum(1 for s in active if c in s))
    return max(candidates, key=lambda c: sum(1 for s in active if c in s))

  ensemble = [elite_maker, checkerboard_maker, one_look_ahead_maker, higher_topo_paving_maker]
  for maker_fn in ensemble:
    m_cells, b_cells = [], []
    maker_won = False
    
    max_turns = (2 * grid_radius + 1) ** 2 // 2 + 1
    for turn in range(max_turns):
      m_set = set(m_cells)
      b_set = set(b_cells)
      
      for s in all_shapes:
        if s.issubset(m_set):
          maker_won = True
          break
      if maker_won:
        break
        
      active = [tuple(s) for s in all_shapes if not (s & b_set)]
      if not active:
        break
        
      m_move = maker_fn(m_cells, b_cells, active)
      if m_move == (999, 999):
        break
      m_cells.append(m_move)
      m_set.add(m_move)
      
      for s in all_shapes:
        if s.issubset(m_set):
          maker_won = True
          break
      if maker_won:
        break
        
      active = [tuple(s) for s in all_shapes if not (s & b_set)]
      if not active:
        break
        
      candidates = set()
      for s in active:
        for p in s:
          if p not in m_set and p not in b_set:
            candidates.add(p)
      if not candidates:
        break
        
      best_move = max(candidates, key=lambda c: breaker_priority(c, m_cells, b_cells, active))
      b_cells.append(best_move)
        
    m_set = set(m_cells)
    
    if maker_won:
      total_score += float(turn * 10.0)
    else:
      max_cells_in_shape = max((len(s & m_set) for s in all_shapes), default=0)
      block_quality = (5 - max_cells_in_shape) * 100.0
      total_score += 1000.0 + block_quality + (max_turns - turn) * 10.0

  return total_score / len(ensemble)
'''

def format_func(func_code, indent_spaces=4):
    lines = func_code.strip().split('\n')
    indented = '\n'.join(' ' * indent_spaces + line for line in lines)
    return indented

def extract_function(file_path, func_name):
    with open(file_path, 'r') as f:
        content = f.read()
    
    match = re.search(r'def ' + func_name + r'\(.*?\).*?:\n(.*?)(\n@funsearch|\Z)', content, re.DOTALL)
    if match:
        body = match.group(1)
        idx = body.find('\ndef ')
        if idx != -1:
            body = body[:idx]
        
        full_func = f"def {func_name}(" + match.group().split(':\n')[0].split(f'def {func_name}(')[1] + ':\n' + body
        return full_func
    return None

def write_problem(spec_name, content):
    path = f"funsearch/problems/{spec_name}.py"
    with open(path, 'w') as f:
        f.write('"""Specification."""\nfrom __future__ import annotations\n\nSPECIFICATION = \'\'\'')
        f.write(content)
        f.write('\'\'\'\nINPUTS = [3, 4]\n')

def run_funsearch_until(problem, target_score):
    print(f"\n[{problem}] Starting mock funsearch (ensemble evaluation)...")
    start_time = time.time()
    
    existing_dirs = set(glob.glob(f"outputs/{problem}_*"))
    
    proc = subprocess.Popen(
        [".venv/bin/python", "-m", "funsearch.cli", "--problem", problem, "--model", "mock", "--iterations", "100", "--islands", "1", "--no-live"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    new_dir = None
    while proc.poll() is None:
        current_dirs = set(glob.glob(f"outputs/{problem}_*"))
        diff = current_dirs - existing_dirs
        if diff:
            new_dir = diff.pop()
            break
        time.sleep(1)
        
    if not new_dir:
        proc.kill()
        return None
        
    print(f"[{problem}] Monitoring {new_dir}/events.jsonl for ensemble average score >= {target_score}")
    
    events_file = f"{new_dir}/events.jsonl"
    
    while proc.poll() is None:
        if os.path.exists(events_file):
            with open(events_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    try:
                        data = json.loads(line.strip())
                        if data.get('score', 0) >= target_score:
                            print(f"[{problem}] Target score reached: {data['score']}!")
                            proc.kill()
                            time.sleep(1)
                            best_prog_path = f"{new_dir}/best_program.py"
                            if os.path.exists(best_prog_path):
                                return best_prog_path
                    except Exception:
                        pass
        time.sleep(0.5)
        
    print(f"[{problem}] Process ended before reaching target.")
    return None

current_maker = """def priority(
    candidate: tuple[int, int],
    maker_cells: list[tuple[int, int]],
    breaker_cells: list[tuple[int, int]],
    active_shapes: list[tuple[tuple[int, int], ...]],
) -> float:
    m_set = set(maker_cells)
    b_set = set(breaker_cells)
    weights = {0: 1.0, 1: 4.1, 2: 26.9, 3: 507.8, 4: 25000.0, 5: 1000000.0}
    score = 0.0
    active_count = 0
    for shape in active_shapes:
        if candidate in shape:
            m_cnt = sum(1 for p in shape if p in m_set)
            score += weights.get(m_cnt, 10.0 ** m_cnt)
            active_count += 1
    score += (active_count ** 1.3) * 2.97
    score -= (abs(candidate[0]) + abs(candidate[1])) * 0.08
    return float(score)"""

current_breaker = None

for i in range(1, 5):
    print(f"\n{'='*50}\n=== LEAD CHANGE {i} ===\n{'='*50}")
    
    if i % 2 == 1:
        print("Evolving BREAKER against Maker Ensemble...")
        spec = SNAKEY_BREAKER_TEMPLATE.replace("{maker_strategy_indented}", format_func(current_maker, 4))
        write_problem("snakey_breaker", spec)
        
        prog_path = run_funsearch_until("snakey_breaker", 1000.0)
        
        if prog_path:
            current_breaker = extract_function(prog_path, "breaker_priority")
            print("Successfully extracted new Breaker strategy!")
        else:
            print("Failed to evolve a winning Breaker.")
            break
            
    else:
        print("Evolving MAKER against Breaker Ensemble...")
        spec = SNAKEY_TEMPLATE.replace("{breaker_strategy_indented}", format_func(current_breaker, 4))
        write_problem("snakey", spec)
        
        prog_path = run_funsearch_until("snakey", 100.0)
        
        if prog_path:
            current_maker = extract_function(prog_path, "priority")
            print("Successfully extracted new Maker strategy!")
        else:
            print("Failed to evolve a winning Maker.")
            break

print("\n--- Final Co-Evolved Ensemble Maker Strategy ---")
print(current_maker)
