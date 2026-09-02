import time
from funsearch.problems import snakey_interactive

def paving_breaker(last_maker_move, m_cells, b_cells, grid_radius=4):
    x, y = last_maker_move
    partner = (x + 1, y) if x % 2 == 0 else (x - 1, y)
    if partner not in set(m_cells) and partner not in set(b_cells):
        return partner
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]:
        cand = (x + dx, y + dy)
        if cand not in set(m_cells) and cand not in set(b_cells) and abs(cand[0]) <= grid_radius and abs(cand[1]) <= grid_radius:
            return cand
    return (999, 999)

def greedy_threat_breaker(last_maker_move, m_cells, b_cells, all_shapes):
    m_set, b_set = set(m_cells), set(b_cells)
    active = [s for s in all_shapes if not (s & b_set)]
    
    threat_1_cells = []
    for s in active:
      diff = s - m_set
      if len(diff) == 1:
        threat_1_cells.append(list(diff)[0])
    if threat_1_cells:
      return threat_1_cells[0]
      
    block_scores = {}
    for s in active:
      m_cnt = len(s & m_set)
      for p in s - m_set:
        block_scores[p] = block_scores.get(p, 0) + (5 ** m_cnt)
    if block_scores:
      return max(block_scores.keys(), key=lambda p: block_scores[p])
    return (999, 999)

def random_maker(m_cells, b_cells, active_shapes):
    m_set, b_set = set(m_cells), set(b_cells)
    for s in active_shapes:
        for p in s:
            if p not in m_set and p not in b_set:
                return p
    return (999, 999)

def simulate_game(maker_fn, breaker_fn, grid_radius=6, verbose=False):
    all_shapes = snakey_interactive._get_board_shapes(radius=grid_radius)
    m_cells, b_cells = [], []
    maker_won = False
    turn_taken = 0
    
    for turn in range(25):
        turn_taken = turn
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
            
        if hasattr(maker_fn, '__name__') and maker_fn.__name__ == 'random_maker':
            best_m_move = random_maker(m_cells, b_cells, active)
        else:
            best_m_move = max(candidates, key=lambda c: maker_fn(c, m_cells, b_cells, active))
            
        m_cells.append(best_m_move)
        if verbose:
            print(f"Turn {turn+1} - Maker plays: {best_m_move}")
        
        m_set = set(m_cells)
        active_for_breaker = [s for s in all_shapes if not (s & b_set)]
        candidates_b = set()
        for s in active_for_breaker:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates_b.add(p)
                    
        if not candidates_b:
            break
            
        if hasattr(breaker_fn, '__name__') and breaker_fn.__name__ == 'paving_breaker':
            b_move = paving_breaker(best_m_move, m_cells, b_cells, grid_radius)
        elif hasattr(breaker_fn, '__name__') and breaker_fn.__name__ == 'greedy_threat_breaker':
            b_move = greedy_threat_breaker(best_m_move, m_cells, b_cells, all_shapes)
        else:
            b_move = max(candidates_b, key=lambda c: breaker_fn(c, m_cells, b_cells, active_for_breaker))
            
        if b_move != (999, 999):
            b_cells.append(b_move)
            if verbose:
                print(f"Turn {turn+1} - Breaker plays: {b_move}")
            
    m_set = set(m_cells)
    max_cells_in_shape = max((len(s & m_set) for s in all_shapes), default=0)
    
    maker_score = float(max_cells_in_shape * 10)
    if maker_won:
        maker_score += 100.0 + (25 - turn_taken) * 10.0
        
    breaker_score = -maker_score
    
    return maker_won, max_cells_in_shape, turn_taken, maker_score, breaker_score

def run_arena():
    print("==================================================")
    print("🏆 FUNSEARCH INTERACTIVE ARENA 🏆")
    print("==================================================")
    
    radius = 6
    maker_fn = snakey_interactive.maker_priority
    breaker_fn = snakey_interactive.breaker_priority
    
    matchups = [
        ("Evolving Maker", maker_fn, "Paving Breaker (Baseline)", paving_breaker),
        ("Evolving Maker", maker_fn, "Greedy Breaker (Baseline)", greedy_threat_breaker),
        ("Random Maker (Baseline)", random_maker, "Evolving Breaker", breaker_fn),
        ("Evolving Maker", maker_fn, "Evolving Breaker", breaker_fn),
    ]
    
    total_maker_score = 0
    total_breaker_score = 0
    
    print(f"{'Matchup':<45} | {'Result':<20} | {'M Score':<8} | {'B Score':<8}")
    print("-" * 90)
    
    for m_name, m_func, b_name, b_func in matchups:
        is_main_event = (m_name == "Evolving Maker" and b_name == "Evolving Breaker")
        if is_main_event:
            print("\n>>> MAIN EVENT TRACE <<<")
        m_won, max_c, turns, m_score, b_score = simulate_game(m_func, b_func, radius, verbose=is_main_event)
        
        if m_name == "Evolving Maker":
            total_maker_score += m_score
        if b_name == "Evolving Breaker":
            total_breaker_score += b_score
            
        res_str = f"M Won (in {turns})" if m_won else f"B Blocked (Max {max_c}/6)"
        match_name = f"{m_name[:14]} vs {b_name[:25]}"
        print(f"{match_name:<45} | {res_str:<20} | {m_score:<8.1f} | {b_score:<8.1f}")
        
    print("==================================================")
    print(f"🥇 Evolving Maker Total Score:   {total_maker_score:.1f}")
    print(f"🥇 Evolving Breaker Total Score: {total_breaker_score:.1f}")
    print("==================================================")

if __name__ == '__main__':
    run_arena()
