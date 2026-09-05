import torch
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "big_nn"))
from resnet import SnakyNet

print("Instantiating SnakyNet v2...")
model = SnakyNet(in_channels=5, num_resBlocks=16, num_channels=256, board_size=13)
print("Model created.")

# Test input: Batch=2, Channels=5, Height=13, Width=13
test_input = torch.randn(2, 5, 13, 13)
print(f"Feeding input of shape {test_input.shape}...")

policy, value = model(test_input)
print(f"Policy output shape: {policy.shape} (Expected: 2, 169)")
print(f"Value output shape: {value.shape} (Expected: 2, 1)")
print("SnakyNet v2 forward pass successful!")
