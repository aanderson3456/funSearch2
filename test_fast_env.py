import time
import numpy as np
from big_nn.env import SnakyEnv

class FastSnakyEnv(SnakyEnv):
    def __init__(self, size=13):
        super().__init__(size)
        self.occupied_array = np.zeros(size * size, dtype=bool)
        
        # Precompute split win masks
        self.wm0 = np.array([m & 0xFFFFFFFFFFFFFFFF for m in self.win_masks], dtype=np.uint64)
        self.wm1 = np.array([(m >> 64) & 0xFFFFFFFFFFFFFFFF for m in self.win_masks], dtype=np.uint64)
        self.wm2 = np.array([(m >> 128) & 0xFFFFFFFFFFFFFFFF for m in self.win_masks], dtype=np.uint64)
        
    def get_legal_moves(self):
        return np.where(~self.occupied_array)[0].tolist()
        
    def step(self, move):
        move = int(move)
        if self.done:
            return self.done, self.winner
            
        self.occupied_array[move] = True
        
        if self.current_player == 1:
            self.maker_board |= (1 << move)
            
            # Fast win check ONLY if Maker moved
            m0 = self.maker_board & 0xFFFFFFFFFFFFFFFF
            m1 = (self.maker_board >> 64) & 0xFFFFFFFFFFFFFFFF
            m2 = (self.maker_board >> 128) & 0xFFFFFFFFFFFFFFFF
            
            matched = ((self.wm0 & m0) == self.wm0) & \
                      ((self.wm1 & m1) == self.wm1) & \
                      ((self.wm2 & m2) == self.wm2)
                      
            if np.any(matched):
                self.done = True
                self.winner = 1
                return self.done, self.winner
        else:
            self.breaker_board |= (1 << move)
            
        if (self.maker_board | self.breaker_board) == ((1 << (self.size * self.size)) - 1):
            self.done = True
            self.winner = 0
            return self.done, self.winner
            
        self.current_player *= -1
        return self.done, self.winner

env1 = SnakyEnv(13)
env2 = FastSnakyEnv(13)

# Benchmark get_legal_moves
t0 = time.time()
for _ in range(10000):
    env1.get_legal_moves()
print("Slow get_legal_moves:", time.time()-t0)

t0 = time.time()
for _ in range(10000):
    env2.get_legal_moves()
print("Fast get_legal_moves:", time.time()-t0)

# Benchmark step (maker win check)
env1.maker_board = (1<<169)-1 # all 1s
env2.maker_board = (1<<169)-1 
t0 = time.time()
for _ in range(10000):
    env1.step(0) # it will trigger win check
print("Slow step:", time.time()-t0)

t0 = time.time()
for _ in range(10000):
    env2.step(0)
print("Fast step:", time.time()-t0)
