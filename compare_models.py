import torch
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "big_nn"))
from resnet import SnakyNet
from env import SnakyEnv

device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

def load_model(path):
    model = SnakyNet(num_resBlocks=16, num_channels=256, board_size=13).to(device)
    model.load_state_dict(torch.load(path, map_location=device, weights_only=True))
    model.eval()
    return model

print("Loading models...")
model_360 = load_model("snaky_large_model_it360.pt")
model_450 = load_model("snaky_large_model_it450.pt")

env = SnakyEnv(size=13)
# Play a few moves to get a non-empty board
env.step(84) # center
env.step(85)
env.step(97)
env.step(98)

# Encode state
states = np.zeros((1, 3, 13, 13), dtype=np.float32)
for i in range(169):
    y, x = divmod(i, 13)
    if env.maker_board & (1 << i):
        states[0, 0, y, x] = 1.0
    if env.breaker_board & (1 << i):
        states[0, 1, y, x] = 1.0
states[0, 2, :, :] = 1.0 if env.current_player == 1 else 0.0

states_tensor = torch.tensor(states, dtype=torch.float32, device=device)

with torch.no_grad():
    p_360, v_360 = model_360(states_tensor)
    p_450, v_450 = model_450(states_tensor)
    
print("\n--- Board State ---")
print("Maker at:", [(i%13, i//13) for i in range(169) if env.maker_board & (1<<i)])
print("Breaker at:", [(i%13, i//13) for i in range(169) if env.breaker_board & (1<<i)])
print("Current Player:", "Maker" if env.current_player == 1 else "Breaker")

print("\n--- Model Evaluation ---")
print(f"Model 360 Value: {v_360.item():.4f}")
print(f"Model 450 Value: {v_450.item():.4f}")

p_360_np = p_360.cpu().numpy()[0]
p_450_np = p_450.cpu().numpy()[0]

top_3_360 = np.argsort(p_360_np)[-3:][::-1]
top_3_450 = np.argsort(p_450_np)[-3:][::-1]

print(f"\nModel 360 Top 3 Moves:")
for i in top_3_360:
    print(f"  ({i%13}, {i//13}) - Prob: {torch.softmax(p_360, dim=1)[0, i].item():.4f}")

print(f"\nModel 450 Top 3 Moves:")
for i in top_3_450:
    print(f"  ({i%13}, {i//13}) - Prob: {torch.softmax(p_450, dim=1)[0, i].item():.4f}")

