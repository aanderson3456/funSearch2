import json
import os

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

core_lean = """import Mathlib

/-!
# Polyomino Paving Framework
Defines the finite representations of Polyominoes and tiling paving logic.
-/

abbrev Point := Int × Int

abbrev Polyomino := List Point

abbrev Paving := Point → Point

def PavingH (p : Point) : Point := 
  if p.1 % 2 == 0 then (p.1 + 1, p.2) else (p.1 - 1, p.2)

def PavingV (p : Point) : Point := 
  if p.2 % 2 == 0 then (p.1, p.2 + 1) else (p.1, p.2 - 1)

def PavingBrick (p : Point) : Point := 
  if p.2 % 2 == 0 then
    if p.1 % 2 == 0 then (p.1 + 1, p.2) else (p.1 - 1, p.2)
  else
    if p.1 % 2 == 1 then (p.1 + 1, p.2) else (p.1 - 1, p.2)

def PavingCheckerboard (p : Point) : Point :=
  if ((p.1 / 2) + (p.2 / 2)) % 2 == 0 then
    if p.1 % 2 == 0 then (p.1 + 1, p.2) else (p.1 - 1, p.2)
  else
    if p.2 % 2 == 0 then (p.1, p.2 + 1) else (p.1, p.2 - 1)

def PavingStripesH (p : Point) : Point :=
  if (p.2 / 2) % 2 == 0 then
    if p.1 % 2 == 0 then (p.1 + 1, p.2) else (p.1 - 1, p.2)
  else
    if p.2 % 2 == 0 then (p.1, p.2 + 1) else (p.1, p.2 - 1)

def PavingStripesV (p : Point) : Point :=
  if (p.1 / 2) % 2 == 0 then
    if p.1 % 2 == 0 then (p.1 + 1, p.2) else (p.1 - 1, p.2)
  else
    if p.2 % 2 == 0 then (p.1, p.2 + 1) else (p.1, p.2 - 1)

def contains_domino (P : Polyomino) (f : Paving) (dx dy : Int) : Bool :=
  P.any (fun p => 
    P.contains ((f (p.1 + dx, p.2 + dy)).1 - dx, (f (p.1 + dx, p.2 + dy)).2 - dy)
  )

def defeated_by (P : Polyomino) (f : Paving) : Bool :=
  let shifts := [(0,0), (1,0), (2,0), (3,0), 
                 (0,1), (1,1), (2,1), (3,1),
                 (0,2), (1,2), (2,2), (3,2),
                 (0,3), (1,3), (2,3), (3,3)]
  shifts.all (fun s => contains_domino P f s.1 s.2)
"""

os.makedirs("LeanProofs/FunSizzy", exist_ok=True)
with open("LeanProofs/FunSizzy/Core.lean", "w") as f:
    f.write(core_lean)

losers_lean = """import FunSizzy.Core

/-!
# Polyomino Paving Losers
Contains mechanically generated proofs that polyominoes are defeated by pavings.
-/

"""

idx = 1
for n in range(1, 8):
    polys = generate_polyominoes(n)
    for p in polys:
        winning_paving = None
        for name, fn in pavings.items():
            if is_paving_loser(p, fn):
                winning_paving = name
                break
                
        if winning_paving:
            isometries = get_all_isometries(p)
            for iso_i, iso in enumerate(isometries):
                pts = ", ".join([f"({x},{y})" for x, y in iso])
                losers_lean += f"def poly_{idx}_iso_{iso_i} : Polyomino := [{pts}]\n"
                losers_lean += f"theorem poly_{idx}_iso_{iso_i}_loser : defeated_by poly_{idx}_iso_{iso_i} {winning_paving} = true := by {{\n  decide\n}}\n\n"
            idx += 1

with open("LeanProofs/FunSizzy/Losers.lean", "w") as f:
    f.write(losers_lean)

print(f"Generated Lean code for {idx-1} paving losers!")
