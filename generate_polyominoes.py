def get_neighbors(cell):
    x, y = cell
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

def generate_polyominoes(n):
    if n == 1:
        return {frozenset([(0, 0)])}
    
    prev = generate_polyominoes(n - 1)
    current = set()
    
    for poly in prev:
        for cell in poly:
            for neighbor in get_neighbors(cell):
                if neighbor not in poly:
                    new_poly = set(poly)
                    new_poly.add(neighbor)
                    
                    # Normalize
                    min_x = min(c[0] for c in new_poly)
                    min_y = min(c[1] for c in new_poly)
                    norm_poly = frozenset(tuple(sorted((c[0] - min_x, c[1] - min_y) for c in new_poly)))
                    
                    # Canonicalize over rotations and reflections
                    canonical = norm_poly
                    for rot in range(4):
                        for ref in [1, -1]:
                            trans = [(c[0]*ref, c[1]) for c in norm_poly]
                            for _ in range(rot):
                                trans = [(c[1], -c[0]) for c in trans]
                            mn_x = min(c[0] for c in trans)
                            mn_y = min(c[1] for c in trans)
                            trans_norm = frozenset(tuple(sorted((c[0] - mn_x, c[1] - mn_y) for c in trans)))
                            if hash(trans_norm) < hash(canonical):  # Just a consistent way to pick one
                                canonical = trans_norm
                    
                    current.add(canonical)
    return current

for i in range(1, 8):
    polys = generate_polyominoes(i)
    print(f"n={i}: {len(polys)} polyominoes")
