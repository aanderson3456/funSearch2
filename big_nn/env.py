import numpy as np

class SnakyEnv:
    def __init__(self, size=13):
        self.size = size
        self.maker_board = 0
        self.breaker_board = 0
        self.current_player = 1 # 1 for Maker, -1 for Breaker
        self.win_masks = self._generate_win_masks()
        self.done = False
        self.winner = 0

    def _normalize(self, shape):
        min_x = min(x for x, y in shape)
        min_y = min(y for x, y in shape)
        return [(x - min_x, y - min_y) for x, y in shape]

    def _get_orientations(self, shape):
        orientations = []
        current = shape
        for _ in range(4):
            current = [(-y, x) for x, y in current]
            orientations.append(self._normalize(current))
            reflected = [(-x, y) for x, y in current]
            orientations.append(self._normalize(reflected))
        
        unique = []
        seen = set()
        for o in orientations:
            o.sort()
            t = tuple(o)
            if t not in seen:
                seen.add(t)
                unique.append(o)
        return unique

    def _generate_win_masks(self):
        # The Snakey Hexomino
        base_shape = [(0,0), (1,0), (2,0), (3,0), (3,1), (4,1)]
        orientations = self._get_orientations(base_shape)
        masks = []
        
        for o in orientations:
            max_x = max(x for x, y in o)
            max_y = max(y for x, y in o)
            
            for dx in range(self.size - max_x):
                for dy in range(self.size - max_y):
                    mask = 0
                    for x, y in o:
                        pos = (dy + y) * self.size + (dx + x)
                        mask |= (1 << pos)
                    masks.append(mask)
        return masks

    def get_legal_moves(self):
        occupied = self.maker_board | self.breaker_board
        return [i for i in range(self.size * self.size) if not (occupied & (1 << i))]
        
    def step(self, move):
        move = int(move)
        if self.done:
            return self.done, self.winner
            
        if self.current_player == 1:
            self.maker_board |= (1 << move)
        else:
            self.breaker_board |= (1 << move)
            
        # Check win for Maker
        for mask in self.win_masks:
            if (self.maker_board & mask) == mask:
                self.done = True
                self.winner = 1
                return self.done, self.winner
                
        # Check draw (board full)
        if (self.maker_board | self.breaker_board) == ((1 << (self.size * self.size)) - 1):
            self.done = True
            self.winner = 0
            return self.done, self.winner
            
        self.current_player *= -1
        return self.done, self.winner
        
    def reset(self):
        self.maker_board = 0
        self.breaker_board = 0
        self.current_player = 1
        self.done = False
        self.winner = 0
        return self
        
    def render(self):
        board = np.zeros((self.size, self.size), dtype=str)
        board[:] = '.'
        for i in range(self.size * self.size):
            y = i // self.size
            x = i % self.size
            if self.maker_board & (1 << i):
                board[y, x] = 'M'
            elif self.breaker_board & (1 << i):
                board[y, x] = 'B'
                
        for row in board:
            print(" ".join(row))
        print(f"Current Player: {'Maker' if self.current_player == 1 else 'Breaker'}")

    def _arr_to_bitboard(self, arr):
        bb = 0
        for y in range(self.size):
            for x in range(self.size):
                if arr[y, x]:
                    bb |= (1 << (y * self.size + x))
        return bb

    def get_symmetries(self, maker_board, breaker_board, policy):
        """
        Returns all 8 D4 symmetries for a given state and its policy.
        """
        mb_arr = np.zeros((self.size, self.size), dtype=np.int8)
        bb_arr = np.zeros((self.size, self.size), dtype=np.int8)
        
        for i in range(self.size * self.size):
            y, x = divmod(i, self.size)
            if maker_board & (1 << i):
                mb_arr[y, x] = 1
            if breaker_board & (1 << i):
                bb_arr[y, x] = 1
                
        pi_arr = np.array(policy).reshape(self.size, self.size)
        
        symmetries = []
        for i in range(4):
            mb_rot = np.rot90(mb_arr, i)
            bb_rot = np.rot90(bb_arr, i)
            pi_rot = np.rot90(pi_arr, i)
            symmetries.append((self._arr_to_bitboard(mb_rot), self._arr_to_bitboard(bb_rot), pi_rot.flatten().tolist()))
            
            mb_flip = np.fliplr(mb_rot)
            bb_flip = np.fliplr(bb_rot)
            pi_flip = np.fliplr(pi_rot)
            symmetries.append((self._arr_to_bitboard(mb_flip), self._arr_to_bitboard(bb_flip), pi_flip.flatten().tolist()))
            
        return symmetries
