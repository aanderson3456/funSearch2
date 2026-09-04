import sys, os, time, torch
sys.path.append("big_nn")
from resnet import SnakyNet
from mcts import MCTS
from env import SnakyEnv

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = SnakyNet(num_resBlocks=16, num_channels=256, board_size=13).to(device)
model.eval()

env = SnakyEnv(size=13)
mcts = MCTS(model, num_searches=400, device=device)

t0 = time.time()
mcts.search(env)
print("1 Move 400 searches:", time.time() - t0)
