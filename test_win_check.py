import numpy as np
import time

# Method 1: NumPy
size = 13
wm0 = np.random.randint(0, 2**63, 880, dtype=np.uint64)
wm1 = np.random.randint(0, 2**63, 880, dtype=np.uint64)
wm2 = np.random.randint(0, 2**63, 880, dtype=np.uint64)

def check_numpy(m0, m1, m2):
    matched = ((wm0 & m0) == wm0) & \
              ((wm1 & m1) == wm1) & \
              ((wm2 & m2) == wm2)
    return np.any(matched)

# Method 2: Pure Python Integers
win_masks = [int(w0) | (int(w1) << 64) | (int(w2) << 128) for w0, w1, w2 in zip(wm0, wm1, wm2)]

def check_python(board):
    for m in win_masks:
        if (board & m) == m:
            return True
    return False

# Benchmark
m0, m1, m2 = int(wm0[0]), int(wm1[0]), int(wm2[0])
board = m0 | (m1 << 64) | (m2 << 128)

t0 = time.time()
for _ in range(25000):
    check_numpy(m0, m1, m2)
print("NumPy:", time.time() - t0)

t0 = time.time()
for _ in range(25000):
    check_python(board)
print("Python:", time.time() - t0)

