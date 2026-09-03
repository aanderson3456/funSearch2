import os
import sys
import time
import json
from pathlib import Path

# Add the project root to sys.path so we can import funsearch modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from funsearch.llm.mock import MockLLM

# Helper from funsearch
_BASE_SNAKY = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)]
def _get_board_shapes(radius: int=4):
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

def simulate(maker_func, breaker_func):
    all_shapes = _get_board_shapes(radius=6)
    m_cells, b_cells = [], []
    maker_won = False
    
    for turn in range(25):
        m_set, b_set = set(m_cells), set(b_cells)
        for s in all_shapes:
            if s.issubset(m_set):
                maker_won = True
                break
        if maker_won:
            break
            
        active = [s for s in all_shapes if not (s & b_set)]
        if not active:
            break
            
        candidates = set()
        for s in active:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates.add(p)
        if not candidates:
            break
            
        best_m_move = max(candidates, key=lambda c: maker_func(c, m_cells, b_cells, active))
        m_cells.append(best_m_move)
        
        m_set = set(m_cells)
        active_for_breaker = [s for s in all_shapes if not (s & b_set)]
        candidates_b = set()
        for s in active_for_breaker:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates_b.add(p)
                    
        if not candidates_b:
            break
            
        b_move = max(candidates_b, key=lambda c: breaker_func(c, m_cells, b_cells, active_for_breaker))
        b_cells.append(b_move)

    # Check one last time after breaker move
    m_set = set(m_cells)
    for s in all_shapes:
        if s.issubset(m_set):
            maker_won = True
            break

    return maker_won, len(m_cells)

def make_maker_func(body_str):
    code = "def priority(candidate, maker_cells, breaker_cells, active_shapes):\n" + body_str
    namespace = {}
    try:
        exec(code, namespace)
    except Exception as e:
        print("Error compiling maker func:", e)
        return None, None
    return namespace["priority"], code

def make_breaker_func(body_str):
    code = "def breaker_priority(candidate, maker_cells, breaker_cells, active_shapes):\n" + body_str
    namespace = {}
    try:
        exec(code, namespace)
    except Exception as e:
        print("Error compiling breaker func:", e)
        return None, None
    return namespace["breaker_priority"], code

def generate_mutations(llm, prompt, count):
    mutations = []
    for _ in range(count):
        body = llm.draw_sample(prompt)
        mutations.append(body)
    return mutations

def main():
    generations = 500
    k_mutations = 20
    
    llm = MockLLM()
    
    # Initialization: Draw random seeds
    maker_code = llm.draw_sample("def priority(candidate, maker_cells, breaker_cells, active_shapes):")
    reigning_maker_func, reigning_maker_src = make_maker_func(maker_code)
    
    breaker_code = llm.draw_sample("def breaker_priority(candidate, maker_cells, breaker_cells, active_shapes):")
    reigning_breaker_func, reigning_breaker_src = make_breaker_func(breaker_code)
    
    maker_survival_stats = []
    breaker_survival_stats = []
    
    current_maker_id = 0
    current_breaker_id = 0
    
    # Active champions' stats
    maker_mutations_defeated = 0
    maker_opponent_gens_survived = 0
    
    breaker_mutations_defeated = 0
    breaker_opponent_gens_survived = 0

    out_dir = Path("co_evolve_champions")
    out_dir.mkdir(exist_ok=True)
    
    print(f"Starting Co-Evolution for {generations} generations with {k_mutations} challengers per gen.")

    start_time = time.time()

    for gen in range(generations):
        # 1. Update Maker
        # Generate k mutant Makers
        maker_mutants_bodies = generate_mutations(llm, "def priority(candidate, maker_cells, breaker_cells, active_shapes):", k_mutations)
        best_maker_mutant = None
        best_maker_win_speed = 999
        
        for body in maker_mutants_bodies:
            m_func, m_src = make_maker_func(body)
            if not m_func: continue
            
            maker_won, turns = simulate(m_func, reigning_breaker_func)
            if maker_won:
                if turns < best_maker_win_speed:
                    best_maker_win_speed = turns
                    best_maker_mutant = (m_func, m_src)
            else:
                # Maker mutant failed to beat the current breaker. The breaker defeated this mutant!
                breaker_mutations_defeated += 1
        
        if best_maker_mutant:
            # A new maker dethroned the old one
            score = maker_mutations_defeated * maker_opponent_gens_survived
            if score > 0:
                maker_survival_stats.append({
                    "id": current_maker_id,
                    "mutations_defeated": maker_mutations_defeated,
                    "gens_survived": maker_opponent_gens_survived,
                    "longevity_score": score,
                    "src": reigning_maker_src
                })
            
            reigning_maker_func, reigning_maker_src = best_maker_mutant
            current_maker_id += 1
            maker_mutations_defeated = 0
            maker_opponent_gens_survived = 0
            
            # Since the breaker was beaten by a new maker, the breaker's reign over *generations* ends?
            # Actually, the breaker itself wasn't dethroned by a fellow breaker, it just met a better maker.
            # We'll just say the maker advanced.
        else:
            # Reigning maker survived all challenger mutations (meaning no challenger could beat the breaker)
            maker_mutations_defeated += k_mutations

        breaker_opponent_gens_survived += 1 # Breaker survived another Maker update cycle

        # 2. Update Breaker
        # Generate k mutant Breakers
        breaker_mutants_bodies = generate_mutations(llm, "def breaker_priority(candidate, maker_cells, breaker_cells, active_shapes):", k_mutations)
        best_breaker_mutant = None
        best_breaker_loss_delay = -1 # we want a breaker that PREVENTS the maker from winning (maker_won = False)
        
        for body in breaker_mutants_bodies:
            b_func, b_src = make_breaker_func(body)
            if not b_func: continue
            
            maker_won, turns = simulate(reigning_maker_func, b_func)
            if not maker_won:
                # Breaker won!
                if turns > best_breaker_loss_delay: # In a sense, it fully blocked. 
                    best_breaker_loss_delay = turns
                    best_breaker_mutant = (b_func, b_src)
            else:
                # Maker won anyway. The maker defeated this breaker mutant.
                maker_mutations_defeated += 1

        if best_breaker_mutant:
            # A new breaker dethroned the old one
            score = breaker_mutations_defeated * breaker_opponent_gens_survived
            if score > 0:
                breaker_survival_stats.append({
                    "id": current_breaker_id,
                    "mutations_defeated": breaker_mutations_defeated,
                    "gens_survived": breaker_opponent_gens_survived,
                    "longevity_score": score,
                    "src": reigning_breaker_src
                })
            
            reigning_breaker_func, reigning_breaker_src = best_breaker_mutant
            current_breaker_id += 1
            breaker_mutations_defeated = 0
            breaker_opponent_gens_survived = 0
        else:
            # Reigning breaker survived all challenger mutations
            breaker_mutations_defeated += k_mutations
            
        maker_opponent_gens_survived += 1 # Maker survived another Breaker update cycle
        
        if (gen + 1) % 50 == 0:
            print(f"Gen {gen + 1}/{generations} ... Elapsed: {time.time()-start_time:.1f}s")
            
    # Save the reigning ones at the end
    maker_score = maker_mutations_defeated * maker_opponent_gens_survived
    maker_survival_stats.append({
        "id": current_maker_id,
        "mutations_defeated": maker_mutations_defeated,
        "gens_survived": maker_opponent_gens_survived,
        "longevity_score": maker_score,
        "src": reigning_maker_src
    })
    
    breaker_score = breaker_mutations_defeated * breaker_opponent_gens_survived
    breaker_survival_stats.append({
        "id": current_breaker_id,
        "mutations_defeated": breaker_mutations_defeated,
        "gens_survived": breaker_opponent_gens_survived,
        "longevity_score": breaker_score,
        "src": reigning_breaker_src
    })

    # Output Rankings
    maker_survival_stats.sort(key=lambda x: x["longevity_score"], reverse=True)
    breaker_survival_stats.sort(key=lambda x: x["longevity_score"], reverse=True)
    
    with open(out_dir / "maker_leaderboard.json", "w") as f:
        json.dump(maker_survival_stats, f, indent=2)
        
    with open(out_dir / "breaker_leaderboard.json", "w") as f:
        json.dump(breaker_survival_stats, f, indent=2)
        
    for i, m in enumerate(maker_survival_stats[:10]):
        with open(out_dir / f"maker_top_{i+1}_score_{m['longevity_score']}.py", "w") as f:
            f.write(f"# Maker ID: {m['id']}\n# Longevity Score: {m['longevity_score']}\n")
            f.write(f"# Gens Survived: {m['gens_survived']}\n# Mutations Defeated: {m['mutations_defeated']}\n\n")
            f.write(m['src'])
            
    for i, b in enumerate(breaker_survival_stats[:10]):
        with open(out_dir / f"breaker_top_{i+1}_score_{b['longevity_score']}.py", "w") as f:
            f.write(f"# Breaker ID: {b['id']}\n# Longevity Score: {b['longevity_score']}\n")
            f.write(f"# Gens Survived: {b['gens_survived']}\n# Mutations Defeated: {b['mutations_defeated']}\n\n")
            f.write(b['src'])

    print(f"Co-Evolution Complete! Saved {len(maker_survival_stats)} Makers and {len(breaker_survival_stats)} Breakers to {out_dir}")

if __name__ == "__main__":
    main()
