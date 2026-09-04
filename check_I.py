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

def get_all_isometries(n):
    return [
        [(i, 0) for i in range(n)],
        [(0, i) for i in range(n)]
    ]

def is_paving_loser(isometries, paving_fn):
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

for n in range(5, 8):
    iso = get_all_isometries(n)
    defeated_by = []
    for name, fn in pavings.items():
        if is_paving_loser(iso, fn):
            defeated_by.append(name)
    print(f"I_{n} is defeated by: {defeated_by}")
