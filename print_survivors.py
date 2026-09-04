import json

def get_neighbors(cell):
    x, y = cell
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

def generate_polyominoes(n):
    if n == 1:
        return [frozenset([(0, 0)])]
    
    prev = generate_polyominoes(n - 1)
    current = set()
    
    for poly in prev:
        for cell in poly:
            for neighbor in get_neighbors(cell):
                if neighbor not in poly:
                    new_poly = set(poly)
                    new_poly.add(neighbor)
                    
                    min_x = min(c[0] for c in new_poly)
                    min_y = min(c[1] for c in new_poly)
                    norm_poly = frozenset(tuple(sorted((c[0] - min_x, c[1] - min_y) for c in new_poly)))
                    
                    canonical_str = ""
                    for rot in range(4):
                        for ref in [1, -1]:
                            trans = [(c[0]*ref, c[1]) for c in norm_poly]
                            for _ in range(rot):
                                trans = [(c[1], -c[0]) for c in trans]
                            mn_x = min(c[0] for c in trans)
                            mn_y = min(c[1] for c in trans)
                            trans_norm = tuple(sorted((c[0] - mn_x, c[1] - mn_y) for c in trans))
                            s = str(trans_norm)
                            if canonical_str == "" or s < canonical_str:
                                canonical_str = s
                                canonical = frozenset(trans_norm)
                    current.add(canonical)
    return list(current)

def get_all_isometries(poly):
    isos = set()
    for rot in range(4):
        for ref in [1, -1]:
            trans = [(c[0]*ref, c[1]) for c in poly]
            for _ in range(rot):
                trans = [(c[1], -c[0]) for c in trans]
            mn_x = min(c[0] for c in trans)
            mn_y = min(c[1] for c in trans)
            trans_norm = tuple(sorted((c[0] - mn_x, c[1] - mn_y) for c in trans))
            isos.add(trans_norm)
    return list(isos)

def h_paving(x, y): return (x+1, y) if x % 2 == 0 else (x-1, y)
def v_paving(x, y): return (x, y+1) if y % 2 == 0 else (x, y-1)
def brick_paving(x, y):
    if y % 2 == 0: return (x+1, y) if x % 2 == 0 else (x-1, y)
    else: return (x+1, y) if x % 2 == 1 else (x-1, y)
def checkerboard_paving(x, y):
    bx, by = x // 2, y // 2
    if (bx + by) % 2 == 0: return h_paving(x, y)
    else: return v_paving(x, y)
def stripes_h_paving(x, y):
    by = y // 2
    if by % 2 == 0: return h_paving(x, y)
    else: return v_paving(x, y)
def stripes_v_paving(x, y):
    bx = x // 2
    if bx % 2 == 0: return h_paving(x, y)
    else: return v_paving(x, y)

pavings = {
    "PavingH": h_paving,
    "PavingV": v_paving,
    "PavingBrick": brick_paving,
    "PavingCheckerboard": checkerboard_paving,
    "PavingStripesH": stripes_h_paving,
    "PavingStripesV": stripes_v_paving
}

def is_paving_loser(poly, paving_fn):
    isometries = get_all_isometries(poly)
    for iso in isometries:
        for dx in range(4):
            for dy in range(4):
                shifted = [(x+dx, y+dy) for x, y in iso]
                contains_domino = False
                for c in shifted:
                    paired = paving_fn(c[0], c[1])
                    if paired in shifted:
                        contains_domino = True
                        break
                if not contains_domino:
                    return False
    return True

def print_poly(p):
    max_x = max(c[0] for c in p)
    max_y = max(c[1] for c in p)
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in p:
        grid[y][x] = "█"
    for row in grid:
        print("".join(row))
    print()

for n in range(4, 8):
    polys = generate_polyominoes(n)
    for p in polys:
        is_loser = False
        for name, fn in pavings.items():
            if is_paving_loser(p, fn):
                is_loser = True
                break
        if not is_loser:
            print(f"n={n} Survivor:")
            print_poly(p)
