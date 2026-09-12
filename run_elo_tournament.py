import torch
import numpy as np
import sys
import os
import json
import itertools
from collections import defaultdict

from arena_tournament import ArenaAgent, run_match_and_save, ALL_SHAPES_13X13, play_match
from big_nn.resnet import SnakyNet
from env import SnakyEnv

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "co_evolve_champions"))
import maker_top_1_score_112 as fs_maker
import breaker_top_1_score_276 as fs_breaker

class FunSearchWrapper:
    def __init__(self, name):
        self.name = name

    def search(self, env):
        # We need to know if we are Maker or Breaker
        role = env.current_player
        
        m_cells = []
        b_cells = []
        for i in range(169):
            if env.maker_board & (1 << i):
                y, x = divmod(i, 13)
                m_cells.append((x - 6, y - 6))
            if env.breaker_board & (1 << i):
                y, x = divmod(i, 13)
                b_cells.append((x - 6, y - 6))
        
        m_set = set(m_cells)
        b_set = set(b_cells)
        active = [s for s in ALL_SHAPES_13X13 if not (s & b_set)]

        scores = np.zeros(169, dtype=np.float32)
        legal_moves = env.get_legal_moves()
        for idx in legal_moves:
            y, x = divmod(idx, 13)
            c = (x - 6, y - 6)
            if role == 1:
                scores[idx] = fs_maker.priority(c, m_cells, b_cells, active)
            else:
                scores[idx] = fs_breaker.breaker_priority(c, m_cells, b_cells, active)
        return scores

def expected_score(rating_a, rating_b):
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))

def update_elo(rating_a, rating_b, score_a, k=32):
    ea = expected_score(rating_a, rating_b)
    eb = expected_score(rating_b, rating_a)
    new_a = rating_a + k * (score_a - ea)
    new_b = rating_b + k * ((1.0 - score_a) - eb)
    return new_a, new_b

def main():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")

    print("Loading models...")
    model_v1 = SnakyNet(in_channels=3)
    model_v1.load_state_dict(torch.load("snaky_v1_model_it850.pt", map_location=device, weights_only=True))
    model_v1.to(device)
    model_v1.eval()
    agent_v1 = ArenaAgent("NNv1", model_v1, in_channels=3, device=device, num_searches=200, use_threat_blend=False)

    model_v2 = SnakyNet(in_channels=5)
    model_v2.load_state_dict(torch.load("snaky_v2_model_it450.pt", map_location=device, weights_only=True))
    model_v2.to(device)
    model_v2.eval()
    agent_v2 = ArenaAgent("NNv2", model_v2, in_channels=5, device=device, num_searches=200, use_threat_blend=False)

    model_v3 = SnakyNet(in_channels=6)
    model_v3.load_state_dict(torch.load("snaky_v3_model_it72.pt", map_location=device, weights_only=True))
    model_v3.to(device)
    model_v3.eval()
    agent_v3 = ArenaAgent("NNv3_it72", model_v3, in_channels=6, device=device, num_searches=200, use_threat_blend=True)

    agent_fs = FunSearchWrapper("FunSearch")

    agents = [agent_v1, agent_v2, agent_v3, agent_fs]
    elos = {a.name: 1000.0 for a in agents}
    stats = {a.name: {
        "wins": 0, "losses": 0,
        "maker_wins": 0, "maker_losses": 0,
        "breaker_wins": 0, "breaker_losses": 0,
        "turns_played": []
    } for a in agents}
    match_history = []

    match_idx = 1
    total_matches = len(agents) * (len(agents) - 1)
    for maker, breaker in itertools.permutations(agents, 2):
        print(f"\n--- Match {match_idx}/{total_matches}: Maker({maker.name}) vs Breaker({breaker.name}) ---")
        trace_file = f"elo_match_{match_idx}_trace.json"
        html_file = f"elo_match_{match_idx}_replay.html"
        title = f"Elo Match {match_idx}: {maker.name} (Maker) vs {breaker.name} (Breaker)"
        
        winner_name, turns = run_match_and_save(maker, breaker, trace_file, html_file, title)
        
        maker_won = (winner_name == maker.name)
        winning_role = "Maker" if maker_won else "Breaker"
        score_maker = 1.0 if maker_won else 0.0
        
        old_m, old_b = elos[maker.name], elos[breaker.name]
        new_m, new_b = update_elo(old_m, old_b, score_maker)
        
        print(f"Result: {winner_name} won as {winning_role} in {turns} turns.")
        print(f"Elo Update: {maker.name} {old_m:.1f} -> {new_m:.1f} ({new_m - old_m:+.1f})")
        print(f"Elo Update: {breaker.name} {old_b:.1f} -> {new_b:.1f} ({new_b - old_b:+.1f})")
        
        elos[maker.name] = new_m
        elos[breaker.name] = new_b
        
        if maker_won:
            stats[maker.name]["wins"] += 1
            stats[maker.name]["maker_wins"] += 1
            stats[breaker.name]["losses"] += 1
            stats[breaker.name]["breaker_losses"] += 1
        else:
            stats[breaker.name]["wins"] += 1
            stats[breaker.name]["breaker_wins"] += 1
            stats[maker.name]["losses"] += 1
            stats[maker.name]["maker_losses"] += 1

        stats[maker.name]["turns_played"].append(turns)
        stats[breaker.name]["turns_played"].append(turns)
        
        match_history.append({
            "match": match_idx,
            "maker": maker.name,
            "breaker": breaker.name,
            "winner": winner_name,
            "winning_role": winning_role,
            "turns": turns,
            "elo_before": {maker.name: round(old_m, 1), breaker.name: round(old_b, 1)},
            "elo_after": {maker.name: round(new_m, 1), breaker.name: round(new_b, 1)}
        })
        
        match_idx += 1

    total_maker_wins = sum(1 for m in match_history if m["winning_role"] == "Maker")
    total_breaker_wins = sum(1 for m in match_history if m["winning_role"] == "Breaker")
    avg_turns = float(np.mean([m["turns"] for m in match_history]))

    print("\n=======================================================")
    print("FINAL ELO RATINGS & TOURNAMENT STANDINGS")
    print("=======================================================")
    sorted_elos = sorted(elos.items(), key=lambda x: x[1], reverse=True)
    rankings = []
    for rank, (name, elo) in enumerate(sorted_elos, 1):
        st = stats[name]
        total_g = st["wins"] + st["losses"]
        win_pct = (st["wins"] / total_g * 100) if total_g > 0 else 0.0
        m_total = st["maker_wins"] + st["maker_losses"]
        m_win_pct = (st["maker_wins"] / m_total * 100) if m_total > 0 else 0.0
        b_total = st["breaker_wins"] + st["breaker_losses"]
        b_win_pct = (st["breaker_wins"] / b_total * 100) if b_total > 0 else 0.0
        avg_t = float(np.mean(st["turns_played"])) if st["turns_played"] else 0.0

        rankings.append({
            "rank": rank,
            "name": name,
            "elo": round(elo, 1),
            "wins": st["wins"],
            "losses": st["losses"],
            "win_pct": round(win_pct, 1),
            "maker_record": f"{st['maker_wins']}-{st['maker_losses']}",
            "maker_win_pct": round(m_win_pct, 1),
            "breaker_record": f"{st['breaker_wins']}-{st['breaker_losses']}",
            "breaker_win_pct": round(b_win_pct, 1),
            "avg_turns": round(avg_t, 1)
        })
        print(f"{rank}. {name:12s} | Elo: {elo:6.1f} | Record: {st['wins']}-{st['losses']} ({win_pct:4.1f}%) | Maker: {st['maker_wins']}-{st['maker_losses']} ({m_win_pct:4.1f}%) | Breaker: {st['breaker_wins']}-{st['breaker_losses']} ({b_win_pct:4.1f}%) | Avg Turns: {avg_t:.1f}")

    print("\n=======================================================")
    print("ROLE STATISTICS")
    print("=======================================================")
    print(f"Maker Wins:   {total_maker_wins} / {total_matches} ({total_maker_wins / total_matches * 100:.1f}%)")
    print(f"Breaker Wins: {total_breaker_wins} / {total_matches} ({total_breaker_wins / total_matches * 100:.1f}%)")
    print(f"Average Game Length: {avg_turns:.1f} turns")
    print("=======================================================\n")

    summary_data = {
        "elos": {k: round(v, 2) for k, v in elos.items()},
        "rankings": rankings,
        "role_statistics": {
            "total_matches": total_matches,
            "maker_wins": total_maker_wins,
            "breaker_wins": total_breaker_wins,
            "maker_win_pct": round(total_maker_wins / total_matches * 100, 1),
            "breaker_win_pct": round(total_breaker_wins / total_matches * 100, 1),
            "avg_game_length_turns": round(avg_turns, 1)
        },
        "history": match_history
    }

    with open("elo_results.json", "w") as f:
        json.dump(summary_data, f, indent=4)
    print("Saved tournament results to elo_results.json")

if __name__ == "__main__":
    main()
