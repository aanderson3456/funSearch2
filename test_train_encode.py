import numpy as np
import time

batch_size = 512
data = [(np.random.randint(0, 2**63), np.random.randint(0, 2**63), 1, np.zeros(169), 1.0) for _ in range(batch_size)]

def parse_old(data):
    states = np.zeros((batch_size, 3, 13, 13), dtype=np.float32)
    for i, (mb, bb, cp, p, v) in enumerate(data):
        for bit in range(169):
            y, x = divmod(bit, 13)
            if mb & (1 << bit):
                states[i, 0, y, x] = 1.0
            if bb & (1 << bit):
                states[i, 1, y, x] = 1.0
        states[i, 2, :, :] = 1.0 if cp == 1 else 0.0

def parse_new(data):
    states = np.zeros((batch_size, 3, 169), dtype=np.float32)
    mb_arr = np.array([item[0] for item in data], dtype=object)
    bb_arr = np.array([item[1] for item in data], dtype=object)
    shifts = 1 << np.arange(169, dtype=object)
    
    states[:, 0, :] = (mb_arr[:, None] & shifts) != 0
    states[:, 1, :] = (bb_arr[:, None] & shifts) != 0
    cp = np.array([item[2] for item in data])
    states[:, 2, :] = (cp == 1)[:, None]
    states = states.reshape((batch_size, 3, 13, 13))

t0 = time.time()
for _ in range(100):
    parse_old(data)
print("Old:", time.time() - t0)

t0 = time.time()
for _ in range(100):
    parse_new(data)
print("New:", time.time() - t0)

