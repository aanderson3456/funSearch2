import torch
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import copy
from env import SnakyEnv
from resnet import SnakyNet
from mcts import MCTS
import os

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.capacity = capacity
        self.buffer = []
        
    def add(self, data):
        self.buffer.extend(data)
        if len(self.buffer) > self.capacity:
            self.buffer = self.buffer[-self.capacity:]
            
    def sample(self, batch_size):
        idx = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in idx]

def self_play(model, num_games=10, mcts_searches=50, device="cpu"):
    mcts = MCTS(model, num_searches=mcts_searches, device=device)
    all_data = []
    
    for g in range(num_games):
        env = SnakyEnv(size=8)
        game_data = [] # list of (mb, bb, policy)
        
        while not env.done:
            # We add exploration noise at the root via MCTS
            action_probs = mcts.search(env)
            
            # Store state and policy (unaugmented)
            game_data.append((env.maker_board, env.breaker_board, env.current_player, action_probs))
            
            # Sample action (temperature = 1 for first 15 moves, else 0)
            if len(game_data) < 15:
                action = np.random.choice(len(action_probs), p=action_probs)
            else:
                action = np.argmax(action_probs)
                
            env.step(action)
            
        # Game over, assign values
        # If Maker wins (winner=1), Maker moves get value 1, Breaker moves get value -1 (relative to their turn)
        # Actually value is always from Maker's perspective in our network.
        v = 1.0 if env.winner == 1 else -1.0 # Breaker wins by drawing or blocking
        
        augmented_data = []
        for mb, bb, cp, policy in game_data:
            symmetries = env.get_symmetries(mb, bb, policy)
            for s_mb, s_bb, s_policy in symmetries:
                augmented_data.append((s_mb, s_bb, cp, s_policy, v))
                
        all_data.extend(augmented_data)
        print(f"Game {g+1}/{num_games} finished. Winner: {'Maker' if env.winner==1 else 'Breaker'}. Moves: {len(game_data)}")
        
    return all_data

def train(model, buffer, batch_size=64, epochs=1, lr=0.001, device="cpu"):
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    model.train()
    
    for epoch in range(epochs):
        data = buffer.sample(batch_size)
        
        states = np.zeros((batch_size, 3, 8, 8), dtype=np.float32)
        target_policies = np.zeros((batch_size, 64), dtype=np.float32)
        target_values = np.zeros((batch_size, 1), dtype=np.float32)
        
        for i, (mb, bb, cp, p, v) in enumerate(data):
            for bit in range(64):
                y, x = divmod(bit, 8)
                if mb & (1 << bit):
                    states[i, 0, y, x] = 1.0
                if bb & (1 << bit):
                    states[i, 1, y, x] = 1.0
            states[i, 2, :, :] = 1.0 if cp == 1 else 0.0
            target_policies[i] = p
            target_values[i] = v
            
        states = torch.tensor(states, dtype=torch.float32, device=device)
        target_policies = torch.tensor(target_policies, dtype=torch.float32, device=device)
        target_values = torch.tensor(target_values, dtype=torch.float32, device=device)
        
        optimizer.zero_grad()
        out_policy, out_value = model(states)
        
        # Policy Loss: Cross Entropy
        # out_policy are logits, target is probabilities
        log_probs = F.log_softmax(out_policy, dim=1)
        policy_loss = -(target_policies * log_probs).sum(dim=1).mean()
        
        # Value Loss: MSE
        value_loss = F.mse_loss(out_value, target_values)
        
        loss = policy_loss + value_loss
        loss.backward()
        optimizer.step()
        
    return loss.item()

def run_pipeline():
    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")
    
    model = SnakyNet(board_size=8).to(device)
    buffer = ReplayBuffer(capacity=50000)
    
    iterations = 3
    games_per_iter = 2
    
    for it in range(iterations):
        print(f"--- Iteration {it+1}/{iterations} ---")
        model.eval()
        data = self_play(model, num_games=games_per_iter, mcts_searches=30, device=device)
        buffer.add(data)
        
        if len(buffer.buffer) >= 64:
            loss = train(model, buffer, batch_size=64, epochs=5, device=device)
            print(f"Training Loss: {loss:.4f}")
            
        # Save checkpoint
        torch.save(model.state_dict(), f"snaky_model_it{it}.pt")

if __name__ == "__main__":
    run_pipeline()
