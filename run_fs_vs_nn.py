import torch
import numpy as np
import sys
import os

from arena_tournament import ArenaAgent, run_match_and_save, ALL_SHAPES_13X13
from big_nn.resnet import SnakyNet
from env import SnakyEnv

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "co_evolve_champions"))
import maker_top_1_score_112 as fs_maker
import breaker_top_1_score_276 as fs_breaker

class FunSearchWrapper:
    def __init__(self, name, priority_func):
        self.name = name
        self.priority_func = priority_func

    def search(self, env):
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
            scores[idx] = self.priority_func(c, m_cells, b_cells, active)
        return scores

def main():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")

    print("Loading NNv3 model...")
    model_v3 = SnakyNet(in_channels=6)
    model_v3.load_state_dict(torch.load("snaky_v3_model_it37.pt", map_location=device))
    model_v3.to(device)
    model_v3.eval()
    agent_nnv3 = ArenaAgent("NNv3_it37", model_v3, in_channels=6, device=device, num_searches=200, use_threat_blend=True)

    agent_fs_maker = FunSearchWrapper("FunSearch_Maker_112", fs_maker.priority)
    agent_fs_breaker = FunSearchWrapper("FunSearch_Breaker_276", fs_breaker.breaker_priority)

    matches = [
        (agent_fs_maker, agent_nnv3, "FS_vs_NN_Match_1_FSMaker_vs_NNv3Breaker"),
        (agent_nnv3, agent_fs_breaker, "FS_vs_NN_Match_2_NNv3Maker_vs_FSBreaker")
    ]

    for maker, breaker, title in matches:
        print(f"\nStarting {title}...")
        trace_file = f"{title}_trace.json"
        html_file = f"{title}_replay.html"
        run_match_and_save(maker, breaker, trace_file, html_file, title)

if __name__ == "__main__":
    main()
