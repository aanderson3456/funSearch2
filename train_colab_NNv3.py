import torch
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import os, glob, math, json, re
import sys

# Ensure local imports work whether run from repo root or FS2
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "big_nn"))
from env import SnakyEnv
from resnet import SnakyNet

print("=" * 60)
print("SnakyNet NNv3: High-Speed Self-Play Training (6-Channel + Threat Prior)")
print("=" * 60)

class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.capacity = capacity
        self.buffer = []
        
    def add(self, data):
        self.buffer.extend(data)
        if len(self.buffer) > self.capacity:
            self.buffer = self.buffer[-self.capacity:]
            
    def sample(self, batch_size):
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in indices]

class FastSnakyEnv:
    def __init__(self, size=13):
        self.size = size
        self.maker_board = 0
        self.breaker_board = 0
        self.current_player = 1
        self.done = False
        self.winner = 0
        
        self.occupied_array = np.zeros(size * size, dtype=bool)
        self.maker_array = np.zeros(size * size, dtype=np.float32)
        self.breaker_array = np.zeros(size * size, dtype=np.float32)
        
        temp_env = SnakyEnv(size=size)
        self.win_masks = temp_env.win_masks

    def get_legal_moves(self):
        return np.where(~self.occupied_array)[0].tolist()
        
    def step(self, move):
        move = int(move)
        if self.done:
            return self.done, self.winner
            
        self.occupied_array[move] = True
        
        if self.current_player == 1:
            self.maker_board |= (1 << move)
            self.maker_array[move] = 1.0
            mb = self.maker_board
            for m in self.win_masks:
                if (mb & m) == m:
                    self.done = True
                    self.winner = 1
                    return self.done, self.winner
        else:
            self.breaker_board |= (1 << move)
            self.breaker_array[move] = 1.0
            
        if (self.maker_board | self.breaker_board) == ((1 << (self.size * self.size)) - 1):
            self.done = True
            self.winner = 0
            return self.done, self.winner
            
        self.current_player *= -1
        return self.done, self.winner

def clone_env(env):
    new_env = FastSnakyEnv(size=env.size)
    new_env.maker_board = env.maker_board
    new_env.breaker_board = env.breaker_board
    new_env.current_player = env.current_player
    new_env.done = env.done
    new_env.winner = env.winner
    
    new_env.occupied_array = env.occupied_array.copy()
    new_env.maker_array = env.maker_array.copy()
    new_env.breaker_array = env.breaker_array.copy()
    new_env.win_masks = env.win_masks
    return new_env

class FastNode:
    __slots__ = ['parent', 'action_idx_in_parent', 'legal_moves', 'priors', 'visits', 'values', 'total_visits', 'children']
    
    def __init__(self, parent=None, action_idx_in_parent=None):
        self.parent = parent
        self.action_idx_in_parent = action_idx_in_parent
        self.legal_moves = None
        self.priors = None
        self.visits = None
        self.values = None
        self.total_visits = 0
        self.children = None
        
    def is_expanded(self):
        return self.legal_moves is not None
        
    def expand(self, legal_moves, policy):
        self.legal_moves = legal_moves
        num_moves = len(legal_moves)
        self.visits = np.zeros(num_moves, dtype=np.int32)
        self.values = np.zeros(num_moves, dtype=np.float32)
        
        if num_moves > 0:
            self.priors = policy[legal_moves].copy()
            p_sum = np.sum(self.priors)
            if p_sum > 0:
                self.priors /= p_sum
            else:
                self.priors = np.ones(num_moves, dtype=np.float32) / num_moves
                
        self.children = [None] * num_moves

# --- Static Heuristic Planes & Precomputed Threat Tables ---
checkerboard = np.zeros((13, 13), dtype=np.float32)
centrality = np.zeros((13, 13), dtype=np.float32)
center = 6.0
max_dist = 13 / 1.414
for _y in range(13):
    for _x in range(13):
        checkerboard[_y, _x] = 1.0 if (_x + _y) % 2 == 0 else 0.0
        dist = np.sqrt((_x - center)**2 + (_y - center)**2)
        centrality[_y, _x] = max(0.0, 1.0 - (dist / max_dist))
HEURISTIC_STATIC_PLANES = np.stack([checkerboard, centrality])

_temp_env = SnakyEnv(size=13)
_mask_cells = []
for m in _temp_env.win_masks:
    _mask_cells.append([i for i in range(169) if (m & (1 << i))])
WIN_MASK_CELLS = np.array(_mask_cells, dtype=np.int32)
WEIGHT_LOOKUP = np.array([0, 2, 10, 50, 250, 10000, 0], dtype=np.float32)

def compute_threat_single(env):
    m_arr = env.maker_array
    b_arr = env.breaker_array
    mask_b_counts = b_arr[WIN_MASK_CELLS].sum(axis=1)
    active_idx = np.where(mask_b_counts == 0)[0]
    if len(active_idx) == 0:
        return np.zeros(169, dtype=np.float32), False
    active_cells = WIN_MASK_CELLS[active_idx]
    m_counts = m_arr[active_cells].sum(axis=1).astype(np.int32)
    is_crit = bool(np.any(m_counts == 5))
    weights = WEIGHT_LOOKUP[m_counts]
    empty_mask = (m_arr[active_cells] == 0)
    t_map = np.zeros(169, dtype=np.float32)
    np.add.at(t_map, active_cells[empty_mask], np.broadcast_to(weights[:, None], active_cells.shape)[empty_mask])
    return t_map, is_crit

def compute_threat_batch(envs):
    n = len(envs)
    threat_maps = np.zeros((n, 169), dtype=np.float32)
    crit_flags = np.zeros(n, dtype=bool)
    for i, e in enumerate(envs):
        t_map, is_crit = compute_threat_single(e)
        threat_maps[i] = t_map
        crit_flags[i] = is_crit
    return threat_maps, crit_flags

def _encode_state_batch(envs, device, threat_maps=None):
    n = len(envs)
    size = envs[0].size
    states = np.empty((n, 6, size, size), dtype=np.float32)
    
    mb = np.array([e.maker_array for e in envs], dtype=np.float32).reshape(n, size, size)
    bb = np.array([e.breaker_array for e in envs], dtype=np.float32).reshape(n, size, size)
    states[:, 0] = mb
    states[:, 1] = bb
    cp = np.array([e.current_player for e in envs], dtype=np.float32)
    states[:, 2] = (cp == 1)[:, None, None]
    states[:, 3] = HEURISTIC_STATIC_PLANES[0]
    states[:, 4] = HEURISTIC_STATIC_PLANES[1]
    
    if threat_maps is None:
        threat_maps, _ = compute_threat_batch(envs)
    
    mx = np.maximum(threat_maps.max(axis=1, keepdims=True), 1e-5)
    norm_threats = (threat_maps / mx).reshape(n, size, size)
    states[:, 5] = norm_threats
    
    return torch.tensor(states, dtype=torch.float32, device=device)

def blend_breaker_policy(policy, env, t_map, is_crit):
    legal_moves = env.get_legal_moves()
    if len(legal_moves) == 0:
        return policy
    t_legal = t_map[legal_moves]
    t_sum = np.sum(t_legal)
    if is_crit:
        crit_mask = (t_legal >= 9000)
        if np.any(crit_mask):
            p_threat = np.zeros_like(t_legal)
            p_threat[crit_mask] = 1.0 / np.sum(crit_mask)
            blended_legal = 0.05 * policy[legal_moves] + 0.95 * p_threat
            p_copy = policy.copy()
            p_copy[legal_moves] = blended_legal
            return p_copy
    elif t_sum > 0:
        p_threat = t_legal / t_sum
        blended_legal = 0.65 * policy[legal_moves] + 0.35 * p_threat
        p_copy = policy.copy()
        p_copy[legal_moves] = blended_legal
        return p_copy
    return policy

def batched_search(model, envs, num_searches, c_puct=1.0, add_noise=False, device='cuda'):
    roots = [FastNode() for _ in range(len(envs))]
    
    # 1. Compute threats ONCE at the root across all active envs (blazingly fast: ~0.01s total)
    threat_maps, crit_flags = compute_threat_batch(envs)
    states_tensor = _encode_state_batch(envs, device, threat_maps=threat_maps)
    with torch.no_grad():
        policy_logits, _ = model(states_tensor)
        policies = F.softmax(policy_logits, dim=1).cpu().numpy()
        
    for i, env in enumerate(envs):
        legal_moves = env.get_legal_moves()
        policy = policies[i]
        if env.current_player == -1:
            policy = blend_breaker_policy(policy, env, threat_maps[i], crit_flags[i])
        roots[i].expand(legal_moves, policy)
        if add_noise and len(legal_moves) > 0:
            dirichlet_alpha = 0.3
            dirichlet_noise = np.random.dirichlet([dirichlet_alpha] * len(legal_moves))
            frac = 0.25
            roots[i].priors = (1 - frac) * roots[i].priors + frac * dirichlet_noise

    # 2. MCTS Simulation Rollouts: Fast GPU batching without re-evaluating python bitmasks 10,000x
    for _ in range(num_searches):
        search_envs = [clone_env(env) for env in envs]
        search_nodes = [root for root in roots]
        
        for i in range(len(envs)):
            node = search_nodes[i]
            env = search_envs[i]
            
            while node.is_expanded():
                if len(node.legal_moves) == 0:
                    break
                    
                q = np.divide(node.values, node.visits, out=np.zeros_like(node.values), where=node.visits!=0)
                if env.current_player == -1:
                    q = -q
                u = c_puct * node.priors * math.sqrt(node.total_visits) / (1.0 + node.visits)
                ucb = q + u
                
                best_idx = np.argmax(ucb)
                best_move = node.legal_moves[best_idx]
                
                env.step(best_move)
                
                if node.children[best_idx] is None:
                    child_node = FastNode(parent=node, action_idx_in_parent=best_idx)
                    node.children[best_idx] = child_node
                    search_nodes[i] = child_node
                    break
                else:
                    node = node.children[best_idx]
                    search_nodes[i] = node
                    
        states_to_eval = []
        eval_indices = []
        
        for i in range(len(envs)):
            env = search_envs[i]
            if not env.done:
                states_to_eval.append(env)
                eval_indices.append(i)
            else:
                v = 1.0 if env.winner == 1 else -1.0
                node = search_nodes[i]
                while node.parent is not None:
                    node.total_visits += 1
                    p = node.parent
                    idx = node.action_idx_in_parent
                    p.visits[idx] += 1
                    p.values[idx] += v
                    node = p
                node.total_visits += 1
                
        if states_to_eval:
            # Inside MCTS, Plane 5 is evaluated directly; GPU handles policy/value in milliseconds!
            states_tensor = _encode_state_batch(states_to_eval, device)
            with torch.no_grad():
                policy_logits, values = model(states_tensor)
                policies = F.softmax(policy_logits, dim=1).cpu().numpy()
                values = values.cpu().numpy()
                
            for idx, i in enumerate(eval_indices):
                node = search_nodes[i]
                env = search_envs[i]
                policy = policies[idx]
                v = values[idx][0]
                
                legal_moves = env.get_legal_moves()
                node.expand(legal_moves, policy)
                
                while node.parent is not None:
                    node.total_visits += 1
                    p = node.parent
                    idx_in_p = node.action_idx_in_parent
                    p.visits[idx_in_p] += 1
                    p.values[idx_in_p] += v
                    node = p
                node.total_visits += 1
                
    action_probs_batch = []
    for i in range(len(envs)):
        action_probs = np.zeros(envs[i].size * envs[i].size)
        root = roots[i]
        for idx_in_p, move in enumerate(root.legal_moves):
            action_probs[move] = root.visits[idx_in_p] / num_searches
        
        s = np.sum(action_probs)
        if s > 0:
            action_probs = action_probs / s
        action_probs_batch.append(action_probs)
        
    return action_probs_batch

def self_play(model, num_games=100, mcts_searches=100, device='cuda'):
    envs = [FastSnakyEnv(size=13) for _ in range(num_games)]
    all_data = []
    
    active_indices = list(range(num_games))
    game_data = [[] for _ in range(num_games)]
    game_lengths = []
    games_finished = 0
    
    move_count = 0
    while active_indices:
        move_count += 1
        current_envs = [envs[i] for i in active_indices]
        
        if move_count % 5 == 0 or move_count == 1:
            print(f'\rProcessing move {move_count} simultaneously for {len(active_indices)} active games...', end='', flush=True)
            
        action_probs_batch = batched_search(model, current_envs, num_searches=mcts_searches, add_noise=True, device=device)
        
        next_active = []
        for idx_in_batch, original_idx in enumerate(active_indices):
            env = current_envs[idx_in_batch]
            action_probs = action_probs_batch[idx_in_batch]
            
            game_data[original_idx].append((env.maker_board, env.breaker_board, env.current_player, action_probs))
            
            action = np.random.choice(169, p=action_probs)
            done, winner = env.step(action)
            
            if done:
                games_finished += 1
                game_lengths.append(move_count)
                reward = 1.0 if winner == 1 else -1.0
                for mb, bb, cp, pi in game_data[original_idx]:
                    all_data.append((mb, bb, cp, pi, reward))
            else:
                next_active.append(original_idx)
                
        active_indices = next_active
        
    print(f'\nAll {num_games} parallel games finished! Avg game length: {np.mean(game_lengths):.1f} moves.')
    return all_data, game_lengths

def train(model, buffer, batch_size=512, epochs=10, device='cuda'):
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    model.train()
    total_loss = 0.0
    shifts = 1 << np.arange(169, dtype=object)
    
    for epoch in range(epochs):
        data = buffer.sample(batch_size)
        states = np.zeros((batch_size, 6, 13, 13), dtype=np.float32)
        target_policies = np.zeros((batch_size, 169), dtype=np.float32)
        target_values = np.zeros((batch_size, 1), dtype=np.float32)
        
        mb_arr = np.array([item[0] for item in data], dtype=object)
        bb_arr = np.array([item[1] for item in data], dtype=object)
        
        mb_bits = (mb_arr[:, None] & shifts) != 0
        bb_bits = (bb_arr[:, None] & shifts) != 0
        states[:, 0] = mb_bits.reshape((batch_size, 13, 13))
        states[:, 1] = bb_bits.reshape((batch_size, 13, 13))
        cp = np.array([item[2] for item in data])
        states[:, 2] = (cp == 1)[:, None, None]
        states[:, 3] = HEURISTIC_STATIC_PLANES[0]
        states[:, 4] = HEURISTIC_STATIC_PLANES[1]
        
        threat_maps = np.zeros((batch_size, 169), dtype=np.float32)
        for i in range(batch_size):
            mask_b_counts = bb_bits[i][WIN_MASK_CELLS].sum(axis=1)
            active_idx = np.where(mask_b_counts == 0)[0]
            if len(active_idx) > 0:
                active_cells = WIN_MASK_CELLS[active_idx]
                m_counts = mb_bits[i][active_cells].sum(axis=1).astype(np.int32)
                weights = WEIGHT_LOOKUP[m_counts]
                empty_mask = (mb_bits[i][active_cells] == 0)
                np.add.at(threat_maps[i], active_cells[empty_mask], np.broadcast_to(weights[:, None], active_cells.shape)[empty_mask])
        mx = np.maximum(threat_maps.max(axis=1, keepdims=True), 1e-5)
        states[:, 5] = (threat_maps / mx).reshape((batch_size, 13, 13))

        for i, item in enumerate(data):
            target_policies[i] = item[3]
            target_values[i] = item[4]
            
        states = torch.tensor(states, dtype=torch.float32, device=device)
        target_policies = torch.tensor(target_policies, dtype=torch.float32, device=device)
        target_values = torch.tensor(target_values, dtype=torch.float32, device=device)
        
        optimizer.zero_grad()
        out_policy, out_value = model(states)
        
        log_probs = F.log_softmax(out_policy, dim=1)
        policy_loss = -(target_policies * log_probs).sum(dim=1).mean()
        value_loss = F.mse_loss(out_value, target_values)
        
        loss = policy_loss + value_loss
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        
    return total_loss / epochs

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')
    print(f'Using compute device: {device}')
    if device.type == 'cuda':
        print(f'GPU Name: {torch.cuda.get_device_name(0)}')

    model = SnakyNet(in_channels=6, num_resBlocks=16, num_channels=256, board_size=13).to(device)
    buffer = ReplayBuffer(capacity=100000)

    checkpoint_dir = "/content/drive/MyDrive/SnakyNet_v3_Checkpoints"
    if not os.path.exists("/content/drive"):
        # Local fallback if running locally
        checkpoint_dir = "checkpoints_v3"
    os.makedirs(checkpoint_dir, exist_ok=True)

    all_models = glob.glob(f"{checkpoint_dir}/snaky_large_model_it*.pt")

    start_iteration = 0
    if all_models:
        def get_it(path):
            m = re.search(r'it(\d+)\.pt', path)
            return int(m.group(1)) if m else -1
        latest_model_path = max(all_models, key=get_it)
        start_iteration = get_it(latest_model_path) + 1
        print(f"\nFound checkpoint: {latest_model_path}")
        loaded = torch.load(latest_model_path, weights_only=False, map_location=device)
        if isinstance(loaded, dict):
            model.load_state_dict(loaded)
            print("Successfully loaded weights from state_dict!")
        else:
            model.load_state_dict(loaded.state_dict())
            print("Successfully extracted and loaded weights from full model!")
    else:
        print("\nNo checkpoints found. Starting NNv3 fresh from scratch at Iteration 0!")

    iterations = 1000
    games_per_iter = 100
    batch_size = 512

    loss_history_path = f"{checkpoint_dir}/loss_history.json"
    loss_history = []
    if os.path.exists(loss_history_path):
        with open(loss_history_path, 'r') as f:
            loss_history = json.load(f)
        print(f"Loaded {len(loss_history)} loss records from Drive!")

    for it in range(start_iteration, iterations):
        print(f"\n--- Iteration {it}/{iterations} ---")
        model.eval()
        print("Starting Self-Play...")
        data, game_lengths = self_play(model, num_games=games_per_iter, mcts_searches=100, device=device)
        buffer.add(data)
        
        if len(buffer.buffer) >= batch_size: 
            loss = train(model, buffer, batch_size=batch_size, epochs=10, device=device)
            print(f"Training Loss: {loss:.4f}")
            
            summary = {
                'min': int(np.min(game_lengths)),
                'q1': float(np.percentile(game_lengths, 25)),
                'median': float(np.median(game_lengths)),
                'q3': float(np.percentile(game_lengths, 75)),
                'max': int(np.max(game_lengths))
            }
            loss_history.append({'iteration': it, 'loss': loss, 'game_lengths': summary})
            
            with open(loss_history_path, 'w') as f:
                json.dump(loss_history, f)
            
        save_path = f"{checkpoint_dir}/snaky_large_model_it{it}.pt"
        torch.save(model.state_dict(), save_path)
        print(f"Saved Checkpoint to Google Drive! ({save_path})")

if __name__ == "__main__":
    main()
