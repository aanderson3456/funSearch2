import torch
from arena_tournament import ArenaAgent, run_match_and_save
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "big_nn"))
from resnet import SnakyNet

def main():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load models
    print("Loading models...")
    model_v1 = SnakyNet(in_channels=3)
    model_v1.load_state_dict(torch.load("snaky_v1_model_it850.pt", map_location=device))
    model_v1.to(device)
    model_v1.eval()
    agent_v1 = ArenaAgent("NNv1_it850", model_v1, in_channels=3, device=device, num_searches=200, use_threat_blend=False)

    model_v2 = SnakyNet(in_channels=5)
    model_v2.load_state_dict(torch.load("snaky_v2_model_it450.pt", map_location=device))
    model_v2.to(device)
    model_v2.eval()
    agent_v2 = ArenaAgent("NNv2_it450", model_v2, in_channels=5, device=device, num_searches=200, use_threat_blend=False)

    model_v3 = SnakyNet(in_channels=6)
    model_v3.load_state_dict(torch.load("snaky_v3_model_it29.pt", map_location=device))
    model_v3.to(device)
    model_v3.eval()
    agent_v3 = ArenaAgent("NNv3_it29", model_v3, in_channels=6, device=device, num_searches=200, use_threat_blend=True)

    matches = [
        (agent_v1, agent_v3, "Match 1 - NNv1 Maker vs NNv3 Breaker"),
        (agent_v3, agent_v1, "Match 2 - NNv3 Maker vs NNv1 Breaker"),
        (agent_v2, agent_v3, "Match 3 - NNv2 Maker vs NNv3 Breaker"),
        (agent_v3, agent_v2, "Match 4 - NNv3 Maker vs NNv2 Breaker"),
        (agent_v2, agent_v1, "Match 5 - NNv2 Maker vs NNv1 Breaker"),
        (agent_v1, agent_v2, "Match 6 - NNv1 Maker vs NNv2 Breaker"),
    ]

    for i, (maker, breaker, title) in enumerate(matches, 1):
        print(f"\nStarting {title}...")
        trace_file = f"match_{i}_trace.json"
        html_file = f"match_{i}_replay.html"
        run_match_and_save(maker, breaker, trace_file, html_file, title)

if __name__ == "__main__":
    main()
