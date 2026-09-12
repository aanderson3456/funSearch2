import sys
import torch
import numpy as np
import json
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "big_nn"))
from resnet import SnakyNet
from mcts import MCTS
from env import SnakyEnv
from generate_html import make_html

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

mcts_cache = {}

def neural_net_priority(candidate, maker_cells, breaker_cells, active_shapes, role, model, device, num_searches=100):
    state_key = (frozenset(maker_cells), frozenset(breaker_cells), role)
    if state_key not in mcts_cache:
        env = SnakyEnv(size=13)
        for x, y in maker_cells:
            env.maker_board |= (1 << ((y+6) * 13 + (x+6)))
        for x, y in breaker_cells:
            env.breaker_board |= (1 << ((y+6) * 13 + (x+6)))
        env.current_player = role
        
        mcts = MCTS(model, num_searches=num_searches, device=device)
        mcts_cache[state_key] = mcts.search(env, add_noise=False)
        
    action_probs = mcts_cache[state_key]
    idx = (candidate[1]+6) * 13 + (candidate[0]+6)
    return float(action_probs[idx])

def play_match(maker_strat, breaker_strat):
    m_cells, b_cells = [], []
    maker_won = False
    trace = []
    winning_shape = None
    
    for turn in range(85): # Max ~84 moves per player on 13x13
        print(f"\rMatch turn {turn+1}...", end="", flush=True)
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

        m_set = set(m_cells)
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
            
        best_b_move = max(candidates, key=lambda c: breaker_strat(c, m_cells, b_cells, active))
        b_cells.append(best_b_move)
        trace.append({"turn": turn+1, "player": "breaker", "move": [best_b_move[0], best_b_move[1]]})

    print(f"\nMatch finished! Maker won: {maker_won} in {len(m_cells)} turns.")
    return trace, winning_shape

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")
    
    print("Loading models...")
    model_450 = SnakyNet(in_channels=3, num_resBlocks=16, num_channels=256, board_size=13).to(device)
    model_450.load_state_dict(torch.load("snaky_large_model_it450.pt", map_location=device, weights_only=True))
    model_450.eval()
    
    model_360 = SnakyNet(in_channels=3, num_resBlocks=16, num_channels=256, board_size=13).to(device)
    model_360.load_state_dict(torch.load("snaky_large_model_it360.pt", map_location=device, weights_only=True))
    model_360.eval()

    print("\nMatch: Maker (450) vs Breaker (360)")
    global mcts_cache
    mcts_cache = {}
    trace1, shape1 = play_match(
        lambda c, m, b, a: neural_net_priority(c, m, b, a, 1, model_450, device),
        lambda c, m, b, a: neural_net_priority(c, m, b, a, -1, model_360, device)
    )
    with open("arena_450_vs_360_trace.json", "w") as f:
        json.dump({"trace": trace1, "winningShape": shape1}, f)
    make_html("arena_450_vs_360_trace.json", "arena_450_vs_360_replay.html", title="Snaky Match: Maker (450) vs Breaker (360)")
    
    print("\nMatch: Maker (360) vs Breaker (450)")
    mcts_cache = {}
    trace2, shape2 = play_match(
        lambda c, m, b, a: neural_net_priority(c, m, b, a, 1, model_360, device),
        lambda c, m, b, a: neural_net_priority(c, m, b, a, -1, model_450, device)
    )
    with open("arena_360_vs_450_trace.json", "w") as f:
        json.dump({"trace": trace2, "winningShape": shape2}, f)
    make_html("arena_360_vs_450_trace.json", "arena_360_vs_450_replay.html", title="Snaky Match: Maker (360) vs Breaker (450)")
    
    print("Matches finished and replays generated.")

if __name__ == "__main__":
    main()
