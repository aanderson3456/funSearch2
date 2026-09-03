import sys
import torch
import numpy as np

# Bring in the baby AlphaGo code
sys.path.append("/Users/austinanderson/AngularMathgod/mathgod/snakey-api/baby_alphago")
from resnet import SnakyNet
from env import SnakyEnv
from mcts import MCTS

# FunSearch 8x8 Board shapes helper (radius=4 gives roughly an 8x8 grid bounds logic)
_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]
def _get_board_shapes_8x8():
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
    for dx in range(8):
      for dy in range(8):
        translated = tuple(sorted((x + dx, y + dy) for x, y in ori))
        if all(0 <= x < 8 and 0 <= y < 8 for x, y in translated):
          shapes.append(frozenset(translated))
  return list(set(shapes))

ALL_SHAPES_8X8 = _get_board_shapes_8x8()

# --- Example Weak Evolved Maker ---
def weak_maker_priority(candidate, maker_cells, breaker_cells, active_shapes):
    m_set = set(maker_cells)
    score = 0.0
    for shape in active_shapes:
        if candidate in shape:
            m_cnt = sum(1 for p in shape if p in m_set)
            score += float(6.6 ** m_cnt)
    dist_sq = (candidate[0]-3.5) ** 2 + (candidate[1]-3.5) ** 2
    score -= dist_sq * 0.0291
    return float(score)

# --- Neural Network Strategy Wrapper ---
def neural_net_priority(candidate, maker_cells, breaker_cells, active_shapes, role, model, device):
    """
    Role: 1 for Maker, -1 for Breaker
    Instead of using MCTS for every move (which is slow), we'll just use the raw policy network.
    """
    state = np.zeros((3, 8, 8), dtype=np.float32)
    for (x, y) in maker_cells:
        state[0, y, x] = 1.0
    for (x, y) in breaker_cells:
        state[1, y, x] = 1.0
        
    if role == 1:
        state[2, :, :] = 1.0
    else:
        state[2, :, :] = 0.0
        
    state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    with torch.no_grad():
        policy_logits, _ = model(state_tensor)
        policy = torch.nn.functional.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy()
        
    # The network outputs 64 probabilities (8x8)
    idx = candidate[1] * 8 + candidate[0]
    return float(policy[idx])

def play_match(maker_strat, breaker_strat):
    m_cells, b_cells = [], []
    maker_won = False
    trace = []
    winning_shape = None
    
    for turn in range(32): # Max 32 moves per player on an 8x8 board
        m_set, b_set = set(m_cells), set(b_cells)
        
        # Check Maker Win
        for s in ALL_SHAPES_8X8:
            if s.issubset(m_set):
                maker_won = True
                winning_shape = list(s)
                break
        if maker_won:
            break
            
        active = [s for s in ALL_SHAPES_8X8 if not (s & b_set)]
        if not active:
            break # Breaker successfully blocked all shapes
            
        candidates = set()
        for s in active:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates.add(p)
        if not candidates:
            break
            
        best_m_move = max(candidates, key=lambda c: maker_strat(c, m_cells, b_cells, active))
        m_cells.append(best_m_move)
        m_set.add(best_m_move)
        trace.append({"turn": turn+1, "player": "maker", "move": [best_m_move[0], best_m_move[1]]})
        
        # Check Maker Win immediately after move
        for s in ALL_SHAPES_8X8:
            if s.issubset(m_set):
                maker_won = True
                winning_shape = list(s)
                break
        if maker_won:
            break
            
        # Breaker turn
        active_for_breaker = [s for s in ALL_SHAPES_8X8 if not (s & b_set)]
        candidates_b = set()
        for s in active_for_breaker:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates_b.add(p)
                    
        if not candidates_b:
            break
            
        b_move = max(candidates_b, key=lambda c: breaker_strat(c, m_cells, b_cells, active_for_breaker))
        b_cells.append(b_move)
        trace.append({"turn": turn+1, "player": "breaker", "move": [b_move[0], b_move[1]]})

    return maker_won, len(m_cells), trace, winning_shape

if __name__ == "__main__":
    device = "cpu"
    print("Loading Neural Network...")
    model = SnakyNet(board_size=8).to(device)
    model.load_state_dict(torch.load("/Users/austinanderson/AngularMathgod/mathgod/snakey-api/baby_alphago/snaky_model_it2.pt", map_location=device, weights_only=True))
    model.eval()
    
    print("Playing Match 1: Maker (NN) vs Breaker (Heuristic)")
    maker_strat = lambda c, m, b, a: neural_net_priority(c, m, b, a, 1, model, device)
    breaker_strat = lambda c, m, b, a: -weak_maker_priority(c, b, m, a) # Reusing maker logic with swapped sets
    
    m_won, turns, t1, w1 = play_match(maker_strat, breaker_strat)
    print(f"Result: {'Maker (NN)' if m_won else 'Breaker (Heuristic)'} won in {turns} turns.\n")
    
    print("Playing Match 2: Maker (Heuristic) vs Breaker (NN)")
    maker_strat2 = lambda c, m, b, a: weak_maker_priority(c, m, b, a)
    breaker_strat2 = lambda c, m, b, a: neural_net_priority(c, m, b, a, -1, model, device)
    
    m_won2, turns2, t2, w2 = play_match(maker_strat2, breaker_strat2)
    print(f"Result: {'Maker (Heuristic)' if m_won2 else 'Breaker (NN)'} won in {turns2} turns.")
    
    import json
    with open("arena_8x8_trace.json", "w") as f:
        json.dump({"trace": t2, "winningShape": w2}, f)

