import sys
import torch
import numpy as np
import json

sys.path.append("/Users/austinanderson/GitHub/FunSizzy/FS2/big_nn")
from resnet import SnakyNet

# 13x13 Board shapes helper (radius=6)
_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]
def _get_board_shapes(radius: int=6):
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

ALL_SHAPES_13X13 = _get_board_shapes(radius=6)

# --- Load Evolved FunSearch Maker ---
with open("co_evolve_champions/maker_top_1_score_112.py", "r") as f:
    maker_src = f.read()
    
# Clean up header comments
lines = [l for l in maker_src.split("\n") if not l.startswith("#")]
maker_src = "\n".join(lines)
maker_namespace = {}
exec(maker_src, maker_namespace)
evolved_maker_priority = maker_namespace["priority"]

# --- Neural Network Strategy Wrapper ---
def neural_net_priority(candidate, maker_cells, breaker_cells, active_shapes, role, model, device):
    state = np.zeros((3, 13, 13), dtype=np.float32)
    for (x, y) in maker_cells:
        state[0, y+6, x+6] = 1.0
    for (x, y) in breaker_cells:
        state[1, y+6, x+6] = 1.0
        
    if role == 1:
        state[2, :, :] = 1.0
    else:
        state[2, :, :] = 0.0
        
    state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    with torch.no_grad():
        policy_logits, _ = model(state_tensor)
        policy = torch.nn.functional.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy()
        
    idx = (candidate[1]+6) * 13 + (candidate[0]+6)
    return float(policy[idx])

def play_match(maker_strat, breaker_strat):
    m_cells, b_cells = [], []
    maker_won = False
    trace = []
    winning_shape = None
    
    for turn in range(85): # Max ~84 moves per player on 13x13
        m_set, b_set = set(m_cells), set(b_cells)
        
        for s in ALL_SHAPES_13X13:
            if s.issubset(m_set):
                maker_won = True
                winning_shape = list(s)
                break
        if maker_won: break
            
        active = [s for s in ALL_SHAPES_13X13 if not (s & b_set)]
        if not active: break 
            
        candidates = set()
        for s in active:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates.add(p)
        if not candidates: break
            
        best_m_move = max(candidates, key=lambda c: maker_strat(c, m_cells, b_cells, active))
        m_cells.append(best_m_move)
        m_set.add(best_m_move)
        trace.append({"turn": turn+1, "player": "maker", "move": [best_m_move[0], best_m_move[1]]})
        
        for s in ALL_SHAPES_13X13:
            if s.issubset(m_set):
                maker_won = True
                winning_shape = list(s)
                break
        if maker_won: break
            
        active_for_breaker = [s for s in ALL_SHAPES_13X13 if not (s & b_set)]
        candidates_b = set()
        for s in active_for_breaker:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates_b.add(p)
                    
        if not candidates_b: break
            
        b_move = max(candidates_b, key=lambda c: breaker_strat(c, m_cells, b_cells, active_for_breaker))
        b_cells.append(b_move)
        trace.append({"turn": turn+1, "player": "breaker", "move": [b_move[0], b_move[1]]})

    return maker_won, len(m_cells), trace, winning_shape

if __name__ == "__main__":
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print("Loading 13x13 Massive Neural Network...")
    model = SnakyNet(num_resBlocks=16, num_channels=256, board_size=13).to(device)
    model.load_state_dict(torch.load("/Users/austinanderson/GitHub/FunSizzy/FS2/snaky_large_model_it2.pt", map_location=device, weights_only=True))
    model.eval()
    
    print("Playing Match: Maker (Top Evolved Heuristic) vs Breaker (Massive NN Policy)")
    maker_strat = lambda c, m, b, a: evolved_maker_priority(c, m, b, a)
    breaker_strat = lambda c, m, b, a: neural_net_priority(c, m, b, a, -1, model, device)
    
    m_won, turns, t, w = play_match(maker_strat, breaker_strat)
    print(f"Result: {'Maker (Heuristic)' if m_won else 'Breaker (NN)'} won in {turns} turns.")
    
    with open("arena_13x13_trace.json", "w") as f:
        json.dump({"trace": t, "winningShape": w}, f)
