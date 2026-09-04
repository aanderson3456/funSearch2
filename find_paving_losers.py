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
                    
                    # Canonicalize
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

# Pavings
def h_paving(x, y):
    return (x+1, y) if x % 2 == 0 else (x-1, y)

def v_paving(x, y):
    return (x, y+1) if y % 2 == 0 else (x, y-1)

# Diagonal brick paving
def brick_paving(x, y):
    if y % 2 == 0:
        return (x+1, y) if x % 2 == 0 else (x-1, y)
    else:
        return (x+1, y) if x % 2 == 1 else (x-1, y)

def is_paving_loser(poly, paving_fn):
    # To be a paving loser, EVERY isometry must contain a domino under EVERY translation.
    # Actually, a tiling is periodic. For H-paving, period is (2,1).
    # We can just check translations within the fundamental domain.
    # For H-paving, fundamental domain is (x%2, 0).
    isometries = get_all_isometries(poly)
    for iso in isometries:
        # Check all possible shifts relative to the paving
        # Since paving_fn might have period (2,2), we check shifts in [0,1] x [0,1]
        for dx in range(2):
            for dy in range(2):
                shifted = [(x+dx, y+dy) for x, y in iso]
                
                # Check if this shifted instance contains at least one domino
                contains_domino = False
                for c in shifted:
                    paired = paving_fn(c[0], c[1])
                    if paired in shifted:
                        contains_domino = True
                        break
                
                if not contains_domino:
                    return False
    return True

all_losers = {}
for i in range(1, 8):
    polys = generate_polyominoes(i)
    losers_h = []
    losers_v = []
    losers_brick = []
    
    for p in polys:
        if is_paving_loser(p, h_paving): losers_h.append(p)
        if is_paving_loser(p, v_paving): losers_v.append(p)
        if is_paving_loser(p, brick_paving): losers_brick.append(p)
        
    all_losers[i] = {
        "total": len(polys),
        "h": len(losers_h),
        "v": len(losers_v),
        "brick": len(losers_brick)
    }
    print(f"n={i}: {len(polys)} polys. H-losers={len(losers_h)}, V={len(losers_v)}, Brick={len(losers_brick)}")
