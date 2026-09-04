import Mathlib

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
