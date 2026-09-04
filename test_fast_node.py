import time, math
import numpy as np

class Node:
    def __init__(self, prior_prob=1.0):
        self.children = {}
        self.visit_count = 0
        self.value_sum = 0
        self.prior_prob = prior_prob
    def get_value(self):
        return 0 if self.visit_count == 0 else self.value_sum / self.visit_count

class FastNode:
    def __init__(self, legal_moves, priors):
        self.legal_moves = np.array(legal_moves, dtype=np.int32)
        num_moves = len(legal_moves)
        self.visits = np.zeros(num_moves, dtype=np.float32)
        self.values = np.zeros(num_moves, dtype=np.float32)
        self.priors = priors[legal_moves]
        self.children = [None] * num_moves
        self.total_visits = 0

# Set up trees
legal_moves = list(range(100))
priors = np.random.rand(169).astype(np.float32)

root_slow = Node()
for m in legal_moves:
    child = Node(prior_prob=priors[m])
    child.visit_count = np.random.randint(1, 100)
    child.value_sum = np.random.randn() * child.visit_count
    root_slow.children[m] = child
root_slow.visit_count = sum(c.visit_count for c in root_slow.children.values())

root_fast = FastNode(legal_moves, priors)
for i, m in enumerate(legal_moves):
    v = np.random.randint(1, 100)
    root_fast.visits[i] = v
    root_fast.values[i] = np.random.randn() * v
root_fast.total_visits = np.sum(root_fast.visits)

c_puct = 1.0

# Benchmark Slow Node UCB
t0 = time.time()
for _ in range(10000):
    best_ucb = -float('inf')
    best_action = None
    
    for action, child in root_slow.children.items():
        q = child.get_value()
        u = c_puct * child.prior_prob * math.sqrt(root_slow.visit_count) / (1 + child.visit_count)
        ucb = q + u
        if ucb > best_ucb:
            best_ucb = ucb
            best_action = action
print("Slow UCB:", time.time() - t0)

# Benchmark Fast Node UCB
t0 = time.time()
for _ in range(10000):
    q = np.where(root_fast.visits > 0, root_fast.values / root_fast.visits, 0.0)
    u = c_puct * root_fast.priors * math.sqrt(root_fast.total_visits) / (1.0 + root_fast.visits)
    ucb = q + u
    best_idx = np.argmax(ucb)
    best_action = root_fast.legal_moves[best_idx]
print("Fast UCB:", time.time() - t0)

