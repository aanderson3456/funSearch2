import numpy as np
import time

class Env:
    def __init__(self):
        self.size = 13
        self.maker_array = np.zeros(169, dtype=np.float32)
        self.breaker_array = np.zeros(169, dtype=np.float32)
        self.current_player = 1

envs = [Env() for _ in range(100)]
for e in envs:
    e.maker_array[np.random.randint(0, 169, 10)] = 1.0
    e.breaker_array[np.random.randint(0, 169, 10)] = 1.0

def encode_new(envs):
    n = len(envs)
    size = 13
    states = np.zeros((n, 3, 169), dtype=np.float32)
    
    for i, e in enumerate(envs):
        states[i, 0] = e.maker_array
        states[i, 1] = e.breaker_array
        states[i, 2] = 1.0 if e.current_player == 1 else 0.0
        
    states = states.reshape(n, 3, size, size)
    return states

def encode_even_faster(envs):
    n = len(envs)
    size = 13
    states = np.empty((n, 3, 169), dtype=np.float32)
    
    # Just grab lists and convert
    states[:, 0] = [e.maker_array for e in envs]
    states[:, 1] = [e.breaker_array for e in envs]
    cp = np.array([e.current_player for e in envs])
    states[:, 2] = (cp == 1)[:, None]
    
    return states.reshape(n, 3, size, size)

t0 = time.time()
for _ in range(1000):
    encode_new(envs)
print("New:", time.time() - t0)

t0 = time.time()
for _ in range(1000):
    encode_even_faster(envs)
print("Even Faster:", time.time() - t0)

