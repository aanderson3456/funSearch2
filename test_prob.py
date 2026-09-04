import numpy as np

visits = np.zeros(169, dtype=np.float32)
for i in range(100):
    visits[np.random.randint(0, 169)] += 1

probs = np.zeros(169)
for i in range(169):
    probs[i] = visits[i] / 100

print(probs.sum())
try:
    np.random.choice(169, p=probs)
    print("Choice succeeded")
except Exception as e:
    print("Choice failed:", e)

# Test with normalization
probs = probs / np.sum(probs)
try:
    np.random.choice(169, p=probs)
    print("Choice succeeded after norm")
except Exception as e:
    print("Choice failed after norm:", e)

