import FunSizzy.Core

/-!
# Polyomino Paving Losers
Contains mechanically generated proofs that polyominoes are defeated by pavings.
-/

def poly_1_iso_0 : Polyomino := [(0,0), (0,1), (1,0), (1,1)]
theorem poly_1_iso_0_loser : defeated_by poly_1_iso_0 PavingBrick = true := by {
  decide
}

def poly_2_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,1)]
theorem poly_2_iso_0_loser : defeated_by poly_2_iso_0 PavingH = true := by {
  decide
}

def poly_2_iso_1 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2)]
theorem poly_2_iso_1_loser : defeated_by poly_2_iso_1 PavingH = true := by {
  decide
}

def poly_2_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0)]
theorem poly_2_iso_2_loser : defeated_by poly_2_iso_2 PavingH = true := by {
  decide
}

def poly_2_iso_3 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,2)]
theorem poly_2_iso_3_loser : defeated_by poly_2_iso_3 PavingH = true := by {
  decide
}

def poly_3_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4)]
theorem poly_3_iso_0_loser : defeated_by poly_3_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_3_iso_1 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (4,0)]
theorem poly_3_iso_1_loser : defeated_by poly_3_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_4_iso_0 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2)]
theorem poly_4_iso_0_loser : defeated_by poly_4_iso_0 PavingBrick = true := by {
  decide
}

def poly_4_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,1)]
theorem poly_4_iso_1_loser : defeated_by poly_4_iso_1 PavingBrick = true := by {
  decide
}

def poly_4_iso_2 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2)]
theorem poly_4_iso_2_loser : defeated_by poly_4_iso_2 PavingBrick = true := by {
  decide
}

def poly_4_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1)]
theorem poly_4_iso_3_loser : defeated_by poly_4_iso_3 PavingBrick = true := by {
  decide
}

def poly_4_iso_4 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,0)]
theorem poly_4_iso_4_loser : defeated_by poly_4_iso_4 PavingBrick = true := by {
  decide
}

def poly_4_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2)]
theorem poly_4_iso_5_loser : defeated_by poly_4_iso_5 PavingBrick = true := by {
  decide
}

def poly_4_iso_6 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1)]
theorem poly_4_iso_6_loser : defeated_by poly_4_iso_6 PavingBrick = true := by {
  decide
}

def poly_4_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1)]
theorem poly_4_iso_7_loser : defeated_by poly_4_iso_7 PavingBrick = true := by {
  decide
}

def poly_5_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,1)]
theorem poly_5_iso_0_loser : defeated_by poly_5_iso_0 PavingH = true := by {
  decide
}

def poly_6_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2)]
theorem poly_6_iso_0_loser : defeated_by poly_6_iso_0 PavingH = true := by {
  decide
}

def poly_6_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,1)]
theorem poly_6_iso_1_loser : defeated_by poly_6_iso_1 PavingH = true := by {
  decide
}

def poly_6_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,1)]
theorem poly_6_iso_2_loser : defeated_by poly_6_iso_2 PavingH = true := by {
  decide
}

def poly_6_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0)]
theorem poly_6_iso_3_loser : defeated_by poly_6_iso_3 PavingH = true := by {
  decide
}

def poly_6_iso_4 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,1)]
theorem poly_6_iso_4_loser : defeated_by poly_6_iso_4 PavingH = true := by {
  decide
}

def poly_6_iso_5 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1)]
theorem poly_6_iso_5_loser : defeated_by poly_6_iso_5 PavingH = true := by {
  decide
}

def poly_6_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,2)]
theorem poly_6_iso_6_loser : defeated_by poly_6_iso_6 PavingH = true := by {
  decide
}

def poly_6_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,1)]
theorem poly_6_iso_7_loser : defeated_by poly_6_iso_7 PavingH = true := by {
  decide
}

def poly_7_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2)]
theorem poly_7_iso_0_loser : defeated_by poly_7_iso_0 PavingH = true := by {
  decide
}

def poly_7_iso_1 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0)]
theorem poly_7_iso_1_loser : defeated_by poly_7_iso_1 PavingH = true := by {
  decide
}

def poly_7_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,2)]
theorem poly_7_iso_2_loser : defeated_by poly_7_iso_2 PavingH = true := by {
  decide
}

def poly_7_iso_3 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1)]
theorem poly_7_iso_3_loser : defeated_by poly_7_iso_3 PavingH = true := by {
  decide
}

def poly_8_iso_0 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,0)]
theorem poly_8_iso_0_loser : defeated_by poly_8_iso_0 PavingH = true := by {
  decide
}

def poly_8_iso_1 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1)]
theorem poly_8_iso_1_loser : defeated_by poly_8_iso_1 PavingH = true := by {
  decide
}

def poly_8_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,2)]
theorem poly_8_iso_2_loser : defeated_by poly_8_iso_2 PavingH = true := by {
  decide
}

def poly_8_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2)]
theorem poly_8_iso_3_loser : defeated_by poly_8_iso_3 PavingH = true := by {
  decide
}

def poly_9_iso_0 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2)]
theorem poly_9_iso_0_loser : defeated_by poly_9_iso_0 PavingH = true := by {
  decide
}

def poly_9_iso_1 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2)]
theorem poly_9_iso_1_loser : defeated_by poly_9_iso_1 PavingH = true := by {
  decide
}

def poly_9_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,2)]
theorem poly_9_iso_2_loser : defeated_by poly_9_iso_2 PavingH = true := by {
  decide
}

def poly_9_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (2,0)]
theorem poly_9_iso_3_loser : defeated_by poly_9_iso_3 PavingH = true := by {
  decide
}

def poly_10_iso_0 : Polyomino := [(0,1), (0,2), (0,3), (1,1), (2,0), (2,1)]
theorem poly_10_iso_0_loser : defeated_by poly_10_iso_0 PavingH = true := by {
  decide
}

def poly_10_iso_1 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (3,0)]
theorem poly_10_iso_1_loser : defeated_by poly_10_iso_1 PavingH = true := by {
  decide
}

def poly_10_iso_2 : Polyomino := [(0,2), (0,3), (1,2), (2,0), (2,1), (2,2)]
theorem poly_10_iso_2_loser : defeated_by poly_10_iso_2 PavingH = true := by {
  decide
}

def poly_10_iso_3 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (2,3)]
theorem poly_10_iso_3_loser : defeated_by poly_10_iso_3 PavingH = true := by {
  decide
}

def poly_10_iso_4 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (3,0)]
theorem poly_10_iso_4_loser : defeated_by poly_10_iso_4 PavingH = true := by {
  decide
}

def poly_10_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,2), (3,2)]
theorem poly_10_iso_5_loser : defeated_by poly_10_iso_5 PavingH = true := by {
  decide
}

def poly_10_iso_6 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (3,2)]
theorem poly_10_iso_6_loser : defeated_by poly_10_iso_6 PavingH = true := by {
  decide
}

def poly_10_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,2), (2,3)]
theorem poly_10_iso_7_loser : defeated_by poly_10_iso_7 PavingH = true := by {
  decide
}

def poly_11_iso_0 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (3,0), (3,1)]
theorem poly_11_iso_0_loser : defeated_by poly_11_iso_0 PavingBrick = true := by {
  decide
}

def poly_11_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,0), (3,1)]
theorem poly_11_iso_1_loser : defeated_by poly_11_iso_1 PavingBrick = true := by {
  decide
}

def poly_11_iso_2 : Polyomino := [(0,0), (0,3), (1,0), (1,1), (1,2), (1,3)]
theorem poly_11_iso_2_loser : defeated_by poly_11_iso_2 PavingBrick = true := by {
  decide
}

def poly_11_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,3)]
theorem poly_11_iso_3_loser : defeated_by poly_11_iso_3 PavingBrick = true := by {
  decide
}

def poly_12_iso_0 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (2,3)]
theorem poly_12_iso_0_loser : defeated_by poly_12_iso_0 PavingH = true := by {
  decide
}

def poly_12_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (3,0)]
theorem poly_12_iso_1_loser : defeated_by poly_12_iso_1 PavingH = true := by {
  decide
}

def poly_12_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,1), (2,1)]
theorem poly_12_iso_2_loser : defeated_by poly_12_iso_2 PavingH = true := by {
  decide
}

def poly_12_iso_3 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (3,0)]
theorem poly_12_iso_3_loser : defeated_by poly_12_iso_3 PavingH = true := by {
  decide
}

def poly_12_iso_4 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (2,3)]
theorem poly_12_iso_4_loser : defeated_by poly_12_iso_4 PavingH = true := by {
  decide
}

def poly_12_iso_5 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,2), (3,2)]
theorem poly_12_iso_5_loser : defeated_by poly_12_iso_5 PavingH = true := by {
  decide
}

def poly_12_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,2), (2,2)]
theorem poly_12_iso_6_loser : defeated_by poly_12_iso_6 PavingH = true := by {
  decide
}

def poly_12_iso_7 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (3,2)]
theorem poly_12_iso_7_loser : defeated_by poly_12_iso_7 PavingH = true := by {
  decide
}

def poly_13_iso_0 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (3,0)]
theorem poly_13_iso_0_loser : defeated_by poly_13_iso_0 PavingH = true := by {
  decide
}

def poly_13_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3)]
theorem poly_13_iso_1_loser : defeated_by poly_13_iso_1 PavingH = true := by {
  decide
}

def poly_13_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (3,2)]
theorem poly_13_iso_2_loser : defeated_by poly_13_iso_2 PavingH = true := by {
  decide
}

def poly_13_iso_3 : Polyomino := [(0,2), (0,3), (1,1), (1,2), (2,0), (2,1)]
theorem poly_13_iso_3_loser : defeated_by poly_13_iso_3 PavingH = true := by {
  decide
}

def poly_14_iso_0 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_14_iso_0_loser : defeated_by poly_14_iso_0 PavingH = true := by {
  decide
}

def poly_14_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,1), (3,1)]
theorem poly_14_iso_1_loser : defeated_by poly_14_iso_1 PavingH = true := by {
  decide
}

def poly_14_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_14_iso_2_loser : defeated_by poly_14_iso_2 PavingH = true := by {
  decide
}

def poly_14_iso_3 : Polyomino := [(0,1), (1,1), (2,1), (3,0), (3,1), (3,2)]
theorem poly_14_iso_3_loser : defeated_by poly_14_iso_3 PavingH = true := by {
  decide
}

def poly_15_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_15_iso_0_loser : defeated_by poly_15_iso_0 PavingH = true := by {
  decide
}

def poly_15_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (3,1)]
theorem poly_15_iso_1_loser : defeated_by poly_15_iso_1 PavingH = true := by {
  decide
}

def poly_15_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_15_iso_2_loser : defeated_by poly_15_iso_2 PavingH = true := by {
  decide
}

def poly_15_iso_3 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (3,1)]
theorem poly_15_iso_3_loser : defeated_by poly_15_iso_3 PavingH = true := by {
  decide
}

def poly_16_iso_0 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (2,0)]
theorem poly_16_iso_0_loser : defeated_by poly_16_iso_0 PavingH = true := by {
  decide
}

def poly_16_iso_1 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (2,2)]
theorem poly_16_iso_1_loser : defeated_by poly_16_iso_1 PavingH = true := by {
  decide
}

def poly_16_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (2,0), (2,1), (2,2)]
theorem poly_16_iso_2_loser : defeated_by poly_16_iso_2 PavingH = true := by {
  decide
}

def poly_16_iso_3 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (2,2)]
theorem poly_16_iso_3_loser : defeated_by poly_16_iso_3 PavingH = true := by {
  decide
}

def poly_16_iso_4 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (2,2)]
theorem poly_16_iso_4_loser : defeated_by poly_16_iso_4 PavingH = true := by {
  decide
}

def poly_16_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,1), (2,2)]
theorem poly_16_iso_5_loser : defeated_by poly_16_iso_5 PavingH = true := by {
  decide
}

def poly_16_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,0), (2,1)]
theorem poly_16_iso_6_loser : defeated_by poly_16_iso_6 PavingH = true := by {
  decide
}

def poly_16_iso_7 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (2,2)]
theorem poly_16_iso_7_loser : defeated_by poly_16_iso_7 PavingH = true := by {
  decide
}

def poly_17_iso_0 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_17_iso_0_loser : defeated_by poly_17_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_17_iso_1 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,1), (4,1)]
theorem poly_17_iso_1_loser : defeated_by poly_17_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_17_iso_2 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,0), (4,0)]
theorem poly_17_iso_2_loser : defeated_by poly_17_iso_2 PavingCheckerboard = true := by {
  decide
}

def poly_17_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,2)]
theorem poly_17_iso_3_loser : defeated_by poly_17_iso_3 PavingCheckerboard = true := by {
  decide
}

def poly_18_iso_0 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,0), (3,0)]
theorem poly_18_iso_0_loser : defeated_by poly_18_iso_0 PavingBrick = true := by {
  decide
}

def poly_18_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (1,3)]
theorem poly_18_iso_1_loser : defeated_by poly_18_iso_1 PavingBrick = true := by {
  decide
}

def poly_18_iso_2 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,0), (3,1)]
theorem poly_18_iso_2_loser : defeated_by poly_18_iso_2 PavingBrick = true := by {
  decide
}

def poly_18_iso_3 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,0), (3,1)]
theorem poly_18_iso_3_loser : defeated_by poly_18_iso_3 PavingBrick = true := by {
  decide
}

def poly_18_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,1)]
theorem poly_18_iso_4_loser : defeated_by poly_18_iso_4 PavingBrick = true := by {
  decide
}

def poly_18_iso_5 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,1), (3,1)]
theorem poly_18_iso_5_loser : defeated_by poly_18_iso_5 PavingBrick = true := by {
  decide
}

def poly_18_iso_6 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (1,3)]
theorem poly_18_iso_6_loser : defeated_by poly_18_iso_6 PavingBrick = true := by {
  decide
}

def poly_18_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,2), (1,3)]
theorem poly_18_iso_7_loser : defeated_by poly_18_iso_7 PavingBrick = true := by {
  decide
}

def poly_19_iso_0 : Polyomino := [(0,3), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_19_iso_0_loser : defeated_by poly_19_iso_0 PavingH = true := by {
  decide
}

def poly_19_iso_1 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,0), (3,0)]
theorem poly_19_iso_1_loser : defeated_by poly_19_iso_1 PavingH = true := by {
  decide
}

def poly_19_iso_2 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (2,0)]
theorem poly_19_iso_2_loser : defeated_by poly_19_iso_2 PavingH = true := by {
  decide
}

def poly_19_iso_3 : Polyomino := [(0,2), (1,2), (2,1), (2,2), (3,0), (3,1)]
theorem poly_19_iso_3_loser : defeated_by poly_19_iso_3 PavingH = true := by {
  decide
}

def poly_19_iso_4 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (2,3)]
theorem poly_19_iso_4_loser : defeated_by poly_19_iso_4 PavingH = true := by {
  decide
}

def poly_19_iso_5 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,2), (3,2)]
theorem poly_19_iso_5_loser : defeated_by poly_19_iso_5 PavingH = true := by {
  decide
}

def poly_19_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (2,3)]
theorem poly_19_iso_6_loser : defeated_by poly_19_iso_6 PavingH = true := by {
  decide
}

def poly_19_iso_7 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,1), (3,2)]
theorem poly_19_iso_7_loser : defeated_by poly_19_iso_7 PavingH = true := by {
  decide
}

def poly_20_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,1), (3,1)]
theorem poly_20_iso_0_loser : defeated_by poly_20_iso_0 PavingH = true := by {
  decide
}

def poly_20_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,1)]
theorem poly_20_iso_1_loser : defeated_by poly_20_iso_1 PavingH = true := by {
  decide
}

def poly_20_iso_2 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (3,2)]
theorem poly_20_iso_2_loser : defeated_by poly_20_iso_2 PavingH = true := by {
  decide
}

def poly_20_iso_3 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,1), (3,1)]
theorem poly_20_iso_3_loser : defeated_by poly_20_iso_3 PavingH = true := by {
  decide
}

def poly_20_iso_4 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (3,0)]
theorem poly_20_iso_4_loser : defeated_by poly_20_iso_4 PavingH = true := by {
  decide
}

def poly_20_iso_5 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (2,2)]
theorem poly_20_iso_5_loser : defeated_by poly_20_iso_5 PavingH = true := by {
  decide
}

def poly_20_iso_6 : Polyomino := [(0,1), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_20_iso_6_loser : defeated_by poly_20_iso_6 PavingH = true := by {
  decide
}

def poly_20_iso_7 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,2), (2,3)]
theorem poly_20_iso_7_loser : defeated_by poly_20_iso_7 PavingH = true := by {
  decide
}

def poly_21_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5)]
theorem poly_21_iso_0_loser : defeated_by poly_21_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_21_iso_1 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0)]
theorem poly_21_iso_1_loser : defeated_by poly_21_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_22_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,1), (2,2)]
theorem poly_22_iso_0_loser : defeated_by poly_22_iso_0 PavingH = true := by {
  decide
}

def poly_22_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (2,1)]
theorem poly_22_iso_1_loser : defeated_by poly_22_iso_1 PavingH = true := by {
  decide
}

def poly_22_iso_2 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (2,1)]
theorem poly_22_iso_2_loser : defeated_by poly_22_iso_2 PavingH = true := by {
  decide
}

def poly_22_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (2,1)]
theorem poly_22_iso_3_loser : defeated_by poly_22_iso_3 PavingH = true := by {
  decide
}

def poly_23_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0)]
theorem poly_23_iso_0_loser : defeated_by poly_23_iso_0 PavingH = true := by {
  decide
}

def poly_23_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (2,2)]
theorem poly_23_iso_1_loser : defeated_by poly_23_iso_1 PavingH = true := by {
  decide
}

def poly_23_iso_2 : Polyomino := [(0,1), (0,2), (1,2), (2,0), (2,1), (2,2)]
theorem poly_23_iso_2_loser : defeated_by poly_23_iso_2 PavingH = true := by {
  decide
}

def poly_23_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,1), (2,2)]
theorem poly_23_iso_3_loser : defeated_by poly_23_iso_3 PavingH = true := by {
  decide
}

def poly_23_iso_4 : Polyomino := [(0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]
theorem poly_23_iso_4_loser : defeated_by poly_23_iso_4 PavingH = true := by {
  decide
}

def poly_23_iso_5 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (2,1), (2,2)]
theorem poly_23_iso_5_loser : defeated_by poly_23_iso_5 PavingH = true := by {
  decide
}

def poly_23_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (2,0), (2,1)]
theorem poly_23_iso_6_loser : defeated_by poly_23_iso_6 PavingH = true := by {
  decide
}

def poly_23_iso_7 : Polyomino := [(0,0), (1,0), (1,2), (2,0), (2,1), (2,2)]
theorem poly_23_iso_7_loser : defeated_by poly_23_iso_7 PavingH = true := by {
  decide
}

def poly_24_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,3)]
theorem poly_24_iso_0_loser : defeated_by poly_24_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_24_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (3,1), (4,1)]
theorem poly_24_iso_1_loser : defeated_by poly_24_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_24_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,1)]
theorem poly_24_iso_2_loser : defeated_by poly_24_iso_2 PavingCheckerboard = true := by {
  decide
}

def poly_24_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_24_iso_3_loser : defeated_by poly_24_iso_3 PavingCheckerboard = true := by {
  decide
}

def poly_24_iso_4 : Polyomino := [(0,1), (1,1), (2,1), (3,0), (3,1), (4,1)]
theorem poly_24_iso_4_loser : defeated_by poly_24_iso_4 PavingCheckerboard = true := by {
  decide
}

def poly_24_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (3,0), (4,0)]
theorem poly_24_iso_5_loser : defeated_by poly_24_iso_5 PavingCheckerboard = true := by {
  decide
}

def poly_24_iso_6 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_24_iso_6_loser : defeated_by poly_24_iso_6 PavingCheckerboard = true := by {
  decide
}

def poly_24_iso_7 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (3,1), (4,0)]
theorem poly_24_iso_7_loser : defeated_by poly_24_iso_7 PavingCheckerboard = true := by {
  decide
}

def poly_25_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,3)]
theorem poly_25_iso_0_loser : defeated_by poly_25_iso_0 PavingH = true := by {
  decide
}

def poly_25_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,2), (2,3)]
theorem poly_25_iso_1_loser : defeated_by poly_25_iso_1 PavingH = true := by {
  decide
}

def poly_25_iso_2 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (3,0)]
theorem poly_25_iso_2_loser : defeated_by poly_25_iso_2 PavingH = true := by {
  decide
}

def poly_25_iso_3 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (2,0)]
theorem poly_25_iso_3_loser : defeated_by poly_25_iso_3 PavingH = true := by {
  decide
}

def poly_25_iso_4 : Polyomino := [(0,2), (1,1), (1,2), (2,1), (3,0), (3,1)]
theorem poly_25_iso_4_loser : defeated_by poly_25_iso_4 PavingH = true := by {
  decide
}

def poly_25_iso_5 : Polyomino := [(0,3), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_25_iso_5_loser : defeated_by poly_25_iso_5 PavingH = true := by {
  decide
}

def poly_25_iso_6 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (3,2)]
theorem poly_25_iso_6_loser : defeated_by poly_25_iso_6 PavingH = true := by {
  decide
}

def poly_25_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (3,1), (3,2)]
theorem poly_25_iso_7_loser : defeated_by poly_25_iso_7 PavingH = true := by {
  decide
}

def poly_26_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,1), (1,2)]
theorem poly_26_iso_0_loser : defeated_by poly_26_iso_0 PavingBrick = true := by {
  decide
}

def poly_26_iso_1 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (1,3)]
theorem poly_26_iso_1_loser : defeated_by poly_26_iso_1 PavingBrick = true := by {
  decide
}

def poly_26_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (3,0)]
theorem poly_26_iso_2_loser : defeated_by poly_26_iso_2 PavingBrick = true := by {
  decide
}

def poly_26_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (3,1)]
theorem poly_26_iso_3_loser : defeated_by poly_26_iso_3 PavingBrick = true := by {
  decide
}

def poly_27_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (3,1)]
theorem poly_27_iso_0_loser : defeated_by poly_27_iso_0 PavingH = true := by {
  decide
}

def poly_27_iso_1 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (3,1)]
theorem poly_27_iso_1_loser : defeated_by poly_27_iso_1 PavingH = true := by {
  decide
}

def poly_27_iso_2 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (2,1)]
theorem poly_27_iso_2_loser : defeated_by poly_27_iso_2 PavingH = true := by {
  decide
}

def poly_27_iso_3 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,2)]
theorem poly_27_iso_3_loser : defeated_by poly_27_iso_3 PavingH = true := by {
  decide
}

def poly_27_iso_4 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (3,0)]
theorem poly_27_iso_4_loser : defeated_by poly_27_iso_4 PavingH = true := by {
  decide
}

def poly_27_iso_5 : Polyomino := [(0,2), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_27_iso_5_loser : defeated_by poly_27_iso_5 PavingH = true := by {
  decide
}

def poly_27_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,2), (2,3)]
theorem poly_27_iso_6_loser : defeated_by poly_27_iso_6 PavingH = true := by {
  decide
}

def poly_27_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (3,2)]
theorem poly_27_iso_7_loser : defeated_by poly_27_iso_7 PavingH = true := by {
  decide
}

def poly_28_iso_0 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,1), (3,2)]
theorem poly_28_iso_0_loser : defeated_by poly_28_iso_0 PavingH = true := by {
  decide
}

def poly_28_iso_1 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_28_iso_1_loser : defeated_by poly_28_iso_1 PavingH = true := by {
  decide
}

def poly_28_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,1), (3,1)]
theorem poly_28_iso_2_loser : defeated_by poly_28_iso_2 PavingH = true := by {
  decide
}

def poly_28_iso_3 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_28_iso_3_loser : defeated_by poly_28_iso_3 PavingH = true := by {
  decide
}

def poly_28_iso_4 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,1), (3,1)]
theorem poly_28_iso_4_loser : defeated_by poly_28_iso_4 PavingH = true := by {
  decide
}

def poly_28_iso_5 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_28_iso_5_loser : defeated_by poly_28_iso_5 PavingH = true := by {
  decide
}

def poly_28_iso_6 : Polyomino := [(0,1), (1,1), (2,1), (2,2), (3,0), (3,1)]
theorem poly_28_iso_6_loser : defeated_by poly_28_iso_6 PavingH = true := by {
  decide
}

def poly_28_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_28_iso_7_loser : defeated_by poly_28_iso_7 PavingH = true := by {
  decide
}

def poly_29_iso_0 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (2,2)]
theorem poly_29_iso_0_loser : defeated_by poly_29_iso_0 PavingH = true := by {
  decide
}

def poly_29_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (2,2)]
theorem poly_29_iso_1_loser : defeated_by poly_29_iso_1 PavingH = true := by {
  decide
}

def poly_29_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (2,0)]
theorem poly_29_iso_2_loser : defeated_by poly_29_iso_2 PavingH = true := by {
  decide
}

def poly_29_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (2,2)]
theorem poly_29_iso_3_loser : defeated_by poly_29_iso_3 PavingH = true := by {
  decide
}

def poly_30_iso_0 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,1), (2,2)]
theorem poly_30_iso_0_loser : defeated_by poly_30_iso_0 PavingH = true := by {
  decide
}

def poly_30_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,0), (2,1)]
theorem poly_30_iso_1_loser : defeated_by poly_30_iso_1 PavingH = true := by {
  decide
}

def poly_30_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (2,2)]
theorem poly_30_iso_2_loser : defeated_by poly_30_iso_2 PavingH = true := by {
  decide
}

def poly_30_iso_3 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (2,1)]
theorem poly_30_iso_3_loser : defeated_by poly_30_iso_3 PavingH = true := by {
  decide
}

def poly_31_iso_0 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3)]
theorem poly_31_iso_0_loser : defeated_by poly_31_iso_0 PavingH = true := by {
  decide
}

def poly_31_iso_1 : Polyomino := [(0,3), (1,3), (2,0), (2,1), (2,2), (2,3)]
theorem poly_31_iso_1_loser : defeated_by poly_31_iso_1 PavingH = true := by {
  decide
}

def poly_31_iso_2 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (3,1), (3,2)]
theorem poly_31_iso_2_loser : defeated_by poly_31_iso_2 PavingH = true := by {
  decide
}

def poly_31_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (2,0)]
theorem poly_31_iso_3_loser : defeated_by poly_31_iso_3 PavingH = true := by {
  decide
}

def poly_31_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3)]
theorem poly_31_iso_4_loser : defeated_by poly_31_iso_4 PavingH = true := by {
  decide
}

def poly_31_iso_5 : Polyomino := [(0,2), (1,2), (2,2), (3,0), (3,1), (3,2)]
theorem poly_31_iso_5_loser : defeated_by poly_31_iso_5 PavingH = true := by {
  decide
}

def poly_31_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (2,0), (3,0)]
theorem poly_31_iso_6_loser : defeated_by poly_31_iso_6 PavingH = true := by {
  decide
}

def poly_31_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,2), (3,2)]
theorem poly_31_iso_7_loser : defeated_by poly_31_iso_7 PavingH = true := by {
  decide
}

def poly_32_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,1), (2,2)]
theorem poly_32_iso_0_loser : defeated_by poly_32_iso_0 PavingH = true := by {
  decide
}

def poly_32_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (2,2)]
theorem poly_32_iso_1_loser : defeated_by poly_32_iso_1 PavingH = true := by {
  decide
}

def poly_32_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (2,1)]
theorem poly_32_iso_2_loser : defeated_by poly_32_iso_2 PavingH = true := by {
  decide
}

def poly_32_iso_3 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,1), (2,2)]
theorem poly_32_iso_3_loser : defeated_by poly_32_iso_3 PavingH = true := by {
  decide
}

def poly_32_iso_4 : Polyomino := [(0,1), (0,2), (1,1), (1,2), (2,0), (2,1)]
theorem poly_32_iso_4_loser : defeated_by poly_32_iso_4 PavingH = true := by {
  decide
}

def poly_32_iso_5 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (2,0)]
theorem poly_32_iso_5_loser : defeated_by poly_32_iso_5 PavingH = true := by {
  decide
}

def poly_32_iso_6 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,1), (2,2)]
theorem poly_32_iso_6_loser : defeated_by poly_32_iso_6 PavingH = true := by {
  decide
}

def poly_32_iso_7 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,0), (2,1)]
theorem poly_32_iso_7_loser : defeated_by poly_32_iso_7 PavingH = true := by {
  decide
}

def poly_33_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (3,0)]
theorem poly_33_iso_0_loser : defeated_by poly_33_iso_0 PavingBrick = true := by {
  decide
}

def poly_33_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (1,3)]
theorem poly_33_iso_1_loser : defeated_by poly_33_iso_1 PavingBrick = true := by {
  decide
}

def poly_33_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (3,1)]
theorem poly_33_iso_2_loser : defeated_by poly_33_iso_2 PavingBrick = true := by {
  decide
}

def poly_33_iso_3 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (1,2)]
theorem poly_33_iso_3_loser : defeated_by poly_33_iso_3 PavingBrick = true := by {
  decide
}

def poly_34_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_34_iso_0_loser : defeated_by poly_34_iso_0 PavingH = true := by {
  decide
}

def poly_34_iso_1 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_34_iso_1_loser : defeated_by poly_34_iso_1 PavingH = true := by {
  decide
}

def poly_34_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,1), (3,1)]
theorem poly_34_iso_2_loser : defeated_by poly_34_iso_2 PavingH = true := by {
  decide
}

def poly_34_iso_3 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (3,1)]
theorem poly_34_iso_3_loser : defeated_by poly_34_iso_3 PavingH = true := by {
  decide
}

def poly_35_iso_0 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1)]
theorem poly_35_iso_0_loser : defeated_by poly_35_iso_0 PavingBrick = true := by {
  decide
}

def poly_35_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]
theorem poly_35_iso_1_loser : defeated_by poly_35_iso_1 PavingBrick = true := by {
  decide
}

def poly_36_iso_0 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (2,1)]
theorem poly_36_iso_0_loser : defeated_by poly_36_iso_0 PavingH = true := by {
  decide
}

def poly_36_iso_1 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (3,1)]
theorem poly_36_iso_1_loser : defeated_by poly_36_iso_1 PavingH = true := by {
  decide
}

def poly_36_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (2,2)]
theorem poly_36_iso_2_loser : defeated_by poly_36_iso_2 PavingH = true := by {
  decide
}

def poly_36_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (3,0)]
theorem poly_36_iso_3_loser : defeated_by poly_36_iso_3 PavingH = true := by {
  decide
}

def poly_36_iso_4 : Polyomino := [(0,2), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_36_iso_4_loser : defeated_by poly_36_iso_4 PavingH = true := by {
  decide
}

def poly_36_iso_5 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (2,3)]
theorem poly_36_iso_5_loser : defeated_by poly_36_iso_5 PavingH = true := by {
  decide
}

def poly_36_iso_6 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (3,1)]
theorem poly_36_iso_6_loser : defeated_by poly_36_iso_6 PavingH = true := by {
  decide
}

def poly_36_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,2), (3,2)]
theorem poly_36_iso_7_loser : defeated_by poly_36_iso_7 PavingH = true := by {
  decide
}

def poly_37_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,0)]
theorem poly_37_iso_0_loser : defeated_by poly_37_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_37_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_37_iso_1_loser : defeated_by poly_37_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_37_iso_2 : Polyomino := [(0,4), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_37_iso_2_loser : defeated_by poly_37_iso_2 PavingCheckerboard = true := by {
  decide
}

def poly_37_iso_3 : Polyomino := [(0,1), (1,1), (2,1), (3,1), (4,0), (4,1)]
theorem poly_37_iso_3_loser : defeated_by poly_37_iso_3 PavingCheckerboard = true := by {
  decide
}

def poly_37_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,4)]
theorem poly_37_iso_4_loser : defeated_by poly_37_iso_4 PavingCheckerboard = true := by {
  decide
}

def poly_37_iso_5 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,1), (4,1)]
theorem poly_37_iso_5_loser : defeated_by poly_37_iso_5 PavingCheckerboard = true := by {
  decide
}

def poly_37_iso_6 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (3,0), (4,0)]
theorem poly_37_iso_6_loser : defeated_by poly_37_iso_6 PavingCheckerboard = true := by {
  decide
}

def poly_37_iso_7 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (4,0), (4,1)]
theorem poly_37_iso_7_loser : defeated_by poly_37_iso_7 PavingCheckerboard = true := by {
  decide
}

def poly_38_iso_0 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_38_iso_0_loser : defeated_by poly_38_iso_0 PavingH = true := by {
  decide
}

def poly_38_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_38_iso_1_loser : defeated_by poly_38_iso_1 PavingH = true := by {
  decide
}

def poly_38_iso_2 : Polyomino := [(0,1), (0,2), (1,1), (2,1), (3,0), (3,1)]
theorem poly_38_iso_2_loser : defeated_by poly_38_iso_2 PavingH = true := by {
  decide
}

def poly_38_iso_3 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,1), (3,2)]
theorem poly_38_iso_3_loser : defeated_by poly_38_iso_3 PavingH = true := by {
  decide
}

def poly_39_iso_0 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (2,2)]
theorem poly_39_iso_0_loser : defeated_by poly_39_iso_0 PavingH = true := by {
  decide
}

def poly_39_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (2,1)]
theorem poly_39_iso_1_loser : defeated_by poly_39_iso_1 PavingH = true := by {
  decide
}

def poly_39_iso_2 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (2,2)]
theorem poly_39_iso_2_loser : defeated_by poly_39_iso_2 PavingH = true := by {
  decide
}

def poly_39_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (2,1)]
theorem poly_39_iso_3_loser : defeated_by poly_39_iso_3 PavingH = true := by {
  decide
}

def poly_39_iso_4 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,1), (2,2)]
theorem poly_39_iso_4_loser : defeated_by poly_39_iso_4 PavingH = true := by {
  decide
}

def poly_39_iso_5 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (2,2)]
theorem poly_39_iso_5_loser : defeated_by poly_39_iso_5 PavingH = true := by {
  decide
}

def poly_39_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (2,1)]
theorem poly_39_iso_6_loser : defeated_by poly_39_iso_6 PavingH = true := by {
  decide
}

def poly_39_iso_7 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (2,0)]
theorem poly_39_iso_7_loser : defeated_by poly_39_iso_7 PavingH = true := by {
  decide
}

def poly_40_iso_0 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,1), (4,1)]
theorem poly_40_iso_0_loser : defeated_by poly_40_iso_0 PavingStripesH = true := by {
  decide
}

def poly_40_iso_1 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,0), (4,0)]
theorem poly_40_iso_1_loser : defeated_by poly_40_iso_1 PavingStripesH = true := by {
  decide
}

def poly_40_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (1,4)]
theorem poly_40_iso_2_loser : defeated_by poly_40_iso_2 PavingStripesH = true := by {
  decide
}

def poly_40_iso_3 : Polyomino := [(0,2), (0,3), (0,4), (1,0), (1,1), (1,2)]
theorem poly_40_iso_3_loser : defeated_by poly_40_iso_3 PavingStripesH = true := by {
  decide
}

def poly_41_iso_0 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_41_iso_0_loser : defeated_by poly_41_iso_0 PavingH = true := by {
  decide
}

def poly_41_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (3,1)]
theorem poly_41_iso_1_loser : defeated_by poly_41_iso_1 PavingH = true := by {
  decide
}

def poly_41_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (3,1), (3,2)]
theorem poly_41_iso_2_loser : defeated_by poly_41_iso_2 PavingH = true := by {
  decide
}

def poly_41_iso_3 : Polyomino := [(0,1), (1,1), (1,2), (2,1), (3,0), (3,1)]
theorem poly_41_iso_3_loser : defeated_by poly_41_iso_3 PavingH = true := by {
  decide
}

def poly_41_iso_4 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (3,1)]
theorem poly_41_iso_4_loser : defeated_by poly_41_iso_4 PavingH = true := by {
  decide
}

def poly_41_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_41_iso_5_loser : defeated_by poly_41_iso_5 PavingH = true := by {
  decide
}

def poly_41_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_41_iso_6_loser : defeated_by poly_41_iso_6 PavingH = true := by {
  decide
}

def poly_41_iso_7 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_41_iso_7_loser : defeated_by poly_41_iso_7 PavingH = true := by {
  decide
}

def poly_42_iso_0 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (3,1), (4,0), (4,1)]
theorem poly_42_iso_0_loser : defeated_by poly_42_iso_0 PavingBrick = true := by {
  decide
}

def poly_42_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_42_iso_1_loser : defeated_by poly_42_iso_1 PavingBrick = true := by {
  decide
}

def poly_42_iso_2 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,1), (3,1), (4,1)]
theorem poly_42_iso_2_loser : defeated_by poly_42_iso_2 PavingBrick = true := by {
  decide
}

def poly_42_iso_3 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,0), (3,0), (4,0)]
theorem poly_42_iso_3_loser : defeated_by poly_42_iso_3 PavingBrick = true := by {
  decide
}

def poly_42_iso_4 : Polyomino := [(0,3), (0,4), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_42_iso_4_loser : defeated_by poly_42_iso_4 PavingBrick = true := by {
  decide
}

def poly_42_iso_5 : Polyomino := [(0,1), (1,1), (2,1), (3,0), (3,1), (4,0), (4,1)]
theorem poly_42_iso_5_loser : defeated_by poly_42_iso_5 PavingBrick = true := by {
  decide
}

def poly_42_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,3), (1,4)]
theorem poly_42_iso_6_loser : defeated_by poly_42_iso_6 PavingBrick = true := by {
  decide
}

def poly_42_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (1,1)]
theorem poly_42_iso_7_loser : defeated_by poly_42_iso_7 PavingBrick = true := by {
  decide
}

def poly_43_iso_0 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (2,2), (2,3)]
theorem poly_43_iso_0_loser : defeated_by poly_43_iso_0 PavingH = true := by {
  decide
}

def poly_43_iso_1 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (2,2), (2,3)]
theorem poly_43_iso_1_loser : defeated_by poly_43_iso_1 PavingH = true := by {
  decide
}

def poly_43_iso_2 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (2,2), (3,2)]
theorem poly_43_iso_2_loser : defeated_by poly_43_iso_2 PavingH = true := by {
  decide
}

def poly_43_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (2,2), (3,0)]
theorem poly_43_iso_3_loser : defeated_by poly_43_iso_3 PavingH = true := by {
  decide
}

def poly_43_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,1), (1,2), (2,2)]
theorem poly_43_iso_4_loser : defeated_by poly_43_iso_4 PavingH = true := by {
  decide
}

def poly_43_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (2,1), (3,0)]
theorem poly_43_iso_5_loser : defeated_by poly_43_iso_5 PavingH = true := by {
  decide
}

def poly_43_iso_6 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,1), (2,2), (3,2)]
theorem poly_43_iso_6_loser : defeated_by poly_43_iso_6 PavingH = true := by {
  decide
}

def poly_43_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,1), (1,2), (2,1)]
theorem poly_43_iso_7_loser : defeated_by poly_43_iso_7 PavingH = true := by {
  decide
}

def poly_44_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (2,2)]
theorem poly_44_iso_0_loser : defeated_by poly_44_iso_0 PavingH = true := by {
  decide
}

def poly_44_iso_1 : Polyomino := [(0,1), (1,1), (2,1), (2,2), (3,1), (4,0), (4,1)]
theorem poly_44_iso_1_loser : defeated_by poly_44_iso_1 PavingH = true := by {
  decide
}

def poly_44_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (3,1), (4,1)]
theorem poly_44_iso_2_loser : defeated_by poly_44_iso_2 PavingH = true := by {
  decide
}

def poly_44_iso_3 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (3,1), (4,1)]
theorem poly_44_iso_3_loser : defeated_by poly_44_iso_3 PavingH = true := by {
  decide
}

def poly_44_iso_4 : Polyomino := [(0,4), (1,0), (1,1), (1,2), (1,3), (1,4), (2,2)]
theorem poly_44_iso_4_loser : defeated_by poly_44_iso_4 PavingH = true := by {
  decide
}

def poly_44_iso_5 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,1), (4,1), (4,2)]
theorem poly_44_iso_5_loser : defeated_by poly_44_iso_5 PavingH = true := by {
  decide
}

def poly_44_iso_6 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (1,4), (2,0)]
theorem poly_44_iso_6_loser : defeated_by poly_44_iso_6 PavingH = true := by {
  decide
}

def poly_44_iso_7 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (1,4), (2,4)]
theorem poly_44_iso_7_loser : defeated_by poly_44_iso_7 PavingH = true := by {
  decide
}

def poly_45_iso_0 : Polyomino := [(0,2), (0,4), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_45_iso_0_loser : defeated_by poly_45_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_45_iso_1 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,1), (4,0), (4,1)]
theorem poly_45_iso_1_loser : defeated_by poly_45_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_45_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (1,2)]
theorem poly_45_iso_2_loser : defeated_by poly_45_iso_2 PavingCheckerboard = true := by {
  decide
}

def poly_45_iso_3 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (2,1), (3,0), (4,0)]
theorem poly_45_iso_3_loser : defeated_by poly_45_iso_3 PavingCheckerboard = true := by {
  decide
}

def poly_45_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,2), (1,4)]
theorem poly_45_iso_4_loser : defeated_by poly_45_iso_4 PavingCheckerboard = true := by {
  decide
}

def poly_45_iso_5 : Polyomino := [(0,0), (0,1), (1,1), (2,0), (2,1), (3,1), (4,1)]
theorem poly_45_iso_5_loser : defeated_by poly_45_iso_5 PavingCheckerboard = true := by {
  decide
}

def poly_45_iso_6 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,0), (4,0), (4,1)]
theorem poly_45_iso_6_loser : defeated_by poly_45_iso_6 PavingCheckerboard = true := by {
  decide
}

def poly_45_iso_7 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_45_iso_7_loser : defeated_by poly_45_iso_7 PavingCheckerboard = true := by {
  decide
}

def poly_46_iso_0 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,1), (2,2), (2,3)]
theorem poly_46_iso_0_loser : defeated_by poly_46_iso_0 PavingH = true := by {
  decide
}

def poly_46_iso_1 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (2,1), (2,2)]
theorem poly_46_iso_1_loser : defeated_by poly_46_iso_1 PavingH = true := by {
  decide
}

def poly_46_iso_2 : Polyomino := [(0,2), (1,0), (1,2), (2,0), (2,1), (2,2), (3,1)]
theorem poly_46_iso_2_loser : defeated_by poly_46_iso_2 PavingH = true := by {
  decide
}

def poly_46_iso_3 : Polyomino := [(0,0), (1,0), (1,2), (2,0), (2,1), (2,2), (3,1)]
theorem poly_46_iso_3_loser : defeated_by poly_46_iso_3 PavingH = true := by {
  decide
}

def poly_46_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (2,1), (2,2)]
theorem poly_46_iso_4_loser : defeated_by poly_46_iso_4 PavingH = true := by {
  decide
}

def poly_46_iso_5 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (2,2), (3,2)]
theorem poly_46_iso_5_loser : defeated_by poly_46_iso_5 PavingH = true := by {
  decide
}

def poly_46_iso_6 : Polyomino := [(0,1), (0,2), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_46_iso_6_loser : defeated_by poly_46_iso_6 PavingH = true := by {
  decide
}

def poly_46_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (2,2), (3,0)]
theorem poly_46_iso_7_loser : defeated_by poly_46_iso_7 PavingH = true := by {
  decide
}

def poly_47_iso_0 : Polyomino := [(0,3), (1,1), (1,2), (1,3), (2,1), (3,0), (3,1)]
theorem poly_47_iso_0_loser : defeated_by poly_47_iso_0 PavingH = true := by {
  decide
}

def poly_47_iso_1 : Polyomino := [(0,2), (0,3), (1,2), (2,0), (2,1), (2,2), (3,0)]
theorem poly_47_iso_1_loser : defeated_by poly_47_iso_1 PavingH = true := by {
  decide
}

def poly_47_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (2,3), (3,3)]
theorem poly_47_iso_2_loser : defeated_by poly_47_iso_2 PavingH = true := by {
  decide
}

def poly_47_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,2), (3,2), (3,3)]
theorem poly_47_iso_3_loser : defeated_by poly_47_iso_3 PavingH = true := by {
  decide
}

def poly_48_iso_0 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)]
theorem poly_48_iso_0_loser : defeated_by poly_48_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_48_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6)]
theorem poly_48_iso_1_loser : defeated_by poly_48_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_49_iso_0 : Polyomino := [(0,1), (1,1), (1,2), (2,1), (3,0), (3,1), (3,2)]
theorem poly_49_iso_0_loser : defeated_by poly_49_iso_0 PavingH = true := by {
  decide
}

def poly_49_iso_1 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_49_iso_1_loser : defeated_by poly_49_iso_1 PavingH = true := by {
  decide
}

def poly_49_iso_2 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,1), (2,3)]
theorem poly_49_iso_2_loser : defeated_by poly_49_iso_2 PavingH = true := by {
  decide
}

def poly_49_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,1), (2,2), (3,1)]
theorem poly_49_iso_3_loser : defeated_by poly_49_iso_3 PavingH = true := by {
  decide
}

def poly_49_iso_4 : Polyomino := [(0,1), (0,3), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_49_iso_4_loser : defeated_by poly_49_iso_4 PavingH = true := by {
  decide
}

def poly_49_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,0), (2,2)]
theorem poly_49_iso_5_loser : defeated_by poly_49_iso_5 PavingH = true := by {
  decide
}

def poly_49_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (3,0), (3,1), (3,2)]
theorem poly_49_iso_6_loser : defeated_by poly_49_iso_6 PavingH = true := by {
  decide
}

def poly_49_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,0), (2,1), (3,1)]
theorem poly_49_iso_7_loser : defeated_by poly_49_iso_7 PavingH = true := by {
  decide
}

def poly_50_iso_0 : Polyomino := [(0,0), (1,0), (1,2), (2,0), (2,1), (2,2), (3,0)]
theorem poly_50_iso_0_loser : defeated_by poly_50_iso_0 PavingH = true := by {
  decide
}

def poly_50_iso_1 : Polyomino := [(0,1), (0,2), (1,2), (2,0), (2,1), (2,2), (2,3)]
theorem poly_50_iso_1_loser : defeated_by poly_50_iso_1 PavingH = true := by {
  decide
}

def poly_50_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (2,2), (3,2)]
theorem poly_50_iso_2_loser : defeated_by poly_50_iso_2 PavingH = true := by {
  decide
}

def poly_50_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (2,2), (3,0)]
theorem poly_50_iso_3_loser : defeated_by poly_50_iso_3 PavingH = true := by {
  decide
}

def poly_50_iso_4 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (2,2), (2,3)]
theorem poly_50_iso_4_loser : defeated_by poly_50_iso_4 PavingH = true := by {
  decide
}

def poly_50_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,2), (2,1), (2,2)]
theorem poly_50_iso_5_loser : defeated_by poly_50_iso_5 PavingH = true := by {
  decide
}

def poly_50_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,1), (2,1), (2,2)]
theorem poly_50_iso_6_loser : defeated_by poly_50_iso_6 PavingH = true := by {
  decide
}

def poly_50_iso_7 : Polyomino := [(0,2), (1,0), (1,2), (2,0), (2,1), (2,2), (3,2)]
theorem poly_50_iso_7_loser : defeated_by poly_50_iso_7 PavingH = true := by {
  decide
}

def poly_51_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,1), (2,2), (3,2)]
theorem poly_51_iso_0_loser : defeated_by poly_51_iso_0 PavingH = true := by {
  decide
}

def poly_51_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,1), (2,2), (2,3)]
theorem poly_51_iso_1_loser : defeated_by poly_51_iso_1 PavingH = true := by {
  decide
}

def poly_51_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (1,3), (2,3)]
theorem poly_51_iso_2_loser : defeated_by poly_51_iso_2 PavingH = true := by {
  decide
}

def poly_51_iso_3 : Polyomino := [(0,2), (1,1), (1,2), (2,1), (2,2), (3,0), (3,1)]
theorem poly_51_iso_3_loser : defeated_by poly_51_iso_3 PavingH = true := by {
  decide
}

def poly_51_iso_4 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,0), (2,1), (3,0)]
theorem poly_51_iso_4_loser : defeated_by poly_51_iso_4 PavingH = true := by {
  decide
}

def poly_51_iso_5 : Polyomino := [(0,3), (1,1), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_51_iso_5_loser : defeated_by poly_51_iso_5 PavingH = true := by {
  decide
}

def poly_51_iso_6 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (2,0)]
theorem poly_51_iso_6_loser : defeated_by poly_51_iso_6 PavingH = true := by {
  decide
}

def poly_51_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (3,1), (3,2)]
theorem poly_51_iso_7_loser : defeated_by poly_51_iso_7 PavingH = true := by {
  decide
}

def poly_52_iso_0 : Polyomino := [(0,4), (1,0), (1,1), (1,2), (1,3), (1,4), (2,3)]
theorem poly_52_iso_0_loser : defeated_by poly_52_iso_0 PavingH = true := by {
  decide
}

def poly_52_iso_1 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,1), (3,1), (4,1)]
theorem poly_52_iso_1_loser : defeated_by poly_52_iso_1 PavingH = true := by {
  decide
}

def poly_52_iso_2 : Polyomino := [(0,1), (1,1), (2,1), (3,1), (3,2), (4,0), (4,1)]
theorem poly_52_iso_2_loser : defeated_by poly_52_iso_2 PavingH = true := by {
  decide
}

def poly_52_iso_3 : Polyomino := [(0,1), (1,1), (2,1), (3,0), (3,1), (4,1), (4,2)]
theorem poly_52_iso_3_loser : defeated_by poly_52_iso_3 PavingH = true := by {
  decide
}

def poly_52_iso_4 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (1,4), (2,4)]
theorem poly_52_iso_4_loser : defeated_by poly_52_iso_4 PavingH = true := by {
  decide
}

def poly_52_iso_5 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,1), (3,1), (4,1)]
theorem poly_52_iso_5_loser : defeated_by poly_52_iso_5 PavingH = true := by {
  decide
}

def poly_52_iso_6 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (2,1)]
theorem poly_52_iso_6_loser : defeated_by poly_52_iso_6 PavingH = true := by {
  decide
}

def poly_52_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (1,4), (2,0)]
theorem poly_52_iso_7_loser : defeated_by poly_52_iso_7 PavingH = true := by {
  decide
}

def poly_53_iso_0 : Polyomino := [(0,1), (0,2), (1,1), (1,2), (2,0), (2,1), (2,2)]
theorem poly_53_iso_0_loser : defeated_by poly_53_iso_0 PavingH = true := by {
  decide
}

def poly_53_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1), (2,2)]
theorem poly_53_iso_1_loser : defeated_by poly_53_iso_1 PavingH = true := by {
  decide
}

def poly_53_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (2,0), (2,1)]
theorem poly_53_iso_2_loser : defeated_by poly_53_iso_2 PavingH = true := by {
  decide
}

def poly_53_iso_3 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
theorem poly_53_iso_3_loser : defeated_by poly_53_iso_3 PavingH = true := by {
  decide
}

def poly_53_iso_4 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
theorem poly_53_iso_4_loser : defeated_by poly_53_iso_4 PavingH = true := by {
  decide
}

def poly_53_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0)]
theorem poly_53_iso_5_loser : defeated_by poly_53_iso_5 PavingH = true := by {
  decide
}

def poly_53_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,2)]
theorem poly_53_iso_6_loser : defeated_by poly_53_iso_6 PavingH = true := by {
  decide
}

def poly_53_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (2,1), (2,2)]
theorem poly_53_iso_7_loser : defeated_by poly_53_iso_7 PavingH = true := by {
  decide
}

def poly_54_iso_0 : Polyomino := [(0,2), (1,2), (2,2), (3,0), (3,1), (3,2), (4,0)]
theorem poly_54_iso_0_loser : defeated_by poly_54_iso_0 PavingH = true := by {
  decide
}

def poly_54_iso_1 : Polyomino := [(0,1), (0,2), (0,3), (0,4), (1,1), (2,0), (2,1)]
theorem poly_54_iso_1_loser : defeated_by poly_54_iso_1 PavingH = true := by {
  decide
}

def poly_54_iso_2 : Polyomino := [(0,3), (0,4), (1,3), (2,0), (2,1), (2,2), (2,3)]
theorem poly_54_iso_2_loser : defeated_by poly_54_iso_2 PavingH = true := by {
  decide
}

def poly_54_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (2,4)]
theorem poly_54_iso_3_loser : defeated_by poly_54_iso_3 PavingH = true := by {
  decide
}

def poly_54_iso_4 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,2), (3,2), (4,2)]
theorem poly_54_iso_4_loser : defeated_by poly_54_iso_4 PavingH = true := by {
  decide
}

def poly_54_iso_5 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (3,1), (3,2), (4,2)]
theorem poly_54_iso_5_loser : defeated_by poly_54_iso_5 PavingH = true := by {
  decide
}

def poly_54_iso_6 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (3,0), (4,0)]
theorem poly_54_iso_6_loser : defeated_by poly_54_iso_6 PavingH = true := by {
  decide
}

def poly_54_iso_7 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (2,3), (2,4)]
theorem poly_54_iso_7_loser : defeated_by poly_54_iso_7 PavingH = true := by {
  decide
}

def poly_55_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1)]
theorem poly_55_iso_0_loser : defeated_by poly_55_iso_0 PavingH = true := by {
  decide
}

def poly_55_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (2,1), (2,2)]
theorem poly_55_iso_1_loser : defeated_by poly_55_iso_1 PavingH = true := by {
  decide
}

def poly_55_iso_2 : Polyomino := [(0,0), (0,1), (1,0), (1,2), (2,0), (2,1), (2,2)]
theorem poly_55_iso_2_loser : defeated_by poly_55_iso_2 PavingH = true := by {
  decide
}

def poly_55_iso_3 : Polyomino := [(0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]
theorem poly_55_iso_3_loser : defeated_by poly_55_iso_3 PavingH = true := by {
  decide
}

def poly_56_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (3,1), (3,2)]
theorem poly_56_iso_0_loser : defeated_by poly_56_iso_0 PavingH = true := by {
  decide
}

def poly_56_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_56_iso_1_loser : defeated_by poly_56_iso_1 PavingH = true := by {
  decide
}

def poly_56_iso_2 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,1), (3,1), (3,2)]
theorem poly_56_iso_2_loser : defeated_by poly_56_iso_2 PavingH = true := by {
  decide
}

def poly_56_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,2), (2,3)]
theorem poly_56_iso_3_loser : defeated_by poly_56_iso_3 PavingH = true := by {
  decide
}

def poly_56_iso_4 : Polyomino := [(0,1), (0,2), (1,1), (1,2), (2,1), (3,0), (3,1)]
theorem poly_56_iso_4_loser : defeated_by poly_56_iso_4 PavingH = true := by {
  decide
}

def poly_56_iso_5 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (3,0), (3,1)]
theorem poly_56_iso_5_loser : defeated_by poly_56_iso_5 PavingH = true := by {
  decide
}

def poly_56_iso_6 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_56_iso_6_loser : defeated_by poly_56_iso_6 PavingH = true := by {
  decide
}

def poly_56_iso_7 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_56_iso_7_loser : defeated_by poly_56_iso_7 PavingH = true := by {
  decide
}

def poly_57_iso_0 : Polyomino := [(0,0), (0,4), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_57_iso_0_loser : defeated_by poly_57_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_57_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (1,4)]
theorem poly_57_iso_1_loser : defeated_by poly_57_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_57_iso_2 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (3,0), (4,0), (4,1)]
theorem poly_57_iso_2_loser : defeated_by poly_57_iso_2 PavingCheckerboard = true := by {
  decide
}

def poly_57_iso_3 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,1), (4,0), (4,1)]
theorem poly_57_iso_3_loser : defeated_by poly_57_iso_3 PavingCheckerboard = true := by {
  decide
}

def poly_58_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (3,0), (3,1), (4,1)]
theorem poly_58_iso_0_loser : defeated_by poly_58_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_58_iso_1 : Polyomino := [(0,1), (0,3), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_58_iso_1_loser : defeated_by poly_58_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_58_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (3,0), (3,1), (4,0)]
theorem poly_58_iso_2_loser : defeated_by poly_58_iso_2 PavingCheckerboard = true := by {
  decide
}

def poly_58_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,1), (1,3)]
theorem poly_58_iso_3_loser : defeated_by poly_58_iso_3 PavingCheckerboard = true := by {
  decide
}

def poly_59_iso_0 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,0), (4,0), (5,0)]
theorem poly_59_iso_0_loser : defeated_by poly_59_iso_0 PavingStripesH = true := by {
  decide
}

def poly_59_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,3), (1,4), (1,5)]
theorem poly_59_iso_1_loser : defeated_by poly_59_iso_1 PavingStripesH = true := by {
  decide
}

def poly_59_iso_2 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,1), (4,1), (5,1)]
theorem poly_59_iso_2_loser : defeated_by poly_59_iso_2 PavingStripesH = true := by {
  decide
}

def poly_59_iso_3 : Polyomino := [(0,1), (1,1), (2,1), (3,0), (3,1), (4,0), (5,0)]
theorem poly_59_iso_3_loser : defeated_by poly_59_iso_3 PavingStripesH = true := by {
  decide
}

def poly_59_iso_4 : Polyomino := [(0,2), (0,3), (0,4), (0,5), (1,0), (1,1), (1,2)]
theorem poly_59_iso_4_loser : defeated_by poly_59_iso_4 PavingStripesH = true := by {
  decide
}

def poly_59_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (1,4), (1,5)]
theorem poly_59_iso_5_loser : defeated_by poly_59_iso_5 PavingStripesH = true := by {
  decide
}

def poly_59_iso_6 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (3,1), (4,1), (5,1)]
theorem poly_59_iso_6_loser : defeated_by poly_59_iso_6 PavingStripesH = true := by {
  decide
}

def poly_59_iso_7 : Polyomino := [(0,3), (0,4), (0,5), (1,0), (1,1), (1,2), (1,3)]
theorem poly_59_iso_7_loser : defeated_by poly_59_iso_7 PavingStripesH = true := by {
  decide
}

def poly_60_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (3,0), (3,1)]
theorem poly_60_iso_0_loser : defeated_by poly_60_iso_0 PavingH = true := by {
  decide
}

def poly_60_iso_1 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,1), (2,2), (3,2)]
theorem poly_60_iso_1_loser : defeated_by poly_60_iso_1 PavingH = true := by {
  decide
}

def poly_60_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,0), (2,1), (3,0)]
theorem poly_60_iso_2_loser : defeated_by poly_60_iso_2 PavingH = true := by {
  decide
}

def poly_60_iso_3 : Polyomino := [(0,0), (0,1), (0,3), (1,1), (1,2), (1,3), (2,2)]
theorem poly_60_iso_3_loser : defeated_by poly_60_iso_3 PavingH = true := by {
  decide
}

def poly_60_iso_4 : Polyomino := [(0,2), (1,1), (1,2), (1,3), (2,0), (2,1), (2,3)]
theorem poly_60_iso_4_loser : defeated_by poly_60_iso_4 PavingH = true := by {
  decide
}

def poly_60_iso_5 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (3,1), (3,2)]
theorem poly_60_iso_5_loser : defeated_by poly_60_iso_5 PavingH = true := by {
  decide
}

def poly_60_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (2,2), (2,3)]
theorem poly_60_iso_6_loser : defeated_by poly_60_iso_6 PavingH = true := by {
  decide
}

def poly_60_iso_7 : Polyomino := [(0,0), (0,2), (0,3), (1,0), (1,1), (1,2), (2,1)]
theorem poly_60_iso_7_loser : defeated_by poly_60_iso_7 PavingH = true := by {
  decide
}

def poly_61_iso_0 : Polyomino := [(0,1), (0,2), (1,2), (2,1), (2,2), (3,0), (3,1)]
theorem poly_61_iso_0_loser : defeated_by poly_61_iso_0 PavingH = true := by {
  decide
}

def poly_61_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (1,3), (2,3)]
theorem poly_61_iso_1_loser : defeated_by poly_61_iso_1 PavingH = true := by {
  decide
}

def poly_61_iso_2 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (2,1), (3,1), (3,2)]
theorem poly_61_iso_2_loser : defeated_by poly_61_iso_2 PavingH = true := by {
  decide
}

def poly_61_iso_3 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,0), (3,0), (3,1)]
theorem poly_61_iso_3_loser : defeated_by poly_61_iso_3 PavingH = true := by {
  decide
}

def poly_61_iso_4 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,2), (3,1), (3,2)]
theorem poly_61_iso_4_loser : defeated_by poly_61_iso_4 PavingH = true := by {
  decide
}

def poly_61_iso_5 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (1,3), (2,0)]
theorem poly_61_iso_5_loser : defeated_by poly_61_iso_5 PavingH = true := by {
  decide
}

def poly_61_iso_6 : Polyomino := [(0,0), (1,0), (1,1), (1,3), (2,1), (2,2), (2,3)]
theorem poly_61_iso_6_loser : defeated_by poly_61_iso_6 PavingH = true := by {
  decide
}

def poly_61_iso_7 : Polyomino := [(0,3), (1,0), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_61_iso_7_loser : defeated_by poly_61_iso_7 PavingH = true := by {
  decide
}

def poly_62_iso_0 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (3,0), (4,0)]
theorem poly_62_iso_0_loser : defeated_by poly_62_iso_0 PavingH = true := by {
  decide
}

def poly_62_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,2), (2,2)]
theorem poly_62_iso_1_loser : defeated_by poly_62_iso_1 PavingH = true := by {
  decide
}

def poly_62_iso_2 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (3,2), (4,2)]
theorem poly_62_iso_2_loser : defeated_by poly_62_iso_2 PavingH = true := by {
  decide
}

def poly_62_iso_3 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (2,3), (2,4)]
theorem poly_62_iso_3_loser : defeated_by poly_62_iso_3 PavingH = true := by {
  decide
}

def poly_63_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (2,2), (3,1)]
theorem poly_63_iso_0_loser : defeated_by poly_63_iso_0 PavingH = true := by {
  decide
}

def poly_63_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,1), (2,2), (3,2)]
theorem poly_63_iso_1_loser : defeated_by poly_63_iso_1 PavingH = true := by {
  decide
}

def poly_63_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,1), (2,2), (2,3)]
theorem poly_63_iso_2_loser : defeated_by poly_63_iso_2 PavingH = true := by {
  decide
}

def poly_63_iso_3 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (2,1)]
theorem poly_63_iso_3_loser : defeated_by poly_63_iso_3 PavingH = true := by {
  decide
}

def poly_63_iso_4 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (2,1), (3,0)]
theorem poly_63_iso_4_loser : defeated_by poly_63_iso_4 PavingH = true := by {
  decide
}

def poly_63_iso_5 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (2,2), (3,1)]
theorem poly_63_iso_5_loser : defeated_by poly_63_iso_5 PavingH = true := by {
  decide
}

def poly_63_iso_6 : Polyomino := [(0,2), (1,1), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_63_iso_6_loser : defeated_by poly_63_iso_6 PavingH = true := by {
  decide
}

def poly_63_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (1,3), (2,2)]
theorem poly_63_iso_7_loser : defeated_by poly_63_iso_7 PavingH = true := by {
  decide
}

def poly_64_iso_0 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1)]
theorem poly_64_iso_0_loser : defeated_by poly_64_iso_0 PavingH = true := by {
  decide
}

def poly_64_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (2,1), (2,2)]
theorem poly_64_iso_1_loser : defeated_by poly_64_iso_1 PavingH = true := by {
  decide
}

def poly_65_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,3)]
theorem poly_65_iso_0_loser : defeated_by poly_65_iso_0 PavingH = true := by {
  decide
}

def poly_65_iso_1 : Polyomino := [(0,2), (0,3), (1,1), (1,2), (2,0), (2,1), (3,0)]
theorem poly_65_iso_1_loser : defeated_by poly_65_iso_1 PavingH = true := by {
  decide
}

def poly_65_iso_2 : Polyomino := [(0,3), (1,2), (1,3), (2,1), (2,2), (3,0), (3,1)]
theorem poly_65_iso_2_loser : defeated_by poly_65_iso_2 PavingH = true := by {
  decide
}

def poly_65_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (3,2), (3,3)]
theorem poly_65_iso_3_loser : defeated_by poly_65_iso_3 PavingH = true := by {
  decide
}

def poly_66_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (3,0), (3,1), (3,2)]
theorem poly_66_iso_0_loser : defeated_by poly_66_iso_0 PavingH = true := by {
  decide
}

def poly_66_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (3,0)]
theorem poly_66_iso_1_loser : defeated_by poly_66_iso_1 PavingH = true := by {
  decide
}

def poly_66_iso_2 : Polyomino := [(0,2), (1,1), (1,2), (2,2), (3,0), (3,1), (3,2)]
theorem poly_66_iso_2_loser : defeated_by poly_66_iso_2 PavingH = true := by {
  decide
}

def poly_66_iso_3 : Polyomino := [(0,3), (1,1), (1,3), (2,0), (2,1), (2,2), (2,3)]
theorem poly_66_iso_3_loser : defeated_by poly_66_iso_3 PavingH = true := by {
  decide
}

def poly_66_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,2), (2,0)]
theorem poly_66_iso_4_loser : defeated_by poly_66_iso_4 PavingH = true := by {
  decide
}

def poly_66_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,1), (2,2), (3,2)]
theorem poly_66_iso_5_loser : defeated_by poly_66_iso_5 PavingH = true := by {
  decide
}

def poly_66_iso_6 : Polyomino := [(0,0), (1,0), (1,2), (2,0), (2,1), (2,2), (2,3)]
theorem poly_66_iso_6_loser : defeated_by poly_66_iso_6 PavingH = true := by {
  decide
}

def poly_66_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,1), (1,3), (2,3)]
theorem poly_66_iso_7_loser : defeated_by poly_66_iso_7 PavingH = true := by {
  decide
}

def poly_67_iso_0 : Polyomino := [(0,1), (0,3), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_67_iso_0_loser : defeated_by poly_67_iso_0 PavingH = true := by {
  decide
}

def poly_67_iso_1 : Polyomino := [(0,1), (0,2), (1,1), (2,1), (2,2), (3,0), (3,1)]
theorem poly_67_iso_1_loser : defeated_by poly_67_iso_1 PavingH = true := by {
  decide
}

def poly_67_iso_2 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,1), (3,0), (3,1)]
theorem poly_67_iso_2_loser : defeated_by poly_67_iso_2 PavingH = true := by {
  decide
}

def poly_67_iso_3 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,0), (2,2)]
theorem poly_67_iso_3_loser : defeated_by poly_67_iso_3 PavingH = true := by {
  decide
}

def poly_67_iso_4 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,1), (3,1), (3,2)]
theorem poly_67_iso_4_loser : defeated_by poly_67_iso_4 PavingH = true := by {
  decide
}

def poly_67_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,1), (2,3)]
theorem poly_67_iso_5_loser : defeated_by poly_67_iso_5 PavingH = true := by {
  decide
}

def poly_67_iso_6 : Polyomino := [(0,0), (0,1), (1,1), (2,0), (2,1), (3,1), (3,2)]
theorem poly_67_iso_6_loser : defeated_by poly_67_iso_6 PavingH = true := by {
  decide
}

def poly_67_iso_7 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_67_iso_7_loser : defeated_by poly_67_iso_7 PavingH = true := by {
  decide
}

def poly_68_iso_0 : Polyomino := [(0,2), (1,2), (2,1), (2,2), (2,3), (3,0), (3,1)]
theorem poly_68_iso_0_loser : defeated_by poly_68_iso_0 PavingH = true := by {
  decide
}

def poly_68_iso_1 : Polyomino := [(0,1), (1,1), (1,2), (1,3), (2,0), (2,1), (3,0)]
theorem poly_68_iso_1_loser : defeated_by poly_68_iso_1 PavingH = true := by {
  decide
}

def poly_68_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (2,3), (3,1)]
theorem poly_68_iso_2_loser : defeated_by poly_68_iso_2 PavingH = true := by {
  decide
}

def poly_68_iso_3 : Polyomino := [(0,3), (1,2), (1,3), (2,0), (2,1), (2,2), (3,2)]
theorem poly_68_iso_3_loser : defeated_by poly_68_iso_3 PavingH = true := by {
  decide
}

def poly_68_iso_4 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,2), (3,2)]
theorem poly_68_iso_4_loser : defeated_by poly_68_iso_4 PavingH = true := by {
  decide
}

def poly_68_iso_5 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (2,1), (3,1)]
theorem poly_68_iso_5_loser : defeated_by poly_68_iso_5 PavingH = true := by {
  decide
}

def poly_68_iso_6 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (3,2), (3,3)]
theorem poly_68_iso_6_loser : defeated_by poly_68_iso_6 PavingH = true := by {
  decide
}

def poly_68_iso_7 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,2), (2,3), (3,3)]
theorem poly_68_iso_7_loser : defeated_by poly_68_iso_7 PavingH = true := by {
  decide
}

def poly_69_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5)]
theorem poly_69_iso_0_loser : defeated_by poly_69_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_69_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (3,0), (4,0), (5,0)]
theorem poly_69_iso_1_loser : defeated_by poly_69_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_69_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,1), (4,1), (5,1)]
theorem poly_69_iso_2_loser : defeated_by poly_69_iso_2 PavingCheckerboard = true := by {
  decide
}

def poly_69_iso_3 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (5,1)]
theorem poly_69_iso_3_loser : defeated_by poly_69_iso_3 PavingCheckerboard = true := by {
  decide
}

def poly_69_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,5)]
theorem poly_69_iso_4_loser : defeated_by poly_69_iso_4 PavingCheckerboard = true := by {
  decide
}

def poly_69_iso_5 : Polyomino := [(0,1), (1,1), (2,1), (3,1), (4,1), (5,0), (5,1)]
theorem poly_69_iso_5_loser : defeated_by poly_69_iso_5 PavingCheckerboard = true := by {
  decide
}

def poly_69_iso_6 : Polyomino := [(0,5), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5)]
theorem poly_69_iso_6_loser : defeated_by poly_69_iso_6 PavingCheckerboard = true := by {
  decide
}

def poly_69_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,0)]
theorem poly_69_iso_7_loser : defeated_by poly_69_iso_7 PavingCheckerboard = true := by {
  decide
}

def poly_70_iso_0 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (2,3), (2,4)]
theorem poly_70_iso_0_loser : defeated_by poly_70_iso_0 PavingH = true := by {
  decide
}

def poly_70_iso_1 : Polyomino := [(0,3), (1,3), (2,0), (2,1), (2,2), (2,3), (2,4)]
theorem poly_70_iso_1_loser : defeated_by poly_70_iso_1 PavingH = true := by {
  decide
}

def poly_70_iso_2 : Polyomino := [(0,2), (1,2), (2,2), (3,0), (3,1), (3,2), (4,2)]
theorem poly_70_iso_2_loser : defeated_by poly_70_iso_2 PavingH = true := by {
  decide
}

def poly_70_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (3,0), (4,0)]
theorem poly_70_iso_3_loser : defeated_by poly_70_iso_3 PavingH = true := by {
  decide
}

def poly_70_iso_4 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,2), (3,2), (4,2)]
theorem poly_70_iso_4_loser : defeated_by poly_70_iso_4 PavingH = true := by {
  decide
}

def poly_70_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,1), (2,1)]
theorem poly_70_iso_5_loser : defeated_by poly_70_iso_5 PavingH = true := by {
  decide
}

def poly_70_iso_6 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (3,1), (3,2), (4,0)]
theorem poly_70_iso_6_loser : defeated_by poly_70_iso_6 PavingH = true := by {
  decide
}

def poly_70_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,3), (2,3)]
theorem poly_70_iso_7_loser : defeated_by poly_70_iso_7 PavingH = true := by {
  decide
}

def poly_71_iso_0 : Polyomino := [(0,2), (1,2), (1,3), (2,2), (3,0), (3,1), (3,2)]
theorem poly_71_iso_0_loser : defeated_by poly_71_iso_0 PavingH = true := by {
  decide
}

def poly_71_iso_1 : Polyomino := [(0,1), (0,2), (0,3), (1,1), (2,0), (2,1), (3,1)]
theorem poly_71_iso_1_loser : defeated_by poly_71_iso_1 PavingH = true := by {
  decide
}

def poly_71_iso_2 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (3,2)]
theorem poly_71_iso_2_loser : defeated_by poly_71_iso_2 PavingH = true := by {
  decide
}

def poly_71_iso_3 : Polyomino := [(0,3), (1,3), (2,0), (2,1), (2,2), (2,3), (3,1)]
theorem poly_71_iso_3_loser : defeated_by poly_71_iso_3 PavingH = true := by {
  decide
}

def poly_71_iso_4 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,3), (3,3)]
theorem poly_71_iso_4_loser : defeated_by poly_71_iso_4 PavingH = true := by {
  decide
}

def poly_71_iso_5 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,0), (3,0)]
theorem poly_71_iso_5_loser : defeated_by poly_71_iso_5 PavingH = true := by {
  decide
}

def poly_71_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (3,1), (3,2), (3,3)]
theorem poly_71_iso_6_loser : defeated_by poly_71_iso_6 PavingH = true := by {
  decide
}

def poly_71_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,2), (2,3), (3,2)]
theorem poly_71_iso_7_loser : defeated_by poly_71_iso_7 PavingH = true := by {
  decide
}

def poly_72_iso_0 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (2,1), (3,1)]
theorem poly_72_iso_0_loser : defeated_by poly_72_iso_0 PavingH = true := by {
  decide
}

def poly_72_iso_1 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_72_iso_1_loser : defeated_by poly_72_iso_1 PavingH = true := by {
  decide
}

def poly_72_iso_2 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (3,1), (3,2)]
theorem poly_72_iso_2_loser : defeated_by poly_72_iso_2 PavingH = true := by {
  decide
}

def poly_72_iso_3 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,2), (2,3)]
theorem poly_72_iso_3_loser : defeated_by poly_72_iso_3 PavingH = true := by {
  decide
}

def poly_72_iso_4 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_72_iso_4_loser : defeated_by poly_72_iso_4 PavingH = true := by {
  decide
}

def poly_72_iso_5 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (3,0), (3,1)]
theorem poly_72_iso_5_loser : defeated_by poly_72_iso_5 PavingH = true := by {
  decide
}

def poly_72_iso_6 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (2,1), (3,1)]
theorem poly_72_iso_6_loser : defeated_by poly_72_iso_6 PavingH = true := by {
  decide
}

def poly_72_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_72_iso_7_loser : defeated_by poly_72_iso_7 PavingH = true := by {
  decide
}

def poly_73_iso_0 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (3,0), (4,0)]
theorem poly_73_iso_0_loser : defeated_by poly_73_iso_0 PavingH = true := by {
  decide
}

def poly_73_iso_1 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (3,2), (4,2)]
theorem poly_73_iso_1_loser : defeated_by poly_73_iso_1 PavingH = true := by {
  decide
}

def poly_73_iso_2 : Polyomino := [(0,2), (0,3), (0,4), (1,2), (2,0), (2,1), (2,2)]
theorem poly_73_iso_2_loser : defeated_by poly_73_iso_2 PavingH = true := by {
  decide
}

def poly_73_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,2), (2,3), (2,4)]
theorem poly_73_iso_3_loser : defeated_by poly_73_iso_3 PavingH = true := by {
  decide
}

def poly_74_iso_0 : Polyomino := [(0,3), (1,0), (1,1), (1,3), (2,1), (2,2), (2,3)]
theorem poly_74_iso_0_loser : defeated_by poly_74_iso_0 PavingH = true := by {
  decide
}

def poly_74_iso_1 : Polyomino := [(0,0), (1,0), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_74_iso_1_loser : defeated_by poly_74_iso_1 PavingH = true := by {
  decide
}

def poly_74_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (3,0), (3,1), (3,2)]
theorem poly_74_iso_2_loser : defeated_by poly_74_iso_2 PavingH = true := by {
  decide
}

def poly_74_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,1), (2,2), (3,1)]
theorem poly_74_iso_3_loser : defeated_by poly_74_iso_3 PavingH = true := by {
  decide
}

def poly_74_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (1,3), (2,0)]
theorem poly_74_iso_4_loser : defeated_by poly_74_iso_4 PavingH = true := by {
  decide
}

def poly_74_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (3,1)]
theorem poly_74_iso_5_loser : defeated_by poly_74_iso_5 PavingH = true := by {
  decide
}

def poly_74_iso_6 : Polyomino := [(0,1), (1,1), (1,2), (2,2), (3,0), (3,1), (3,2)]
theorem poly_74_iso_6_loser : defeated_by poly_74_iso_6 PavingH = true := by {
  decide
}

def poly_74_iso_7 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (1,3), (2,3)]
theorem poly_74_iso_7_loser : defeated_by poly_74_iso_7 PavingH = true := by {
  decide
}

def poly_75_iso_0 : Polyomino := [(0,1), (0,2), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_75_iso_0_loser : defeated_by poly_75_iso_0 PavingH = true := by {
  decide
}

def poly_75_iso_1 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (2,1), (2,2)]
theorem poly_75_iso_1_loser : defeated_by poly_75_iso_1 PavingH = true := by {
  decide
}

def poly_75_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (2,2), (3,2)]
theorem poly_75_iso_2_loser : defeated_by poly_75_iso_2 PavingH = true := by {
  decide
}

def poly_75_iso_3 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (2,2), (3,0)]
theorem poly_75_iso_3_loser : defeated_by poly_75_iso_3 PavingH = true := by {
  decide
}

def poly_75_iso_4 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (2,2), (2,3)]
theorem poly_75_iso_4_loser : defeated_by poly_75_iso_4 PavingH = true := by {
  decide
}

def poly_75_iso_5 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,1), (2,2)]
theorem poly_75_iso_5_loser : defeated_by poly_75_iso_5 PavingH = true := by {
  decide
}

def poly_75_iso_6 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,1), (2,2), (3,1)]
theorem poly_75_iso_6_loser : defeated_by poly_75_iso_6 PavingH = true := by {
  decide
}

def poly_75_iso_7 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (3,1)]
theorem poly_75_iso_7_loser : defeated_by poly_75_iso_7 PavingH = true := by {
  decide
}

def poly_76_iso_0 : Polyomino := [(0,2), (0,3), (0,4), (1,0), (1,1), (1,2), (2,0)]
theorem poly_76_iso_0_loser : defeated_by poly_76_iso_0 PavingH = true := by {
  decide
}

def poly_76_iso_1 : Polyomino := [(0,2), (1,2), (2,1), (2,2), (3,1), (4,0), (4,1)]
theorem poly_76_iso_1_loser : defeated_by poly_76_iso_1 PavingH = true := by {
  decide
}

def poly_76_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (3,2), (4,2)]
theorem poly_76_iso_2_loser : defeated_by poly_76_iso_2 PavingH = true := by {
  decide
}

def poly_76_iso_3 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,1), (4,1), (4,2)]
theorem poly_76_iso_3_loser : defeated_by poly_76_iso_3 PavingH = true := by {
  decide
}

def poly_76_iso_4 : Polyomino := [(0,4), (1,2), (1,3), (1,4), (2,0), (2,1), (2,2)]
theorem poly_76_iso_4_loser : defeated_by poly_76_iso_4 PavingH = true := by {
  decide
}

def poly_76_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (1,4), (2,4)]
theorem poly_76_iso_5_loser : defeated_by poly_76_iso_5 PavingH = true := by {
  decide
}

def poly_76_iso_6 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (3,0), (4,0)]
theorem poly_76_iso_6_loser : defeated_by poly_76_iso_6 PavingH = true := by {
  decide
}

def poly_76_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,2), (2,3), (2,4)]
theorem poly_76_iso_7_loser : defeated_by poly_76_iso_7 PavingH = true := by {
  decide
}

def poly_77_iso_0 : Polyomino := [(0,1), (1,1), (1,2), (1,3), (1,4), (2,0), (2,1)]
theorem poly_77_iso_0_loser : defeated_by poly_77_iso_0 PavingH = true := by {
  decide
}

def poly_77_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (1,4), (2,1)]
theorem poly_77_iso_1_loser : defeated_by poly_77_iso_1 PavingH = true := by {
  decide
}

def poly_77_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,1), (3,1), (4,1)]
theorem poly_77_iso_2_loser : defeated_by poly_77_iso_2 PavingH = true := by {
  decide
}

def poly_77_iso_3 : Polyomino := [(0,3), (0,4), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_77_iso_3_loser : defeated_by poly_77_iso_3 PavingH = true := by {
  decide
}

def poly_77_iso_4 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,1), (3,1), (4,1)]
theorem poly_77_iso_4_loser : defeated_by poly_77_iso_4 PavingH = true := by {
  decide
}

def poly_77_iso_5 : Polyomino := [(0,1), (1,1), (2,1), (3,0), (3,1), (3,2), (4,0)]
theorem poly_77_iso_5_loser : defeated_by poly_77_iso_5 PavingH = true := by {
  decide
}

def poly_77_iso_6 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,3), (2,4)]
theorem poly_77_iso_6_loser : defeated_by poly_77_iso_6 PavingH = true := by {
  decide
}

def poly_77_iso_7 : Polyomino := [(0,1), (1,1), (2,1), (3,0), (3,1), (3,2), (4,2)]
theorem poly_77_iso_7_loser : defeated_by poly_77_iso_7 PavingH = true := by {
  decide
}

def poly_78_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (1,4), (2,1)]
theorem poly_78_iso_0_loser : defeated_by poly_78_iso_0 PavingH = true := by {
  decide
}

def poly_78_iso_1 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (1,4), (2,3)]
theorem poly_78_iso_1_loser : defeated_by poly_78_iso_1 PavingH = true := by {
  decide
}

def poly_78_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,1), (3,1), (4,1)]
theorem poly_78_iso_2_loser : defeated_by poly_78_iso_2 PavingH = true := by {
  decide
}

def poly_78_iso_3 : Polyomino := [(0,1), (1,1), (2,1), (3,0), (3,1), (3,2), (4,1)]
theorem poly_78_iso_3_loser : defeated_by poly_78_iso_3 PavingH = true := by {
  decide
}

def poly_79_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,2), (3,1), (3,2)]
theorem poly_79_iso_0_loser : defeated_by poly_79_iso_0 PavingH = true := by {
  decide
}

def poly_79_iso_1 : Polyomino := [(0,2), (1,0), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_79_iso_1_loser : defeated_by poly_79_iso_1 PavingH = true := by {
  decide
}

def poly_79_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (1,3), (2,1), (2,2), (2,3)]
theorem poly_79_iso_2_loser : defeated_by poly_79_iso_2 PavingH = true := by {
  decide
}

def poly_79_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (3,0), (3,1)]
theorem poly_79_iso_3_loser : defeated_by poly_79_iso_3 PavingH = true := by {
  decide
}

def poly_79_iso_4 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (2,1), (2,2), (3,1)]
theorem poly_79_iso_4_loser : defeated_by poly_79_iso_4 PavingH = true := by {
  decide
}

def poly_79_iso_5 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (1,3), (2,1)]
theorem poly_79_iso_5_loser : defeated_by poly_79_iso_5 PavingH = true := by {
  decide
}

def poly_79_iso_6 : Polyomino := [(0,1), (0,2), (1,2), (2,0), (2,1), (2,2), (3,1)]
theorem poly_79_iso_6_loser : defeated_by poly_79_iso_6 PavingH = true := by {
  decide
}

def poly_79_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (1,3), (2,2)]
theorem poly_79_iso_7_loser : defeated_by poly_79_iso_7 PavingH = true := by {
  decide
}

def poly_80_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,0), (3,1), (3,2)]
theorem poly_80_iso_0_loser : defeated_by poly_80_iso_0 PavingH = true := by {
  decide
}

def poly_80_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,0), (2,3)]
theorem poly_80_iso_1_loser : defeated_by poly_80_iso_1 PavingH = true := by {
  decide
}

def poly_80_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,1), (3,1), (3,2)]
theorem poly_80_iso_2_loser : defeated_by poly_80_iso_2 PavingH = true := by {
  decide
}

def poly_80_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,1), (3,0), (3,1)]
theorem poly_80_iso_3_loser : defeated_by poly_80_iso_3 PavingH = true := by {
  decide
}

def poly_80_iso_4 : Polyomino := [(0,0), (0,3), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_80_iso_4_loser : defeated_by poly_80_iso_4 PavingH = true := by {
  decide
}

def poly_80_iso_5 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,0), (2,3)]
theorem poly_80_iso_5_loser : defeated_by poly_80_iso_5 PavingH = true := by {
  decide
}

def poly_80_iso_6 : Polyomino := [(0,1), (0,2), (1,1), (2,1), (3,0), (3,1), (3,2)]
theorem poly_80_iso_6_loser : defeated_by poly_80_iso_6 PavingH = true := by {
  decide
}

def poly_80_iso_7 : Polyomino := [(0,0), (0,3), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_80_iso_7_loser : defeated_by poly_80_iso_7 PavingH = true := by {
  decide
}

def poly_81_iso_0 : Polyomino := [(0,1), (0,2), (0,3), (1,1), (2,1), (3,0), (3,1)]
theorem poly_81_iso_0_loser : defeated_by poly_81_iso_0 PavingH = true := by {
  decide
}

def poly_81_iso_1 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (3,3)]
theorem poly_81_iso_1_loser : defeated_by poly_81_iso_1 PavingH = true := by {
  decide
}

def poly_81_iso_2 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,0), (3,0)]
theorem poly_81_iso_2_loser : defeated_by poly_81_iso_2 PavingH = true := by {
  decide
}

def poly_81_iso_3 : Polyomino := [(0,2), (0,3), (1,2), (2,2), (3,0), (3,1), (3,2)]
theorem poly_81_iso_3_loser : defeated_by poly_81_iso_3 PavingH = true := by {
  decide
}

def poly_81_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,2), (3,2), (3,3)]
theorem poly_81_iso_4_loser : defeated_by poly_81_iso_4 PavingH = true := by {
  decide
}

def poly_81_iso_5 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,1), (3,2), (3,3)]
theorem poly_81_iso_5_loser : defeated_by poly_81_iso_5 PavingH = true := by {
  decide
}

def poly_81_iso_6 : Polyomino := [(0,3), (1,3), (2,0), (2,1), (2,2), (2,3), (3,0)]
theorem poly_81_iso_6_loser : defeated_by poly_81_iso_6 PavingH = true := by {
  decide
}

def poly_81_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,3), (3,3)]
theorem poly_81_iso_7_loser : defeated_by poly_81_iso_7 PavingH = true := by {
  decide
}

def poly_82_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,2), (2,2)]
theorem poly_82_iso_0_loser : defeated_by poly_82_iso_0 PavingH = true := by {
  decide
}

def poly_82_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (2,1), (2,2), (3,0)]
theorem poly_82_iso_1_loser : defeated_by poly_82_iso_1 PavingH = true := by {
  decide
}

def poly_82_iso_2 : Polyomino := [(0,1), (1,1), (1,3), (2,0), (2,1), (2,2), (2,3)]
theorem poly_82_iso_2_loser : defeated_by poly_82_iso_2 PavingH = true := by {
  decide
}

def poly_82_iso_3 : Polyomino := [(0,1), (0,2), (1,2), (2,0), (2,1), (2,2), (3,2)]
theorem poly_82_iso_3_loser : defeated_by poly_82_iso_3 PavingH = true := by {
  decide
}

def poly_82_iso_4 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (3,0), (3,1)]
theorem poly_82_iso_4_loser : defeated_by poly_82_iso_4 PavingH = true := by {
  decide
}

def poly_82_iso_5 : Polyomino := [(0,2), (1,0), (1,2), (2,0), (2,1), (2,2), (2,3)]
theorem poly_82_iso_5_loser : defeated_by poly_82_iso_5 PavingH = true := by {
  decide
}

def poly_82_iso_6 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,2), (3,1), (3,2)]
theorem poly_82_iso_6_loser : defeated_by poly_82_iso_6 PavingH = true := by {
  decide
}

def poly_82_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,1), (1,3), (2,1)]
theorem poly_82_iso_7_loser : defeated_by poly_82_iso_7 PavingH = true := by {
  decide
}

def poly_83_iso_0 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (2,2), (3,2)]
theorem poly_83_iso_0_loser : defeated_by poly_83_iso_0 PavingH = true := by {
  decide
}

def poly_83_iso_1 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (3,0)]
theorem poly_83_iso_1_loser : defeated_by poly_83_iso_1 PavingH = true := by {
  decide
}

def poly_83_iso_2 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (2,0), (2,1)]
theorem poly_83_iso_2_loser : defeated_by poly_83_iso_2 PavingH = true := by {
  decide
}

def poly_83_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (2,2), (2,3)]
theorem poly_83_iso_3_loser : defeated_by poly_83_iso_3 PavingH = true := by {
  decide
}

def poly_83_iso_4 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (3,0), (3,1)]
theorem poly_83_iso_4_loser : defeated_by poly_83_iso_4 PavingH = true := by {
  decide
}

def poly_83_iso_5 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (3,1), (3,2)]
theorem poly_83_iso_5_loser : defeated_by poly_83_iso_5 PavingH = true := by {
  decide
}

def poly_83_iso_6 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,1), (2,2), (2,3)]
theorem poly_83_iso_6_loser : defeated_by poly_83_iso_6 PavingH = true := by {
  decide
}

def poly_83_iso_7 : Polyomino := [(0,2), (0,3), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_83_iso_7_loser : defeated_by poly_83_iso_7 PavingH = true := by {
  decide
}

def poly_84_iso_0 : Polyomino := [(0,0), (0,3), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_84_iso_0_loser : defeated_by poly_84_iso_0 PavingH = true := by {
  decide
}

def poly_84_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,1), (3,0), (3,1)]
theorem poly_84_iso_1_loser : defeated_by poly_84_iso_1 PavingH = true := by {
  decide
}

def poly_84_iso_2 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,1), (3,1), (3,2)]
theorem poly_84_iso_2_loser : defeated_by poly_84_iso_2 PavingH = true := by {
  decide
}

def poly_84_iso_3 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (3,0), (3,1)]
theorem poly_84_iso_3_loser : defeated_by poly_84_iso_3 PavingH = true := by {
  decide
}

def poly_84_iso_4 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (3,1), (3,2)]
theorem poly_84_iso_4_loser : defeated_by poly_84_iso_4 PavingH = true := by {
  decide
}

def poly_84_iso_5 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,0), (2,3)]
theorem poly_84_iso_5_loser : defeated_by poly_84_iso_5 PavingH = true := by {
  decide
}

def poly_84_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,0), (2,3)]
theorem poly_84_iso_6_loser : defeated_by poly_84_iso_6 PavingH = true := by {
  decide
}

def poly_84_iso_7 : Polyomino := [(0,0), (0,3), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_84_iso_7_loser : defeated_by poly_84_iso_7 PavingH = true := by {
  decide
}

def poly_85_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (3,2), (4,2)]
theorem poly_85_iso_0_loser : defeated_by poly_85_iso_0 PavingH = true := by {
  decide
}

def poly_85_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (1,4), (2,3)]
theorem poly_85_iso_1_loser : defeated_by poly_85_iso_1 PavingH = true := by {
  decide
}

def poly_85_iso_2 : Polyomino := [(0,2), (1,2), (2,1), (2,2), (3,0), (3,1), (4,1)]
theorem poly_85_iso_2_loser : defeated_by poly_85_iso_2 PavingH = true := by {
  decide
}

def poly_85_iso_3 : Polyomino := [(0,3), (1,2), (1,3), (1,4), (2,0), (2,1), (2,2)]
theorem poly_85_iso_3_loser : defeated_by poly_85_iso_3 PavingH = true := by {
  decide
}

def poly_85_iso_4 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,1), (3,2), (4,1)]
theorem poly_85_iso_4_loser : defeated_by poly_85_iso_4 PavingH = true := by {
  decide
}

def poly_85_iso_5 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,2), (2,3), (2,4)]
theorem poly_85_iso_5_loser : defeated_by poly_85_iso_5 PavingH = true := by {
  decide
}

def poly_85_iso_6 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (3,0), (4,0)]
theorem poly_85_iso_6_loser : defeated_by poly_85_iso_6 PavingH = true := by {
  decide
}

def poly_85_iso_7 : Polyomino := [(0,2), (0,3), (0,4), (1,0), (1,1), (1,2), (2,1)]
theorem poly_85_iso_7_loser : defeated_by poly_85_iso_7 PavingH = true := by {
  decide
}

def poly_86_iso_0 : Polyomino := [(0,4), (1,0), (1,1), (1,2), (1,3), (1,4), (2,1)]
theorem poly_86_iso_0_loser : defeated_by poly_86_iso_0 PavingH = true := by {
  decide
}

def poly_86_iso_1 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (1,4), (2,0)]
theorem poly_86_iso_1_loser : defeated_by poly_86_iso_1 PavingH = true := by {
  decide
}

def poly_86_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (1,4), (2,4)]
theorem poly_86_iso_2_loser : defeated_by poly_86_iso_2 PavingH = true := by {
  decide
}

def poly_86_iso_3 : Polyomino := [(0,1), (1,1), (1,2), (2,1), (3,1), (4,0), (4,1)]
theorem poly_86_iso_3_loser : defeated_by poly_86_iso_3 PavingH = true := by {
  decide
}

def poly_86_iso_4 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (2,3)]
theorem poly_86_iso_4_loser : defeated_by poly_86_iso_4 PavingH = true := by {
  decide
}

def poly_86_iso_5 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (3,1), (4,1), (4,2)]
theorem poly_86_iso_5_loser : defeated_by poly_86_iso_5 PavingH = true := by {
  decide
}

def poly_86_iso_6 : Polyomino := [(0,1), (0,2), (1,1), (2,1), (3,0), (3,1), (4,1)]
theorem poly_86_iso_6_loser : defeated_by poly_86_iso_6 PavingH = true := by {
  decide
}

def poly_86_iso_7 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,1), (3,2), (4,1)]
theorem poly_86_iso_7_loser : defeated_by poly_86_iso_7 PavingH = true := by {
  decide
}

def poly_87_iso_0 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,1), (3,0), (3,1)]
theorem poly_87_iso_0_loser : defeated_by poly_87_iso_0 PavingH = true := by {
  decide
}

def poly_87_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (2,0), (2,1), (2,2), (3,2)]
theorem poly_87_iso_1_loser : defeated_by poly_87_iso_1 PavingH = true := by {
  decide
}

def poly_87_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,1), (2,3)]
theorem poly_87_iso_2_loser : defeated_by poly_87_iso_2 PavingH = true := by {
  decide
}

def poly_87_iso_3 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (2,2), (2,3)]
theorem poly_87_iso_3_loser : defeated_by poly_87_iso_3 PavingH = true := by {
  decide
}

def poly_87_iso_4 : Polyomino := [(0,1), (0,3), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_87_iso_4_loser : defeated_by poly_87_iso_4 PavingH = true := by {
  decide
}

def poly_87_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,1), (3,1), (3,2)]
theorem poly_87_iso_5_loser : defeated_by poly_87_iso_5 PavingH = true := by {
  decide
}

def poly_87_iso_6 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (2,2), (3,0)]
theorem poly_87_iso_6_loser : defeated_by poly_87_iso_6 PavingH = true := by {
  decide
}

def poly_87_iso_7 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (2,0), (2,2)]
theorem poly_87_iso_7_loser : defeated_by poly_87_iso_7 PavingH = true := by {
  decide
}

def poly_88_iso_0 : Polyomino := [(0,2), (1,1), (1,2), (1,3), (2,0), (2,1), (3,1)]
theorem poly_88_iso_0_loser : defeated_by poly_88_iso_0 PavingH = true := by {
  decide
}

def poly_88_iso_1 : Polyomino := [(0,2), (1,2), (1,3), (2,0), (2,1), (2,2), (3,1)]
theorem poly_88_iso_1_loser : defeated_by poly_88_iso_1 PavingH = true := by {
  decide
}

def poly_88_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,2), (2,3), (3,2)]
theorem poly_88_iso_2_loser : defeated_by poly_88_iso_2 PavingH = true := by {
  decide
}

def poly_88_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (2,3), (3,2)]
theorem poly_88_iso_3_loser : defeated_by poly_88_iso_3 PavingH = true := by {
  decide
}

def poly_89_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,2), (3,2)]
theorem poly_89_iso_0_loser : defeated_by poly_89_iso_0 PavingH = true := by {
  decide
}

def poly_89_iso_1 : Polyomino := [(0,2), (1,2), (1,3), (2,0), (2,1), (2,2), (3,2)]
theorem poly_89_iso_1_loser : defeated_by poly_89_iso_1 PavingH = true := by {
  decide
}

def poly_89_iso_2 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (2,3), (3,1)]
theorem poly_89_iso_2_loser : defeated_by poly_89_iso_2 PavingH = true := by {
  decide
}

def poly_89_iso_3 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,2), (2,3), (3,2)]
theorem poly_89_iso_3_loser : defeated_by poly_89_iso_3 PavingH = true := by {
  decide
}

def poly_89_iso_4 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (2,3), (3,1)]
theorem poly_89_iso_4_loser : defeated_by poly_89_iso_4 PavingH = true := by {
  decide
}

def poly_89_iso_5 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (2,3), (3,2)]
theorem poly_89_iso_5_loser : defeated_by poly_89_iso_5 PavingH = true := by {
  decide
}

def poly_89_iso_6 : Polyomino := [(0,1), (1,1), (1,2), (1,3), (2,0), (2,1), (3,1)]
theorem poly_89_iso_6_loser : defeated_by poly_89_iso_6 PavingH = true := by {
  decide
}

def poly_89_iso_7 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,1), (3,1)]
theorem poly_89_iso_7_loser : defeated_by poly_89_iso_7 PavingH = true := by {
  decide
}

def poly_90_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (1,3)]
theorem poly_90_iso_0_loser : defeated_by poly_90_iso_0 PavingBrick = true := by {
  decide
}

def poly_90_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (3,0), (3,1), (4,0)]
theorem poly_90_iso_1_loser : defeated_by poly_90_iso_1 PavingBrick = true := by {
  decide
}

def poly_90_iso_2 : Polyomino := [(0,1), (0,4), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_90_iso_2_loser : defeated_by poly_90_iso_2 PavingBrick = true := by {
  decide
}

def poly_90_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (3,1), (4,0), (4,1)]
theorem poly_90_iso_3_loser : defeated_by poly_90_iso_3 PavingBrick = true := by {
  decide
}

def poly_90_iso_4 : Polyomino := [(0,0), (0,3), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_90_iso_4_loser : defeated_by poly_90_iso_4 PavingBrick = true := by {
  decide
}

def poly_90_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,1), (1,4)]
theorem poly_90_iso_5_loser : defeated_by poly_90_iso_5 PavingBrick = true := by {
  decide
}

def poly_90_iso_6 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (3,0), (4,0), (4,1)]
theorem poly_90_iso_6_loser : defeated_by poly_90_iso_6 PavingBrick = true := by {
  decide
}

def poly_90_iso_7 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,0), (3,1), (4,1)]
theorem poly_90_iso_7_loser : defeated_by poly_90_iso_7 PavingBrick = true := by {
  decide
}

def poly_91_iso_0 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (1,4), (2,2)]
theorem poly_91_iso_0_loser : defeated_by poly_91_iso_0 PavingH = true := by {
  decide
}

def poly_91_iso_1 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (3,1), (4,1)]
theorem poly_91_iso_1_loser : defeated_by poly_91_iso_1 PavingH = true := by {
  decide
}

def poly_92_iso_0 : Polyomino := [(0,1), (0,2), (0,3), (1,1), (2,0), (2,1), (2,2)]
theorem poly_92_iso_0_loser : defeated_by poly_92_iso_0 PavingH = true := by {
  decide
}

def poly_92_iso_1 : Polyomino := [(0,0), (1,0), (1,2), (2,0), (2,1), (2,2), (3,2)]
theorem poly_92_iso_1_loser : defeated_by poly_92_iso_1 PavingH = true := by {
  decide
}

def poly_92_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (2,2), (3,0)]
theorem poly_92_iso_2_loser : defeated_by poly_92_iso_2 PavingH = true := by {
  decide
}

def poly_92_iso_3 : Polyomino := [(0,2), (1,0), (1,2), (2,0), (2,1), (2,2), (3,0)]
theorem poly_92_iso_3_loser : defeated_by poly_92_iso_3 PavingH = true := by {
  decide
}

def poly_92_iso_4 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (2,2), (3,2)]
theorem poly_92_iso_4_loser : defeated_by poly_92_iso_4 PavingH = true := by {
  decide
}

def poly_92_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,1), (2,2), (2,3)]
theorem poly_92_iso_5_loser : defeated_by poly_92_iso_5 PavingH = true := by {
  decide
}

def poly_92_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,1), (2,2), (2,3)]
theorem poly_92_iso_6_loser : defeated_by poly_92_iso_6 PavingH = true := by {
  decide
}

def poly_92_iso_7 : Polyomino := [(0,1), (0,2), (0,3), (1,2), (2,0), (2,1), (2,2)]
theorem poly_92_iso_7_loser : defeated_by poly_92_iso_7 PavingH = true := by {
  decide
}

def poly_93_iso_0 : Polyomino := [(0,2), (1,2), (1,3), (2,1), (2,2), (3,0), (3,1)]
theorem poly_93_iso_0_loser : defeated_by poly_93_iso_0 PavingH = true := by {
  decide
}

def poly_93_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (3,2), (3,3)]
theorem poly_93_iso_1_loser : defeated_by poly_93_iso_1 PavingH = true := by {
  decide
}

def poly_93_iso_2 : Polyomino := [(0,3), (1,2), (1,3), (2,0), (2,1), (2,2), (3,1)]
theorem poly_93_iso_2_loser : defeated_by poly_93_iso_2 PavingH = true := by {
  decide
}

def poly_93_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,2), (2,3), (3,3)]
theorem poly_93_iso_3_loser : defeated_by poly_93_iso_3 PavingH = true := by {
  decide
}

def poly_93_iso_4 : Polyomino := [(0,2), (0,3), (1,1), (1,2), (2,0), (2,1), (3,1)]
theorem poly_93_iso_4_loser : defeated_by poly_93_iso_4 PavingH = true := by {
  decide
}

def poly_93_iso_5 : Polyomino := [(0,2), (1,1), (1,2), (1,3), (2,0), (2,1), (3,0)]
theorem poly_93_iso_5_loser : defeated_by poly_93_iso_5 PavingH = true := by {
  decide
}

def poly_93_iso_6 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (2,3), (3,2)]
theorem poly_93_iso_6_loser : defeated_by poly_93_iso_6 PavingH = true := by {
  decide
}

def poly_93_iso_7 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,2)]
theorem poly_93_iso_7_loser : defeated_by poly_93_iso_7 PavingH = true := by {
  decide
}

def poly_94_iso_0 : Polyomino := [(0,1), (1,1), (1,2), (1,3), (2,0), (2,1), (2,3)]
theorem poly_94_iso_0_loser : defeated_by poly_94_iso_0 PavingH = true := by {
  decide
}

def poly_94_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (2,0), (2,1), (2,2), (3,0)]
theorem poly_94_iso_1_loser : defeated_by poly_94_iso_1 PavingH = true := by {
  decide
}

def poly_94_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (2,2), (2,3)]
theorem poly_94_iso_2_loser : defeated_by poly_94_iso_2 PavingH = true := by {
  decide
}

def poly_94_iso_3 : Polyomino := [(0,0), (0,2), (0,3), (1,0), (1,1), (1,2), (2,2)]
theorem poly_94_iso_3_loser : defeated_by poly_94_iso_3 PavingH = true := by {
  decide
}

def poly_94_iso_4 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,1), (3,1), (3,2)]
theorem poly_94_iso_4_loser : defeated_by poly_94_iso_4 PavingH = true := by {
  decide
}

def poly_94_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,1), (3,0), (3,1)]
theorem poly_94_iso_5_loser : defeated_by poly_94_iso_5 PavingH = true := by {
  decide
}

def poly_94_iso_6 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (2,2), (3,2)]
theorem poly_94_iso_6_loser : defeated_by poly_94_iso_6 PavingH = true := by {
  decide
}

def poly_94_iso_7 : Polyomino := [(0,0), (0,1), (0,3), (1,1), (1,2), (1,3), (2,1)]
theorem poly_94_iso_7_loser : defeated_by poly_94_iso_7 PavingH = true := by {
  decide
}

def poly_95_iso_0 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,1), (3,2), (3,3)]
theorem poly_95_iso_0_loser : defeated_by poly_95_iso_0 PavingH = true := by {
  decide
}

def poly_95_iso_1 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,3), (3,3)]
theorem poly_95_iso_1_loser : defeated_by poly_95_iso_1 PavingH = true := by {
  decide
}

def poly_95_iso_2 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (2,1), (3,1)]
theorem poly_95_iso_2_loser : defeated_by poly_95_iso_2 PavingH = true := by {
  decide
}

def poly_95_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (2,2), (3,2)]
theorem poly_95_iso_3_loser : defeated_by poly_95_iso_3 PavingH = true := by {
  decide
}

def poly_95_iso_4 : Polyomino := [(0,2), (1,2), (2,2), (2,3), (3,0), (3,1), (3,2)]
theorem poly_95_iso_4_loser : defeated_by poly_95_iso_4 PavingH = true := by {
  decide
}

def poly_95_iso_5 : Polyomino := [(0,3), (1,3), (2,0), (2,1), (2,2), (2,3), (3,2)]
theorem poly_95_iso_5_loser : defeated_by poly_95_iso_5 PavingH = true := by {
  decide
}

def poly_95_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,0), (3,0)]
theorem poly_95_iso_6_loser : defeated_by poly_95_iso_6 PavingH = true := by {
  decide
}

def poly_95_iso_7 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (3,1)]
theorem poly_95_iso_7_loser : defeated_by poly_95_iso_7 PavingH = true := by {
  decide
}

def poly_96_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,4), (1,2), (1,3), (1,4)]
theorem poly_96_iso_0_loser : defeated_by poly_96_iso_0 PavingStripesH = true := by {
  decide
}

def poly_96_iso_1 : Polyomino := [(0,2), (0,3), (0,4), (1,0), (1,1), (1,2), (1,4)]
theorem poly_96_iso_1_loser : defeated_by poly_96_iso_1 PavingStripesH = true := by {
  decide
}

def poly_96_iso_2 : Polyomino := [(0,0), (0,2), (0,3), (0,4), (1,0), (1,1), (1,2)]
theorem poly_96_iso_2_loser : defeated_by poly_96_iso_2 PavingStripesH = true := by {
  decide
}

def poly_96_iso_3 : Polyomino := [(0,0), (0,1), (1,1), (2,0), (2,1), (3,0), (4,0)]
theorem poly_96_iso_3_loser : defeated_by poly_96_iso_3 PavingStripesH = true := by {
  decide
}

def poly_96_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (1,3), (1,4)]
theorem poly_96_iso_4_loser : defeated_by poly_96_iso_4 PavingStripesH = true := by {
  decide
}

def poly_96_iso_5 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,0), (4,0), (4,1)]
theorem poly_96_iso_5_loser : defeated_by poly_96_iso_5 PavingStripesH = true := by {
  decide
}

def poly_96_iso_6 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (2,1), (3,1), (4,1)]
theorem poly_96_iso_6_loser : defeated_by poly_96_iso_6 PavingStripesH = true := by {
  decide
}

def poly_96_iso_7 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,1), (4,0), (4,1)]
theorem poly_96_iso_7_loser : defeated_by poly_96_iso_7 PavingStripesH = true := by {
  decide
}

def poly_97_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (3,1), (3,2), (4,2)]
theorem poly_97_iso_0_loser : defeated_by poly_97_iso_0 PavingH = true := by {
  decide
}

def poly_97_iso_1 : Polyomino := [(0,2), (1,1), (1,2), (2,1), (3,0), (3,1), (4,1)]
theorem poly_97_iso_1_loser : defeated_by poly_97_iso_1 PavingH = true := by {
  decide
}

def poly_97_iso_2 : Polyomino := [(0,3), (1,1), (1,2), (1,3), (1,4), (2,0), (2,1)]
theorem poly_97_iso_2_loser : defeated_by poly_97_iso_2 PavingH = true := by {
  decide
}

def poly_97_iso_3 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (1,4), (2,3)]
theorem poly_97_iso_3_loser : defeated_by poly_97_iso_3 PavingH = true := by {
  decide
}

def poly_97_iso_4 : Polyomino := [(0,1), (1,1), (1,2), (2,1), (3,0), (3,1), (4,0)]
theorem poly_97_iso_4_loser : defeated_by poly_97_iso_4 PavingH = true := by {
  decide
}

def poly_97_iso_5 : Polyomino := [(0,3), (0,4), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_97_iso_5_loser : defeated_by poly_97_iso_5 PavingH = true := by {
  decide
}

def poly_97_iso_6 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (3,1), (3,2), (4,1)]
theorem poly_97_iso_6_loser : defeated_by poly_97_iso_6 PavingH = true := by {
  decide
}

def poly_97_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,3), (2,4)]
theorem poly_97_iso_7_loser : defeated_by poly_97_iso_7 PavingH = true := by {
  decide
}

def poly_98_iso_0 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_98_iso_0_loser : defeated_by poly_98_iso_0 PavingBrick = true := by {
  decide
}

def poly_98_iso_1 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,0), (3,1), (4,0)]
theorem poly_98_iso_1_loser : defeated_by poly_98_iso_1 PavingBrick = true := by {
  decide
}

def poly_98_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,2), (1,3)]
theorem poly_98_iso_2_loser : defeated_by poly_98_iso_2 PavingBrick = true := by {
  decide
}

def poly_98_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,1), (1,2)]
theorem poly_98_iso_3_loser : defeated_by poly_98_iso_3 PavingBrick = true := by {
  decide
}

def poly_98_iso_4 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_98_iso_4_loser : defeated_by poly_98_iso_4 PavingBrick = true := by {
  decide
}

def poly_98_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (3,0), (4,0)]
theorem poly_98_iso_5_loser : defeated_by poly_98_iso_5 PavingBrick = true := by {
  decide
}

def poly_98_iso_6 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,0), (3,1), (4,1)]
theorem poly_98_iso_6_loser : defeated_by poly_98_iso_6 PavingBrick = true := by {
  decide
}

def poly_98_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (3,1), (4,1)]
theorem poly_98_iso_7_loser : defeated_by poly_98_iso_7 PavingBrick = true := by {
  decide
}

def poly_99_iso_0 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (1,4), (2,1)]
theorem poly_99_iso_0_loser : defeated_by poly_99_iso_0 PavingH = true := by {
  decide
}

def poly_99_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (1,4), (2,3)]
theorem poly_99_iso_1_loser : defeated_by poly_99_iso_1 PavingH = true := by {
  decide
}

def poly_99_iso_2 : Polyomino := [(0,1), (1,1), (1,2), (2,1), (3,0), (3,1), (4,1)]
theorem poly_99_iso_2_loser : defeated_by poly_99_iso_2 PavingH = true := by {
  decide
}

def poly_99_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (3,1), (3,2), (4,1)]
theorem poly_99_iso_3_loser : defeated_by poly_99_iso_3 PavingH = true := by {
  decide
}

def poly_100_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,3), (2,4)]
theorem poly_100_iso_0_loser : defeated_by poly_100_iso_0 PavingH = true := by {
  decide
}

def poly_100_iso_1 : Polyomino := [(0,3), (0,4), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_100_iso_1_loser : defeated_by poly_100_iso_1 PavingH = true := by {
  decide
}

def poly_100_iso_2 : Polyomino := [(0,2), (1,1), (1,2), (2,1), (3,0), (3,1), (4,0)]
theorem poly_100_iso_2_loser : defeated_by poly_100_iso_2 PavingH = true := by {
  decide
}

def poly_100_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (3,1), (3,2), (4,2)]
theorem poly_100_iso_3_loser : defeated_by poly_100_iso_3 PavingH = true := by {
  decide
}

def poly_101_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (2,0), (2,1), (2,2), (2,3)]
theorem poly_101_iso_0_loser : defeated_by poly_101_iso_0 PavingH = true := by {
  decide
}

def poly_101_iso_1 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (3,0), (3,2)]
theorem poly_101_iso_1_loser : defeated_by poly_101_iso_1 PavingH = true := by {
  decide
}

def poly_101_iso_2 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (2,0), (3,0)]
theorem poly_101_iso_2_loser : defeated_by poly_101_iso_2 PavingH = true := by {
  decide
}

def poly_101_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,2), (2,2), (2,3)]
theorem poly_101_iso_3_loser : defeated_by poly_101_iso_3 PavingH = true := by {
  decide
}

def poly_101_iso_4 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (3,0), (3,2)]
theorem poly_101_iso_4_loser : defeated_by poly_101_iso_4 PavingH = true := by {
  decide
}

def poly_101_iso_5 : Polyomino := [(0,2), (0,3), (1,2), (2,0), (2,1), (2,2), (2,3)]
theorem poly_101_iso_5_loser : defeated_by poly_101_iso_5 PavingH = true := by {
  decide
}

def poly_101_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,1), (2,0), (2,1)]
theorem poly_101_iso_6_loser : defeated_by poly_101_iso_6 PavingH = true := by {
  decide
}

def poly_101_iso_7 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (2,2), (3,2)]
theorem poly_101_iso_7_loser : defeated_by poly_101_iso_7 PavingH = true := by {
  decide
}

def poly_102_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_102_iso_0_loser : defeated_by poly_102_iso_0 PavingH = true := by {
  decide
}

def poly_102_iso_1 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (2,1), (3,1)]
theorem poly_102_iso_1_loser : defeated_by poly_102_iso_1 PavingH = true := by {
  decide
}

def poly_102_iso_2 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (3,0), (3,2)]
theorem poly_102_iso_2_loser : defeated_by poly_102_iso_2 PavingH = true := by {
  decide
}

def poly_102_iso_3 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (2,2), (2,3)]
theorem poly_102_iso_3_loser : defeated_by poly_102_iso_3 PavingH = true := by {
  decide
}

def poly_103_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,2), (1,3)]
theorem poly_103_iso_0_loser : defeated_by poly_103_iso_0 PavingBrick = true := by {
  decide
}

def poly_103_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,3)]
theorem poly_103_iso_1_loser : defeated_by poly_103_iso_1 PavingBrick = true := by {
  decide
}

def poly_103_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (2,0), (2,1), (3,0), (3,1)]
theorem poly_103_iso_2_loser : defeated_by poly_103_iso_2 PavingBrick = true := by {
  decide
}

def poly_103_iso_3 : Polyomino := [(0,0), (0,2), (0,3), (1,0), (1,1), (1,2), (1,3)]
theorem poly_103_iso_3_loser : defeated_by poly_103_iso_3 PavingBrick = true := by {
  decide
}

def poly_103_iso_4 : Polyomino := [(0,0), (0,1), (0,3), (1,0), (1,1), (1,2), (1,3)]
theorem poly_103_iso_4_loser : defeated_by poly_103_iso_4 PavingBrick = true := by {
  decide
}

def poly_103_iso_5 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,1), (3,0), (3,1)]
theorem poly_103_iso_5_loser : defeated_by poly_103_iso_5 PavingBrick = true := by {
  decide
}

def poly_103_iso_6 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (2,1), (3,0), (3,1)]
theorem poly_103_iso_6_loser : defeated_by poly_103_iso_6 PavingBrick = true := by {
  decide
}

def poly_103_iso_7 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,0), (3,0), (3,1)]
theorem poly_103_iso_7_loser : defeated_by poly_103_iso_7 PavingBrick = true := by {
  decide
}

def poly_104_iso_0 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (3,1), (3,2), (4,1)]
theorem poly_104_iso_0_loser : defeated_by poly_104_iso_0 PavingH = true := by {
  decide
}

def poly_104_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,2), (3,2), (4,2)]
theorem poly_104_iso_1_loser : defeated_by poly_104_iso_1 PavingH = true := by {
  decide
}

def poly_104_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (2,3), (2,4)]
theorem poly_104_iso_2_loser : defeated_by poly_104_iso_2 PavingH = true := by {
  decide
}

def poly_104_iso_3 : Polyomino := [(0,3), (1,3), (1,4), (2,0), (2,1), (2,2), (2,3)]
theorem poly_104_iso_3_loser : defeated_by poly_104_iso_3 PavingH = true := by {
  decide
}

def poly_104_iso_4 : Polyomino := [(0,2), (1,2), (2,2), (3,0), (3,1), (3,2), (4,1)]
theorem poly_104_iso_4_loser : defeated_by poly_104_iso_4 PavingH = true := by {
  decide
}

def poly_104_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,3), (1,4), (2,3)]
theorem poly_104_iso_5_loser : defeated_by poly_104_iso_5 PavingH = true := by {
  decide
}

def poly_104_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (3,0), (4,0)]
theorem poly_104_iso_6_loser : defeated_by poly_104_iso_6 PavingH = true := by {
  decide
}

def poly_104_iso_7 : Polyomino := [(0,1), (0,2), (0,3), (0,4), (1,0), (1,1), (2,1)]
theorem poly_104_iso_7_loser : defeated_by poly_104_iso_7 PavingH = true := by {
  decide
}

def poly_105_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,2), (3,2), (4,2)]
theorem poly_105_iso_0_loser : defeated_by poly_105_iso_0 PavingH = true := by {
  decide
}

def poly_105_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4)]
theorem poly_105_iso_1_loser : defeated_by poly_105_iso_1 PavingH = true := by {
  decide
}

def poly_105_iso_2 : Polyomino := [(0,4), (1,4), (2,0), (2,1), (2,2), (2,3), (2,4)]
theorem poly_105_iso_2_loser : defeated_by poly_105_iso_2 PavingH = true := by {
  decide
}

def poly_105_iso_3 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (2,4)]
theorem poly_105_iso_3_loser : defeated_by poly_105_iso_3 PavingH = true := by {
  decide
}

def poly_105_iso_4 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (4,0), (4,1), (4,2)]
theorem poly_105_iso_4_loser : defeated_by poly_105_iso_4 PavingH = true := by {
  decide
}

def poly_105_iso_5 : Polyomino := [(0,2), (1,2), (2,2), (3,2), (4,0), (4,1), (4,2)]
theorem poly_105_iso_5_loser : defeated_by poly_105_iso_5 PavingH = true := by {
  decide
}

def poly_105_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (2,0)]
theorem poly_105_iso_6_loser : defeated_by poly_105_iso_6 PavingH = true := by {
  decide
}

def poly_105_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (2,0), (3,0), (4,0)]
theorem poly_105_iso_7_loser : defeated_by poly_105_iso_7 PavingH = true := by {
  decide
}

def poly_106_iso_0 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (2,0), (2,2)]
theorem poly_106_iso_0_loser : defeated_by poly_106_iso_0 PavingH = true := by {
  decide
}

def poly_106_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,0), (2,1), (2,2)]
theorem poly_106_iso_1_loser : defeated_by poly_106_iso_1 PavingH = true := by {
  decide
}

def poly_107_iso_0 : Polyomino := [(0,1), (0,2), (0,3), (0,4), (1,0), (1,1), (1,4)]
theorem poly_107_iso_0_loser : defeated_by poly_107_iso_0 PavingBrick = true := by {
  decide
}

def poly_107_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (3,0), (4,0), (4,1)]
theorem poly_107_iso_1_loser : defeated_by poly_107_iso_1 PavingBrick = true := by {
  decide
}

def poly_107_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (3,1), (4,0), (4,1)]
theorem poly_107_iso_2_loser : defeated_by poly_107_iso_2 PavingBrick = true := by {
  decide
}

def poly_107_iso_3 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,0), (3,1), (4,0)]
theorem poly_107_iso_3_loser : defeated_by poly_107_iso_3 PavingBrick = true := by {
  decide
}

def poly_107_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,3), (1,4)]
theorem poly_107_iso_4_loser : defeated_by poly_107_iso_4 PavingBrick = true := by {
  decide
}

def poly_107_iso_5 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (3,0), (3,1), (4,1)]
theorem poly_107_iso_5_loser : defeated_by poly_107_iso_5 PavingBrick = true := by {
  decide
}

def poly_107_iso_6 : Polyomino := [(0,0), (0,3), (0,4), (1,0), (1,1), (1,2), (1,3)]
theorem poly_107_iso_6_loser : defeated_by poly_107_iso_6 PavingBrick = true := by {
  decide
}

def poly_107_iso_7 : Polyomino := [(0,0), (0,1), (0,4), (1,1), (1,2), (1,3), (1,4)]
theorem poly_107_iso_7_loser : defeated_by poly_107_iso_7 PavingBrick = true := by {
  decide
}

def poly_108_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (3,0), (3,1), (4,0)]
theorem poly_108_iso_0_loser : defeated_by poly_108_iso_0 PavingStripesH = true := by {
  decide
}

def poly_108_iso_1 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (1,3), (1,4)]
theorem poly_108_iso_1_loser : defeated_by poly_108_iso_1 PavingStripesH = true := by {
  decide
}

def poly_108_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (3,0), (3,1), (4,1)]
theorem poly_108_iso_2_loser : defeated_by poly_108_iso_2 PavingStripesH = true := by {
  decide
}

def poly_108_iso_3 : Polyomino := [(0,0), (0,1), (0,3), (0,4), (1,1), (1,2), (1,3)]
theorem poly_108_iso_3_loser : defeated_by poly_108_iso_3 PavingStripesH = true := by {
  decide
}

def poly_109_iso_0 : Polyomino := [(0,2), (1,1), (1,2), (2,1), (3,1), (4,0), (4,1)]
theorem poly_109_iso_0_loser : defeated_by poly_109_iso_0 PavingH = true := by {
  decide
}

def poly_109_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (3,1), (4,1), (4,2)]
theorem poly_109_iso_1_loser : defeated_by poly_109_iso_1 PavingH = true := by {
  decide
}

def poly_109_iso_2 : Polyomino := [(0,1), (0,2), (1,1), (2,1), (3,0), (3,1), (4,0)]
theorem poly_109_iso_2_loser : defeated_by poly_109_iso_2 PavingH = true := by {
  decide
}

def poly_109_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,3), (2,4)]
theorem poly_109_iso_3_loser : defeated_by poly_109_iso_3 PavingH = true := by {
  decide
}

def poly_109_iso_4 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,1), (3,2), (4,2)]
theorem poly_109_iso_4_loser : defeated_by poly_109_iso_4 PavingH = true := by {
  decide
}

def poly_109_iso_5 : Polyomino := [(0,3), (0,4), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_109_iso_5_loser : defeated_by poly_109_iso_5 PavingH = true := by {
  decide
}

def poly_109_iso_6 : Polyomino := [(0,4), (1,1), (1,2), (1,3), (1,4), (2,0), (2,1)]
theorem poly_109_iso_6_loser : defeated_by poly_109_iso_6 PavingH = true := by {
  decide
}

def poly_109_iso_7 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (1,4), (2,4)]
theorem poly_109_iso_7_loser : defeated_by poly_109_iso_7 PavingH = true := by {
  decide
}

def poly_110_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (3,1), (3,2)]
theorem poly_110_iso_0_loser : defeated_by poly_110_iso_0 PavingH = true := by {
  decide
}

def poly_110_iso_1 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (3,0), (3,1)]
theorem poly_110_iso_1_loser : defeated_by poly_110_iso_1 PavingH = true := by {
  decide
}

def poly_110_iso_2 : Polyomino := [(0,2), (0,3), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_110_iso_2_loser : defeated_by poly_110_iso_2 PavingH = true := by {
  decide
}

def poly_110_iso_3 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,2), (2,3)]
theorem poly_110_iso_3_loser : defeated_by poly_110_iso_3 PavingH = true := by {
  decide
}

def poly_110_iso_4 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (2,0), (2,1)]
theorem poly_110_iso_4_loser : defeated_by poly_110_iso_4 PavingH = true := by {
  decide
}

def poly_110_iso_5 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (2,2), (2,3)]
theorem poly_110_iso_5_loser : defeated_by poly_110_iso_5 PavingH = true := by {
  decide
}

def poly_110_iso_6 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,1), (2,2), (3,2)]
theorem poly_110_iso_6_loser : defeated_by poly_110_iso_6 PavingH = true := by {
  decide
}

def poly_110_iso_7 : Polyomino := [(0,1), (0,2), (1,1), (1,2), (2,0), (2,1), (3,0)]
theorem poly_110_iso_7_loser : defeated_by poly_110_iso_7 PavingH = true := by {
  decide
}

def poly_111_iso_0 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_111_iso_0_loser : defeated_by poly_111_iso_0 PavingH = true := by {
  decide
}

def poly_111_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,1), (2,2)]
theorem poly_111_iso_1_loser : defeated_by poly_111_iso_1 PavingH = true := by {
  decide
}

def poly_111_iso_2 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,0), (2,1), (3,1)]
theorem poly_111_iso_2_loser : defeated_by poly_111_iso_2 PavingH = true := by {
  decide
}

def poly_111_iso_3 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,1), (2,2)]
theorem poly_111_iso_3_loser : defeated_by poly_111_iso_3 PavingH = true := by {
  decide
}

def poly_111_iso_4 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_111_iso_4_loser : defeated_by poly_111_iso_4 PavingH = true := by {
  decide
}

def poly_111_iso_5 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,1), (2,2), (3,1)]
theorem poly_111_iso_5_loser : defeated_by poly_111_iso_5 PavingH = true := by {
  decide
}

def poly_111_iso_6 : Polyomino := [(0,1), (1,1), (1,2), (2,1), (2,2), (3,0), (3,1)]
theorem poly_111_iso_6_loser : defeated_by poly_111_iso_6 PavingH = true := by {
  decide
}

def poly_111_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (3,1), (3,2)]
theorem poly_111_iso_7_loser : defeated_by poly_111_iso_7 PavingH = true := by {
  decide
}

def poly_112_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,3), (2,0)]
theorem poly_112_iso_0_loser : defeated_by poly_112_iso_0 PavingH = true := by {
  decide
}

def poly_112_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (2,0), (3,0), (3,1)]
theorem poly_112_iso_1_loser : defeated_by poly_112_iso_1 PavingH = true := by {
  decide
}

def poly_112_iso_2 : Polyomino := [(0,1), (0,2), (1,2), (2,2), (3,0), (3,1), (3,2)]
theorem poly_112_iso_2_loser : defeated_by poly_112_iso_2 PavingH = true := by {
  decide
}

def poly_112_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,2), (3,1), (3,2)]
theorem poly_112_iso_3_loser : defeated_by poly_112_iso_3 PavingH = true := by {
  decide
}

def poly_112_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,3), (2,3)]
theorem poly_112_iso_4_loser : defeated_by poly_112_iso_4 PavingH = true := by {
  decide
}

def poly_112_iso_5 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (3,0), (3,1), (3,2)]
theorem poly_112_iso_5_loser : defeated_by poly_112_iso_5 PavingH = true := by {
  decide
}

def poly_112_iso_6 : Polyomino := [(0,0), (1,0), (1,3), (2,0), (2,1), (2,2), (2,3)]
theorem poly_112_iso_6_loser : defeated_by poly_112_iso_6 PavingH = true := by {
  decide
}

def poly_112_iso_7 : Polyomino := [(0,3), (1,0), (1,3), (2,0), (2,1), (2,2), (2,3)]
theorem poly_112_iso_7_loser : defeated_by poly_112_iso_7 PavingH = true := by {
  decide
}

def poly_113_iso_0 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,0), (4,0), (5,0)]
theorem poly_113_iso_0_loser : defeated_by poly_113_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_113_iso_1 : Polyomino := [(0,1), (1,1), (2,1), (3,0), (3,1), (4,1), (5,1)]
theorem poly_113_iso_1_loser : defeated_by poly_113_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_113_iso_2 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5)]
theorem poly_113_iso_2_loser : defeated_by poly_113_iso_2 PavingCheckerboard = true := by {
  decide
}

def poly_113_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,3)]
theorem poly_113_iso_3_loser : defeated_by poly_113_iso_3 PavingCheckerboard = true := by {
  decide
}

def poly_113_iso_4 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (3,1), (4,0), (5,0)]
theorem poly_113_iso_4_loser : defeated_by poly_113_iso_4 PavingCheckerboard = true := by {
  decide
}

def poly_113_iso_5 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,1), (4,1), (5,1)]
theorem poly_113_iso_5_loser : defeated_by poly_113_iso_5 PavingCheckerboard = true := by {
  decide
}

def poly_113_iso_6 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5)]
theorem poly_113_iso_6_loser : defeated_by poly_113_iso_6 PavingCheckerboard = true := by {
  decide
}

def poly_113_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,2)]
theorem poly_113_iso_7_loser : defeated_by poly_113_iso_7 PavingCheckerboard = true := by {
  decide
}

def poly_114_iso_0 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (3,0), (3,1)]
theorem poly_114_iso_0_loser : defeated_by poly_114_iso_0 PavingH = true := by {
  decide
}

def poly_114_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,2), (2,3)]
theorem poly_114_iso_1_loser : defeated_by poly_114_iso_1 PavingH = true := by {
  decide
}

def poly_114_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_114_iso_2_loser : defeated_by poly_114_iso_2 PavingH = true := by {
  decide
}

def poly_114_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (3,1), (3,2)]
theorem poly_114_iso_3_loser : defeated_by poly_114_iso_3 PavingH = true := by {
  decide
}

def poly_114_iso_4 : Polyomino := [(0,1), (0,2), (1,1), (1,2), (2,0), (2,1), (3,1)]
theorem poly_114_iso_4_loser : defeated_by poly_114_iso_4 PavingH = true := by {
  decide
}

def poly_114_iso_5 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_114_iso_5_loser : defeated_by poly_114_iso_5 PavingH = true := by {
  decide
}

def poly_114_iso_6 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,1), (2,2), (3,1)]
theorem poly_114_iso_6_loser : defeated_by poly_114_iso_6 PavingH = true := by {
  decide
}

def poly_114_iso_7 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_114_iso_7_loser : defeated_by poly_114_iso_7 PavingH = true := by {
  decide
}

def poly_115_iso_0 : Polyomino := [(0,2), (1,2), (1,3), (2,0), (2,1), (2,2), (3,0)]
theorem poly_115_iso_0_loser : defeated_by poly_115_iso_0 PavingH = true := by {
  decide
}

def poly_115_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,2), (3,2), (3,3)]
theorem poly_115_iso_1_loser : defeated_by poly_115_iso_1 PavingH = true := by {
  decide
}

def poly_115_iso_2 : Polyomino := [(0,2), (1,1), (1,2), (1,3), (2,1), (3,0), (3,1)]
theorem poly_115_iso_2_loser : defeated_by poly_115_iso_2 PavingH = true := by {
  decide
}

def poly_115_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,2), (2,3), (3,2)]
theorem poly_115_iso_3_loser : defeated_by poly_115_iso_3 PavingH = true := by {
  decide
}

def poly_115_iso_4 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (2,3), (3,2)]
theorem poly_115_iso_4_loser : defeated_by poly_115_iso_4 PavingH = true := by {
  decide
}

def poly_115_iso_5 : Polyomino := [(0,3), (1,1), (1,2), (1,3), (2,0), (2,1), (3,1)]
theorem poly_115_iso_5_loser : defeated_by poly_115_iso_5 PavingH = true := by {
  decide
}

def poly_115_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (2,3), (3,3)]
theorem poly_115_iso_6_loser : defeated_by poly_115_iso_6 PavingH = true := by {
  decide
}

def poly_115_iso_7 : Polyomino := [(0,2), (0,3), (1,2), (2,0), (2,1), (2,2), (3,1)]
theorem poly_115_iso_7_loser : defeated_by poly_115_iso_7 PavingH = true := by {
  decide
}

def poly_116_iso_0 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (2,2), (3,0)]
theorem poly_116_iso_0_loser : defeated_by poly_116_iso_0 PavingH = true := by {
  decide
}

def poly_116_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,1), (2,2), (3,2)]
theorem poly_116_iso_1_loser : defeated_by poly_116_iso_1 PavingH = true := by {
  decide
}

def poly_116_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (3,0)]
theorem poly_116_iso_2_loser : defeated_by poly_116_iso_2 PavingH = true := by {
  decide
}

def poly_116_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (2,2), (2,3)]
theorem poly_116_iso_3_loser : defeated_by poly_116_iso_3 PavingH = true := by {
  decide
}

def poly_116_iso_4 : Polyomino := [(0,2), (0,3), (1,1), (1,2), (2,0), (2,1), (2,2)]
theorem poly_116_iso_4_loser : defeated_by poly_116_iso_4 PavingH = true := by {
  decide
}

def poly_116_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (2,2), (3,2)]
theorem poly_116_iso_5_loser : defeated_by poly_116_iso_5 PavingH = true := by {
  decide
}

def poly_116_iso_6 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,1), (2,2), (2,3)]
theorem poly_116_iso_6_loser : defeated_by poly_116_iso_6 PavingH = true := by {
  decide
}

def poly_116_iso_7 : Polyomino := [(0,1), (0,2), (0,3), (1,1), (1,2), (2,0), (2,1)]
theorem poly_116_iso_7_loser : defeated_by poly_116_iso_7 PavingH = true := by {
  decide
}

def poly_117_iso_0 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,1), (3,2), (4,1)]
theorem poly_117_iso_0_loser : defeated_by poly_117_iso_0 PavingH = true := by {
  decide
}

def poly_117_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (1,4), (2,2)]
theorem poly_117_iso_1_loser : defeated_by poly_117_iso_1 PavingH = true := by {
  decide
}

def poly_117_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (1,4), (2,3)]
theorem poly_117_iso_2_loser : defeated_by poly_117_iso_2 PavingH = true := by {
  decide
}

def poly_117_iso_3 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (1,4), (2,2)]
theorem poly_117_iso_3_loser : defeated_by poly_117_iso_3 PavingH = true := by {
  decide
}

def poly_117_iso_4 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (1,4), (2,1)]
theorem poly_117_iso_4_loser : defeated_by poly_117_iso_4 PavingH = true := by {
  decide
}

def poly_117_iso_5 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (3,1), (4,1)]
theorem poly_117_iso_5_loser : defeated_by poly_117_iso_5 PavingH = true := by {
  decide
}

def poly_117_iso_6 : Polyomino := [(0,1), (1,1), (2,1), (2,2), (3,0), (3,1), (4,1)]
theorem poly_117_iso_6_loser : defeated_by poly_117_iso_6 PavingH = true := by {
  decide
}

def poly_117_iso_7 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (3,1), (4,1)]
theorem poly_117_iso_7_loser : defeated_by poly_117_iso_7 PavingH = true := by {
  decide
}

def poly_118_iso_0 : Polyomino := [(0,1), (0,3), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_118_iso_0_loser : defeated_by poly_118_iso_0 PavingH = true := by {
  decide
}

def poly_118_iso_1 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_118_iso_1_loser : defeated_by poly_118_iso_1 PavingH = true := by {
  decide
}

def poly_118_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,0), (2,2)]
theorem poly_118_iso_2_loser : defeated_by poly_118_iso_2 PavingH = true := by {
  decide
}

def poly_118_iso_3 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,1), (2,3)]
theorem poly_118_iso_3_loser : defeated_by poly_118_iso_3 PavingH = true := by {
  decide
}

def poly_118_iso_4 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,0), (2,1), (3,1)]
theorem poly_118_iso_4_loser : defeated_by poly_118_iso_4 PavingH = true := by {
  decide
}

def poly_118_iso_5 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,1), (2,2), (3,1)]
theorem poly_118_iso_5_loser : defeated_by poly_118_iso_5 PavingH = true := by {
  decide
}

def poly_118_iso_6 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (3,1), (3,2)]
theorem poly_118_iso_6_loser : defeated_by poly_118_iso_6 PavingH = true := by {
  decide
}

def poly_118_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (2,2), (3,0), (3,1)]
theorem poly_118_iso_7_loser : defeated_by poly_118_iso_7 PavingH = true := by {
  decide
}

def poly_119_iso_0 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,1), (3,2), (4,2)]
theorem poly_119_iso_0_loser : defeated_by poly_119_iso_0 PavingH = true := by {
  decide
}

def poly_119_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (3,1), (4,1)]
theorem poly_119_iso_1_loser : defeated_by poly_119_iso_1 PavingH = true := by {
  decide
}

def poly_119_iso_2 : Polyomino := [(0,3), (0,4), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_119_iso_2_loser : defeated_by poly_119_iso_2 PavingH = true := by {
  decide
}

def poly_119_iso_3 : Polyomino := [(0,1), (1,1), (2,1), (2,2), (3,0), (3,1), (4,0)]
theorem poly_119_iso_3_loser : defeated_by poly_119_iso_3 PavingH = true := by {
  decide
}

def poly_119_iso_4 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,3), (2,4)]
theorem poly_119_iso_4_loser : defeated_by poly_119_iso_4 PavingH = true := by {
  decide
}

def poly_119_iso_5 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (3,1), (4,1)]
theorem poly_119_iso_5_loser : defeated_by poly_119_iso_5 PavingH = true := by {
  decide
}

def poly_119_iso_6 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (1,4), (2,2)]
theorem poly_119_iso_6_loser : defeated_by poly_119_iso_6 PavingH = true := by {
  decide
}

def poly_119_iso_7 : Polyomino := [(0,2), (1,1), (1,2), (1,3), (1,4), (2,0), (2,1)]
theorem poly_119_iso_7_loser : defeated_by poly_119_iso_7 PavingH = true := by {
  decide
}

def poly_120_iso_0 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (1,3)]
theorem poly_120_iso_0_loser : defeated_by poly_120_iso_0 PavingBrick = true := by {
  decide
}

def poly_120_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (1,3)]
theorem poly_120_iso_1_loser : defeated_by poly_120_iso_1 PavingBrick = true := by {
  decide
}

def poly_120_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,2)]
theorem poly_120_iso_2_loser : defeated_by poly_120_iso_2 PavingBrick = true := by {
  decide
}

def poly_120_iso_3 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1), (3,1)]
theorem poly_120_iso_3_loser : defeated_by poly_120_iso_3 PavingBrick = true := by {
  decide
}

def poly_120_iso_4 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (3,0), (3,1)]
theorem poly_120_iso_4_loser : defeated_by poly_120_iso_4 PavingBrick = true := by {
  decide
}

def poly_120_iso_5 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1), (3,0)]
theorem poly_120_iso_5_loser : defeated_by poly_120_iso_5 PavingBrick = true := by {
  decide
}

def poly_120_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,1), (1,2), (1,3)]
theorem poly_120_iso_6_loser : defeated_by poly_120_iso_6 PavingBrick = true := by {
  decide
}

def poly_120_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (3,0), (3,1)]
theorem poly_120_iso_7_loser : defeated_by poly_120_iso_7 PavingBrick = true := by {
  decide
}

def poly_121_iso_0 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (2,1), (2,2)]
theorem poly_121_iso_0_loser : defeated_by poly_121_iso_0 PavingH = true := by {
  decide
}

def poly_121_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (2,1), (2,2)]
theorem poly_121_iso_1_loser : defeated_by poly_121_iso_1 PavingH = true := by {
  decide
}

def poly_121_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,0), (2,1), (2,2)]
theorem poly_121_iso_2_loser : defeated_by poly_121_iso_2 PavingH = true := by {
  decide
}

def poly_121_iso_3 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,2)]
theorem poly_121_iso_3_loser : defeated_by poly_121_iso_3 PavingH = true := by {
  decide
}

def poly_121_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (2,0), (2,1)]
theorem poly_121_iso_4_loser : defeated_by poly_121_iso_4 PavingH = true := by {
  decide
}

def poly_121_iso_5 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,0), (2,1), (2,2)]
theorem poly_121_iso_5_loser : defeated_by poly_121_iso_5 PavingH = true := by {
  decide
}

def poly_121_iso_6 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (2,0), (2,2)]
theorem poly_121_iso_6_loser : defeated_by poly_121_iso_6 PavingH = true := by {
  decide
}

def poly_121_iso_7 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1)]
theorem poly_121_iso_7_loser : defeated_by poly_121_iso_7 PavingH = true := by {
  decide
}

def poly_122_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (3,0), (4,0)]
theorem poly_122_iso_0_loser : defeated_by poly_122_iso_0 PavingBrick = true := by {
  decide
}

def poly_122_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (1,3), (1,4)]
theorem poly_122_iso_1_loser : defeated_by poly_122_iso_1 PavingBrick = true := by {
  decide
}

def poly_122_iso_2 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,0), (3,1), (4,0)]
theorem poly_122_iso_2_loser : defeated_by poly_122_iso_2 PavingBrick = true := by {
  decide
}

def poly_122_iso_3 : Polyomino := [(0,2), (0,3), (0,4), (1,0), (1,1), (1,2), (1,3)]
theorem poly_122_iso_3_loser : defeated_by poly_122_iso_3 PavingBrick = true := by {
  decide
}

def poly_122_iso_4 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,0), (3,1), (4,1)]
theorem poly_122_iso_4_loser : defeated_by poly_122_iso_4 PavingBrick = true := by {
  decide
}

def poly_122_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,2), (1,3), (1,4)]
theorem poly_122_iso_5_loser : defeated_by poly_122_iso_5 PavingBrick = true := by {
  decide
}

def poly_122_iso_6 : Polyomino := [(0,1), (0,2), (0,3), (0,4), (1,0), (1,1), (1,2)]
theorem poly_122_iso_6_loser : defeated_by poly_122_iso_6 PavingBrick = true := by {
  decide
}

def poly_122_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (3,1), (4,1)]
theorem poly_122_iso_7_loser : defeated_by poly_122_iso_7 PavingBrick = true := by {
  decide
}

def poly_123_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,3), (3,3)]
theorem poly_123_iso_0_loser : defeated_by poly_123_iso_0 PavingH = true := by {
  decide
}

def poly_123_iso_1 : Polyomino := [(0,3), (1,2), (1,3), (2,2), (3,0), (3,1), (3,2)]
theorem poly_123_iso_1_loser : defeated_by poly_123_iso_1 PavingH = true := by {
  decide
}

def poly_123_iso_2 : Polyomino := [(0,3), (1,3), (2,1), (2,2), (2,3), (3,0), (3,1)]
theorem poly_123_iso_2_loser : defeated_by poly_123_iso_2 PavingH = true := by {
  decide
}

def poly_123_iso_3 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (3,2), (3,3)]
theorem poly_123_iso_3_loser : defeated_by poly_123_iso_3 PavingH = true := by {
  decide
}

def poly_123_iso_4 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (2,0), (3,0)]
theorem poly_123_iso_4_loser : defeated_by poly_123_iso_4 PavingH = true := by {
  decide
}

def poly_123_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (3,1), (3,2), (3,3)]
theorem poly_123_iso_5_loser : defeated_by poly_123_iso_5 PavingH = true := by {
  decide
}

def poly_123_iso_6 : Polyomino := [(0,1), (0,2), (0,3), (1,1), (2,0), (2,1), (3,0)]
theorem poly_123_iso_6_loser : defeated_by poly_123_iso_6 PavingH = true := by {
  decide
}

def poly_123_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,2), (2,3), (3,3)]
theorem poly_123_iso_7_loser : defeated_by poly_123_iso_7 PavingH = true := by {
  decide
}

def poly_124_iso_0 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (2,3), (3,1)]
theorem poly_124_iso_0_loser : defeated_by poly_124_iso_0 PavingH = true := by {
  decide
}

def poly_124_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,1), (3,1)]
theorem poly_124_iso_1_loser : defeated_by poly_124_iso_1 PavingH = true := by {
  decide
}

def poly_124_iso_2 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,2), (3,2)]
theorem poly_124_iso_2_loser : defeated_by poly_124_iso_2 PavingH = true := by {
  decide
}

def poly_124_iso_3 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (2,3), (3,2)]
theorem poly_124_iso_3_loser : defeated_by poly_124_iso_3 PavingH = true := by {
  decide
}

def poly_125_iso_0 : Polyomino := [(0,1), (1,1), (2,1), (3,1), (4,0), (4,1), (5,0)]
theorem poly_125_iso_0_loser : defeated_by poly_125_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_125_iso_1 : Polyomino := [(0,4), (0,5), (1,0), (1,1), (1,2), (1,3), (1,4)]
theorem poly_125_iso_1_loser : defeated_by poly_125_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_125_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (1,5)]
theorem poly_125_iso_2_loser : defeated_by poly_125_iso_2 PavingCheckerboard = true := by {
  decide
}

def poly_125_iso_3 : Polyomino := [(0,1), (0,2), (0,3), (0,4), (0,5), (1,0), (1,1)]
theorem poly_125_iso_3_loser : defeated_by poly_125_iso_3 PavingCheckerboard = true := by {
  decide
}

def poly_125_iso_4 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (3,0), (4,0), (5,0)]
theorem poly_125_iso_4_loser : defeated_by poly_125_iso_4 PavingCheckerboard = true := by {
  decide
}

def poly_125_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (3,1), (4,1), (5,1)]
theorem poly_125_iso_5_loser : defeated_by poly_125_iso_5 PavingCheckerboard = true := by {
  decide
}

def poly_125_iso_6 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (1,4), (1,5)]
theorem poly_125_iso_6_loser : defeated_by poly_125_iso_6 PavingCheckerboard = true := by {
  decide
}

def poly_125_iso_7 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (4,0), (4,1), (5,1)]
theorem poly_125_iso_7_loser : defeated_by poly_125_iso_7 PavingCheckerboard = true := by {
  decide
}

def poly_126_iso_0 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,2), (2,3)]
theorem poly_126_iso_0_loser : defeated_by poly_126_iso_0 PavingH = true := by {
  decide
}

def poly_126_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (2,1), (3,1)]
theorem poly_126_iso_1_loser : defeated_by poly_126_iso_1 PavingH = true := by {
  decide
}

def poly_126_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,0), (2,1)]
theorem poly_126_iso_2_loser : defeated_by poly_126_iso_2 PavingH = true := by {
  decide
}

def poly_126_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (2,1), (3,1)]
theorem poly_126_iso_3_loser : defeated_by poly_126_iso_3 PavingH = true := by {
  decide
}

def poly_126_iso_4 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (1,3), (2,3)]
theorem poly_126_iso_4_loser : defeated_by poly_126_iso_4 PavingH = true := by {
  decide
}

def poly_126_iso_5 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (1,3), (2,0)]
theorem poly_126_iso_5_loser : defeated_by poly_126_iso_5 PavingH = true := by {
  decide
}

def poly_126_iso_6 : Polyomino := [(0,1), (1,1), (2,1), (2,2), (3,0), (3,1), (3,2)]
theorem poly_126_iso_6_loser : defeated_by poly_126_iso_6 PavingH = true := by {
  decide
}

def poly_126_iso_7 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (3,0), (3,1), (3,2)]
theorem poly_126_iso_7_loser : defeated_by poly_126_iso_7 PavingH = true := by {
  decide
}

def poly_127_iso_0 : Polyomino := [(0,1), (0,2), (1,1), (2,0), (2,1), (2,2), (3,1)]
theorem poly_127_iso_0_loser : defeated_by poly_127_iso_0 PavingH = true := by {
  decide
}

def poly_127_iso_1 : Polyomino := [(0,0), (0,2), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_127_iso_1_loser : defeated_by poly_127_iso_1 PavingH = true := by {
  decide
}

def poly_127_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,1), (3,0), (3,1)]
theorem poly_127_iso_2_loser : defeated_by poly_127_iso_2 PavingH = true := by {
  decide
}

def poly_127_iso_3 : Polyomino := [(0,1), (0,3), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_127_iso_3_loser : defeated_by poly_127_iso_3 PavingH = true := by {
  decide
}

def poly_127_iso_4 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,0), (2,2)]
theorem poly_127_iso_4_loser : defeated_by poly_127_iso_4 PavingH = true := by {
  decide
}

def poly_127_iso_5 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,1), (2,3)]
theorem poly_127_iso_5_loser : defeated_by poly_127_iso_5 PavingH = true := by {
  decide
}

def poly_127_iso_6 : Polyomino := [(0,0), (0,1), (1,1), (2,0), (2,1), (2,2), (3,1)]
theorem poly_127_iso_6_loser : defeated_by poly_127_iso_6 PavingH = true := by {
  decide
}

def poly_127_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,1), (3,1), (3,2)]
theorem poly_127_iso_7_loser : defeated_by poly_127_iso_7 PavingH = true := by {
  decide
}

def poly_128_iso_0 : Polyomino := [(0,1), (1,0), (1,1), (2,1), (3,1), (4,1), (5,1)]
theorem poly_128_iso_0_loser : defeated_by poly_128_iso_0 PavingCheckerboard = true := by {
  decide
}

def poly_128_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,1)]
theorem poly_128_iso_1_loser : defeated_by poly_128_iso_1 PavingCheckerboard = true := by {
  decide
}

def poly_128_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5)]
theorem poly_128_iso_2_loser : defeated_by poly_128_iso_2 PavingCheckerboard = true := by {
  decide
}

def poly_128_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (3,0), (4,0), (5,0)]
theorem poly_128_iso_3_loser : defeated_by poly_128_iso_3 PavingCheckerboard = true := by {
  decide
}

def poly_128_iso_4 : Polyomino := [(0,4), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5)]
theorem poly_128_iso_4_loser : defeated_by poly_128_iso_4 PavingCheckerboard = true := by {
  decide
}

def poly_128_iso_5 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (4,0), (4,1), (5,0)]
theorem poly_128_iso_5_loser : defeated_by poly_128_iso_5 PavingCheckerboard = true := by {
  decide
}

def poly_128_iso_6 : Polyomino := [(0,1), (1,1), (2,1), (3,1), (4,0), (4,1), (5,1)]
theorem poly_128_iso_6_loser : defeated_by poly_128_iso_6 PavingCheckerboard = true := by {
  decide
}

def poly_128_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,4)]
theorem poly_128_iso_7_loser : defeated_by poly_128_iso_7 PavingCheckerboard = true := by {
  decide
}

def poly_129_iso_0 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (2,1), (2,2)]
theorem poly_129_iso_0_loser : defeated_by poly_129_iso_0 PavingH = true := by {
  decide
}

def poly_129_iso_1 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (2,0), (2,1)]
theorem poly_129_iso_1_loser : defeated_by poly_129_iso_1 PavingH = true := by {
  decide
}

def poly_129_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,1)]
theorem poly_129_iso_2_loser : defeated_by poly_129_iso_2 PavingH = true := by {
  decide
}

def poly_129_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
theorem poly_129_iso_3_loser : defeated_by poly_129_iso_3 PavingH = true := by {
  decide
}

def poly_130_iso_0 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,1), (3,2), (3,3)]
theorem poly_130_iso_0_loser : defeated_by poly_130_iso_0 PavingH = true := by {
  decide
}

def poly_130_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (2,3), (3,3)]
theorem poly_130_iso_1_loser : defeated_by poly_130_iso_1 PavingH = true := by {
  decide
}

def poly_130_iso_2 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (2,0), (3,0)]
theorem poly_130_iso_2_loser : defeated_by poly_130_iso_2 PavingH = true := by {
  decide
}

def poly_130_iso_3 : Polyomino := [(0,3), (1,3), (2,2), (2,3), (3,0), (3,1), (3,2)]
theorem poly_130_iso_3_loser : defeated_by poly_130_iso_3 PavingH = true := by {
  decide
}

def poly_131_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (3,1), (4,1), (4,2)]
theorem poly_131_iso_0_loser : defeated_by poly_131_iso_0 PavingH = true := by {
  decide
}

def poly_131_iso_1 : Polyomino := [(0,1), (0,2), (1,1), (2,1), (3,1), (4,0), (4,1)]
theorem poly_131_iso_1_loser : defeated_by poly_131_iso_1 PavingH = true := by {
  decide
}

def poly_131_iso_2 : Polyomino := [(0,4), (1,0), (1,1), (1,2), (1,3), (1,4), (2,0)]
theorem poly_131_iso_2_loser : defeated_by poly_131_iso_2 PavingH = true := by {
  decide
}

def poly_131_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (2,4)]
theorem poly_131_iso_3_loser : defeated_by poly_131_iso_3 PavingH = true := by {
  decide
}

def poly_132_iso_0 : Polyomino := [(0,1), (0,2), (0,3), (0,4), (1,0), (1,1), (2,0)]
theorem poly_132_iso_0_loser : defeated_by poly_132_iso_0 PavingH = true := by {
  decide
}

def poly_132_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,2), (3,2), (4,2)]
theorem poly_132_iso_1_loser : defeated_by poly_132_iso_1 PavingH = true := by {
  decide
}

def poly_132_iso_2 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (2,0), (3,0), (4,0)]
theorem poly_132_iso_2_loser : defeated_by poly_132_iso_2 PavingH = true := by {
  decide
}

def poly_132_iso_3 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (3,1), (4,1), (4,2)]
theorem poly_132_iso_3_loser : defeated_by poly_132_iso_3 PavingH = true := by {
  decide
}

def poly_132_iso_4 : Polyomino := [(0,4), (1,3), (1,4), (2,0), (2,1), (2,2), (2,3)]
theorem poly_132_iso_4_loser : defeated_by poly_132_iso_4 PavingH = true := by {
  decide
}

def poly_132_iso_5 : Polyomino := [(0,2), (1,2), (2,2), (3,1), (3,2), (4,0), (4,1)]
theorem poly_132_iso_5_loser : defeated_by poly_132_iso_5 PavingH = true := by {
  decide
}

def poly_132_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,3), (1,4), (2,4)]
theorem poly_132_iso_6_loser : defeated_by poly_132_iso_6 PavingH = true := by {
  decide
}

def poly_132_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (2,3), (2,4)]
theorem poly_132_iso_7_loser : defeated_by poly_132_iso_7 PavingH = true := by {
  decide
}

def poly_133_iso_0 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,1), (3,2), (4,2)]
theorem poly_133_iso_0_loser : defeated_by poly_133_iso_0 PavingH = true := by {
  decide
}

def poly_133_iso_1 : Polyomino := [(0,3), (0,4), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_133_iso_1_loser : defeated_by poly_133_iso_1 PavingH = true := by {
  decide
}

def poly_133_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (2,4)]
theorem poly_133_iso_2_loser : defeated_by poly_133_iso_2 PavingH = true := by {
  decide
}

def poly_133_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (2,3), (2,4)]
theorem poly_133_iso_3_loser : defeated_by poly_133_iso_3 PavingH = true := by {
  decide
}

def poly_133_iso_4 : Polyomino := [(0,2), (1,2), (2,1), (2,2), (3,0), (3,1), (4,0)]
theorem poly_133_iso_4_loser : defeated_by poly_133_iso_4 PavingH = true := by {
  decide
}

def poly_133_iso_5 : Polyomino := [(0,2), (0,3), (0,4), (1,1), (1,2), (2,0), (2,1)]
theorem poly_133_iso_5_loser : defeated_by poly_133_iso_5 PavingH = true := by {
  decide
}

def poly_133_iso_6 : Polyomino := [(0,2), (1,1), (1,2), (2,0), (2,1), (3,0), (4,0)]
theorem poly_133_iso_6_loser : defeated_by poly_133_iso_6 PavingH = true := by {
  decide
}

def poly_133_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (3,2), (4,2)]
theorem poly_133_iso_7_loser : defeated_by poly_133_iso_7 PavingH = true := by {
  decide
}

def poly_134_iso_0 : Polyomino := [(0,2), (1,2), (2,1), (2,2), (3,0), (3,1), (3,2)]
theorem poly_134_iso_0_loser : defeated_by poly_134_iso_0 PavingH = true := by {
  decide
}

def poly_134_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (2,0), (2,1), (2,2), (2,3)]
theorem poly_134_iso_1_loser : defeated_by poly_134_iso_1 PavingH = true := by {
  decide
}

def poly_134_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,1), (2,0), (3,0)]
theorem poly_134_iso_2_loser : defeated_by poly_134_iso_2 PavingH = true := by {
  decide
}

def poly_134_iso_3 : Polyomino := [(0,3), (1,2), (1,3), (2,0), (2,1), (2,2), (2,3)]
theorem poly_134_iso_3_loser : defeated_by poly_134_iso_3 PavingH = true := by {
  decide
}

def poly_134_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (2,2), (3,2)]
theorem poly_134_iso_4_loser : defeated_by poly_134_iso_4 PavingH = true := by {
  decide
}

def poly_134_iso_5 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (3,0), (3,1), (3,2)]
theorem poly_134_iso_5_loser : defeated_by poly_134_iso_5 PavingH = true := by {
  decide
}

def poly_134_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
theorem poly_134_iso_6_loser : defeated_by poly_134_iso_6 PavingH = true := by {
  decide
}

def poly_134_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (2,0)]
theorem poly_134_iso_7_loser : defeated_by poly_134_iso_7 PavingH = true := by {
  decide
}

def poly_135_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (2,0), (2,1), (2,2)]
theorem poly_135_iso_0_loser : defeated_by poly_135_iso_0 PavingH = true := by {
  decide
}

def poly_135_iso_1 : Polyomino := [(0,0), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]
theorem poly_135_iso_1_loser : defeated_by poly_135_iso_1 PavingH = true := by {
  decide
}

def poly_135_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (2,2)]
theorem poly_135_iso_2_loser : defeated_by poly_135_iso_2 PavingH = true := by {
  decide
}

def poly_135_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,2)]
theorem poly_135_iso_3_loser : defeated_by poly_135_iso_3 PavingH = true := by {
  decide
}

def poly_136_iso_0 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (2,1), (2,2), (2,3)]
theorem poly_136_iso_0_loser : defeated_by poly_136_iso_0 PavingH = true := by {
  decide
}

def poly_136_iso_1 : Polyomino := [(0,2), (1,2), (2,0), (2,2), (3,0), (3,1), (3,2)]
theorem poly_136_iso_1_loser : defeated_by poly_136_iso_1 PavingH = true := by {
  decide
}

def poly_136_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,3), (2,2), (2,3)]
theorem poly_136_iso_2_loser : defeated_by poly_136_iso_2 PavingH = true := by {
  decide
}

def poly_136_iso_3 : Polyomino := [(0,2), (0,3), (1,3), (2,0), (2,1), (2,2), (2,3)]
theorem poly_136_iso_3_loser : defeated_by poly_136_iso_3 PavingH = true := by {
  decide
}

def poly_136_iso_4 : Polyomino := [(0,0), (1,0), (2,0), (2,2), (3,0), (3,1), (3,2)]
theorem poly_136_iso_4_loser : defeated_by poly_136_iso_4 PavingH = true := by {
  decide
}

def poly_136_iso_5 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (2,0), (2,1)]
theorem poly_136_iso_5_loser : defeated_by poly_136_iso_5 PavingH = true := by {
  decide
}

def poly_136_iso_6 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (2,2), (3,2)]
theorem poly_136_iso_6_loser : defeated_by poly_136_iso_6 PavingH = true := by {
  decide
}

def poly_136_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (3,0)]
theorem poly_136_iso_7_loser : defeated_by poly_136_iso_7 PavingH = true := by {
  decide
}

def poly_137_iso_0 : Polyomino := [(0,1), (1,1), (1,2), (1,3), (2,1), (3,0), (3,1)]
theorem poly_137_iso_0_loser : defeated_by poly_137_iso_0 PavingH = true := by {
  decide
}

def poly_137_iso_1 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (2,3), (3,1)]
theorem poly_137_iso_1_loser : defeated_by poly_137_iso_1 PavingH = true := by {
  decide
}

def poly_137_iso_2 : Polyomino := [(0,2), (0,3), (1,2), (2,0), (2,1), (2,2), (3,2)]
theorem poly_137_iso_2_loser : defeated_by poly_137_iso_2 PavingH = true := by {
  decide
}

def poly_137_iso_3 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (2,3), (3,3)]
theorem poly_137_iso_3_loser : defeated_by poly_137_iso_3 PavingH = true := by {
  decide
}

def poly_137_iso_4 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,1), (3,1)]
theorem poly_137_iso_4_loser : defeated_by poly_137_iso_4 PavingH = true := by {
  decide
}

def poly_137_iso_5 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,2), (3,2), (3,3)]
theorem poly_137_iso_5_loser : defeated_by poly_137_iso_5 PavingH = true := by {
  decide
}

def poly_137_iso_6 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,2), (3,2)]
theorem poly_137_iso_6_loser : defeated_by poly_137_iso_6 PavingH = true := by {
  decide
}

def poly_137_iso_7 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (2,3), (3,0)]
theorem poly_137_iso_7_loser : defeated_by poly_137_iso_7 PavingH = true := by {
  decide
}

def poly_138_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (1,4), (2,0)]
theorem poly_138_iso_0_loser : defeated_by poly_138_iso_0 PavingH = true := by {
  decide
}

def poly_138_iso_1 : Polyomino := [(0,4), (1,0), (1,1), (1,2), (1,3), (1,4), (2,4)]
theorem poly_138_iso_1_loser : defeated_by poly_138_iso_1 PavingH = true := by {
  decide
}

def poly_138_iso_2 : Polyomino := [(0,1), (1,1), (2,1), (3,1), (4,0), (4,1), (4,2)]
theorem poly_138_iso_2_loser : defeated_by poly_138_iso_2 PavingH = true := by {
  decide
}

def poly_138_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,1), (3,1), (4,1)]
theorem poly_138_iso_3_loser : defeated_by poly_138_iso_3 PavingH = true := by {
  decide
}

def poly_139_iso_0 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (3,1), (4,1)]
theorem poly_139_iso_0_loser : defeated_by poly_139_iso_0 PavingH = true := by {
  decide
}

def poly_139_iso_1 : Polyomino := [(0,2), (0,3), (0,4), (1,0), (1,1), (1,2), (2,2)]
theorem poly_139_iso_1_loser : defeated_by poly_139_iso_1 PavingH = true := by {
  decide
}

def poly_139_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (1,2), (1,3), (1,4), (2,2)]
theorem poly_139_iso_2_loser : defeated_by poly_139_iso_2 PavingH = true := by {
  decide
}

def poly_139_iso_3 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,2), (2,3), (2,4)]
theorem poly_139_iso_3_loser : defeated_by poly_139_iso_3 PavingH = true := by {
  decide
}

def poly_139_iso_4 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (3,0), (4,0)]
theorem poly_139_iso_4_loser : defeated_by poly_139_iso_4 PavingH = true := by {
  decide
}

def poly_139_iso_5 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (3,1), (4,1)]
theorem poly_139_iso_5_loser : defeated_by poly_139_iso_5 PavingH = true := by {
  decide
}

def poly_139_iso_6 : Polyomino := [(0,2), (1,2), (1,3), (1,4), (2,0), (2,1), (2,2)]
theorem poly_139_iso_6_loser : defeated_by poly_139_iso_6 PavingH = true := by {
  decide
}

def poly_139_iso_7 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (3,2), (4,2)]
theorem poly_139_iso_7_loser : defeated_by poly_139_iso_7 PavingH = true := by {
  decide
}

def poly_140_iso_0 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (3,1), (3,2)]
theorem poly_140_iso_0_loser : defeated_by poly_140_iso_0 PavingH = true := by {
  decide
}

def poly_140_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,2), (1,3), (2,2)]
theorem poly_140_iso_1_loser : defeated_by poly_140_iso_1 PavingH = true := by {
  decide
}

def poly_140_iso_2 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (2,1)]
theorem poly_140_iso_2_loser : defeated_by poly_140_iso_2 PavingH = true := by {
  decide
}

def poly_140_iso_3 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (2,2), (2,3)]
theorem poly_140_iso_3_loser : defeated_by poly_140_iso_3 PavingH = true := by {
  decide
}

def poly_140_iso_4 : Polyomino := [(0,0), (0,1), (1,0), (1,1), (1,2), (2,0), (3,0)]
theorem poly_140_iso_4_loser : defeated_by poly_140_iso_4 PavingH = true := by {
  decide
}

def poly_140_iso_5 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (2,2), (3,2)]
theorem poly_140_iso_5_loser : defeated_by poly_140_iso_5 PavingH = true := by {
  decide
}

def poly_140_iso_6 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (3,0), (3,1)]
theorem poly_140_iso_6_loser : defeated_by poly_140_iso_6 PavingH = true := by {
  decide
}

def poly_140_iso_7 : Polyomino := [(0,2), (1,2), (1,3), (2,0), (2,1), (2,2), (2,3)]
theorem poly_140_iso_7_loser : defeated_by poly_140_iso_7 PavingH = true := by {
  decide
}

def poly_141_iso_0 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,0), (2,0), (3,0)]
theorem poly_141_iso_0_loser : defeated_by poly_141_iso_0 PavingH = true := by {
  decide
}

def poly_141_iso_1 : Polyomino := [(0,3), (1,3), (2,3), (3,0), (3,1), (3,2), (3,3)]
theorem poly_141_iso_1_loser : defeated_by poly_141_iso_1 PavingH = true := by {
  decide
}

def poly_141_iso_2 : Polyomino := [(0,0), (1,0), (2,0), (3,0), (3,1), (3,2), (3,3)]
theorem poly_141_iso_2_loser : defeated_by poly_141_iso_2 PavingH = true := by {
  decide
}

def poly_141_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3)]
theorem poly_141_iso_3_loser : defeated_by poly_141_iso_3 PavingH = true := by {
  decide
}

def poly_142_iso_0 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (1,3), (2,1), (3,1)]
theorem poly_142_iso_0_loser : defeated_by poly_142_iso_0 PavingH = true := by {
  decide
}

def poly_142_iso_1 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,1), (3,1)]
theorem poly_142_iso_1_loser : defeated_by poly_142_iso_1 PavingH = true := by {
  decide
}

def poly_142_iso_2 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (2,3), (3,3)]
theorem poly_142_iso_2_loser : defeated_by poly_142_iso_2 PavingH = true := by {
  decide
}

def poly_142_iso_3 : Polyomino := [(0,2), (0,3), (1,0), (1,1), (1,2), (2,2), (3,2)]
theorem poly_142_iso_3_loser : defeated_by poly_142_iso_3 PavingH = true := by {
  decide
}

def poly_142_iso_4 : Polyomino := [(0,1), (1,1), (2,0), (2,1), (2,2), (2,3), (3,0)]
theorem poly_142_iso_4_loser : defeated_by poly_142_iso_4 PavingH = true := by {
  decide
}

def poly_142_iso_5 : Polyomino := [(0,1), (1,1), (2,1), (2,2), (2,3), (3,0), (3,1)]
theorem poly_142_iso_5_loser : defeated_by poly_142_iso_5 PavingH = true := by {
  decide
}

def poly_142_iso_6 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,2), (3,2)]
theorem poly_142_iso_6_loser : defeated_by poly_142_iso_6 PavingH = true := by {
  decide
}

def poly_142_iso_7 : Polyomino := [(0,2), (1,2), (2,0), (2,1), (2,2), (3,2), (3,3)]
theorem poly_142_iso_7_loser : defeated_by poly_142_iso_7 PavingH = true := by {
  decide
}

def poly_143_iso_0 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (1,3), (2,1)]
theorem poly_143_iso_0_loser : defeated_by poly_143_iso_0 PavingH = true := by {
  decide
}

def poly_143_iso_1 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,0), (2,1), (3,1)]
theorem poly_143_iso_1_loser : defeated_by poly_143_iso_1 PavingH = true := by {
  decide
}

def poly_143_iso_2 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (2,2), (3,1)]
theorem poly_143_iso_2_loser : defeated_by poly_143_iso_2 PavingH = true := by {
  decide
}

def poly_143_iso_3 : Polyomino := [(0,1), (0,2), (1,0), (1,1), (1,2), (1,3), (2,2)]
theorem poly_143_iso_3_loser : defeated_by poly_143_iso_3 PavingH = true := by {
  decide
}

def poly_143_iso_4 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (1,3), (2,1), (2,2)]
theorem poly_143_iso_4_loser : defeated_by poly_143_iso_4 PavingH = true := by {
  decide
}

def poly_143_iso_5 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (2,2), (3,1)]
theorem poly_143_iso_5_loser : defeated_by poly_143_iso_5 PavingH = true := by {
  decide
}

def poly_143_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (2,1), (2,2), (3,1)]
theorem poly_143_iso_6_loser : defeated_by poly_143_iso_6 PavingH = true := by {
  decide
}

def poly_143_iso_7 : Polyomino := [(0,1), (1,0), (1,1), (1,2), (1,3), (2,1), (2,2)]
theorem poly_143_iso_7_loser : defeated_by poly_143_iso_7 PavingH = true := by {
  decide
}

def poly_144_iso_0 : Polyomino := [(0,1), (0,2), (1,2), (2,0), (2,1), (2,2), (3,0)]
theorem poly_144_iso_0_loser : defeated_by poly_144_iso_0 PavingH = true := by {
  decide
}

def poly_144_iso_1 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,0), (3,0), (3,1)]
theorem poly_144_iso_1_loser : defeated_by poly_144_iso_1 PavingH = true := by {
  decide
}

def poly_144_iso_2 : Polyomino := [(0,2), (0,3), (1,0), (1,2), (2,0), (2,1), (2,2)]
theorem poly_144_iso_2_loser : defeated_by poly_144_iso_2 PavingH = true := by {
  decide
}

def poly_144_iso_3 : Polyomino := [(0,1), (0,2), (0,3), (1,1), (1,3), (2,0), (2,1)]
theorem poly_144_iso_3_loser : defeated_by poly_144_iso_3 PavingH = true := by {
  decide
}

def poly_144_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (1,0), (1,2), (2,2), (2,3)]
theorem poly_144_iso_4_loser : defeated_by poly_144_iso_4 PavingH = true := by {
  decide
}

def poly_144_iso_5 : Polyomino := [(0,0), (0,1), (1,1), (1,3), (2,1), (2,2), (2,3)]
theorem poly_144_iso_5_loser : defeated_by poly_144_iso_5 PavingH = true := by {
  decide
}

def poly_144_iso_6 : Polyomino := [(0,0), (0,1), (1,0), (2,0), (2,1), (2,2), (3,2)]
theorem poly_144_iso_6_loser : defeated_by poly_144_iso_6 PavingH = true := by {
  decide
}

def poly_144_iso_7 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,2), (3,1), (3,2)]
theorem poly_144_iso_7_loser : defeated_by poly_144_iso_7 PavingH = true := by {
  decide
}

def poly_145_iso_0 : Polyomino := [(0,1), (1,1), (2,1), (3,0), (3,1), (3,2), (3,3)]
theorem poly_145_iso_0_loser : defeated_by poly_145_iso_0 PavingH = true := by {
  decide
}

def poly_145_iso_1 : Polyomino := [(0,3), (1,0), (1,1), (1,2), (1,3), (2,3), (3,3)]
theorem poly_145_iso_1_loser : defeated_by poly_145_iso_1 PavingH = true := by {
  decide
}

def poly_145_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (1,3), (2,0), (3,0)]
theorem poly_145_iso_2_loser : defeated_by poly_145_iso_2 PavingH = true := by {
  decide
}

def poly_145_iso_3 : Polyomino := [(0,2), (1,2), (2,2), (3,0), (3,1), (3,2), (3,3)]
theorem poly_145_iso_3_loser : defeated_by poly_145_iso_3 PavingH = true := by {
  decide
}

def poly_145_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,2), (2,2), (3,2)]
theorem poly_145_iso_4_loser : defeated_by poly_145_iso_4 PavingH = true := by {
  decide
}

def poly_145_iso_5 : Polyomino := [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (3,0)]
theorem poly_145_iso_5_loser : defeated_by poly_145_iso_5 PavingH = true := by {
  decide
}

def poly_145_iso_6 : Polyomino := [(0,3), (1,3), (2,0), (2,1), (2,2), (2,3), (3,3)]
theorem poly_145_iso_6_loser : defeated_by poly_145_iso_6 PavingH = true := by {
  decide
}

def poly_145_iso_7 : Polyomino := [(0,0), (0,1), (0,2), (0,3), (1,1), (2,1), (3,1)]
theorem poly_145_iso_7_loser : defeated_by poly_145_iso_7 PavingH = true := by {
  decide
}

def poly_146_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (2,1), (3,1)]
theorem poly_146_iso_0_loser : defeated_by poly_146_iso_0 PavingH = true := by {
  decide
}

def poly_146_iso_1 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,1), (2,2), (3,1)]
theorem poly_146_iso_1_loser : defeated_by poly_146_iso_1 PavingH = true := by {
  decide
}

def poly_146_iso_2 : Polyomino := [(0,1), (1,1), (1,2), (2,0), (2,1), (2,2), (3,2)]
theorem poly_146_iso_2_loser : defeated_by poly_146_iso_2 PavingH = true := by {
  decide
}

def poly_146_iso_3 : Polyomino := [(0,1), (1,1), (1,2), (1,3), (2,0), (2,1), (2,2)]
theorem poly_146_iso_3_loser : defeated_by poly_146_iso_3 PavingH = true := by {
  decide
}

def poly_146_iso_4 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (1,2), (1,3), (2,1)]
theorem poly_146_iso_4_loser : defeated_by poly_146_iso_4 PavingH = true := by {
  decide
}

def poly_146_iso_5 : Polyomino := [(0,2), (1,0), (1,1), (1,2), (2,1), (2,2), (2,3)]
theorem poly_146_iso_5_loser : defeated_by poly_146_iso_5 PavingH = true := by {
  decide
}

def poly_146_iso_6 : Polyomino := [(0,1), (1,0), (1,1), (2,0), (2,1), (2,2), (3,0)]
theorem poly_146_iso_6_loser : defeated_by poly_146_iso_6 PavingH = true := by {
  decide
}

def poly_146_iso_7 : Polyomino := [(0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (2,2)]
theorem poly_146_iso_7_loser : defeated_by poly_146_iso_7 PavingH = true := by {
  decide
}

def poly_147_iso_0 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,2), (2,3), (3,3)]
theorem poly_147_iso_0_loser : defeated_by poly_147_iso_0 PavingH = true := by {
  decide
}

def poly_147_iso_1 : Polyomino := [(0,3), (1,1), (1,2), (1,3), (2,0), (2,1), (3,0)]
theorem poly_147_iso_1_loser : defeated_by poly_147_iso_1 PavingH = true := by {
  decide
}

def poly_147_iso_2 : Polyomino := [(0,0), (0,1), (1,1), (1,2), (2,2), (3,2), (3,3)]
theorem poly_147_iso_2_loser : defeated_by poly_147_iso_2 PavingH = true := by {
  decide
}

def poly_147_iso_3 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (2,2), (2,3), (3,3)]
theorem poly_147_iso_3_loser : defeated_by poly_147_iso_3 PavingH = true := by {
  decide
}

def poly_147_iso_4 : Polyomino := [(0,3), (1,2), (1,3), (2,0), (2,1), (2,2), (3,0)]
theorem poly_147_iso_4_loser : defeated_by poly_147_iso_4 PavingH = true := by {
  decide
}

def poly_147_iso_5 : Polyomino := [(0,2), (0,3), (1,1), (1,2), (2,1), (3,0), (3,1)]
theorem poly_147_iso_5_loser : defeated_by poly_147_iso_5 PavingH = true := by {
  decide
}

def poly_147_iso_6 : Polyomino := [(0,2), (0,3), (1,2), (2,1), (2,2), (3,0), (3,1)]
theorem poly_147_iso_6_loser : defeated_by poly_147_iso_6 PavingH = true := by {
  decide
}

def poly_147_iso_7 : Polyomino := [(0,0), (0,1), (1,1), (2,1), (2,2), (3,2), (3,3)]
theorem poly_147_iso_7_loser : defeated_by poly_147_iso_7 PavingH = true := by {
  decide
}

def poly_148_iso_0 : Polyomino := [(0,3), (1,1), (1,2), (1,3), (2,0), (2,1), (2,3)]
theorem poly_148_iso_0_loser : defeated_by poly_148_iso_0 PavingH = true := by {
  decide
}

def poly_148_iso_1 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,1), (2,2), (3,2)]
theorem poly_148_iso_1_loser : defeated_by poly_148_iso_1 PavingH = true := by {
  decide
}

def poly_148_iso_2 : Polyomino := [(0,0), (1,0), (1,1), (2,1), (3,0), (3,1), (3,2)]
theorem poly_148_iso_2_loser : defeated_by poly_148_iso_2 PavingH = true := by {
  decide
}

def poly_148_iso_3 : Polyomino := [(0,0), (0,1), (0,2), (1,1), (2,0), (2,1), (3,0)]
theorem poly_148_iso_3_loser : defeated_by poly_148_iso_3 PavingH = true := by {
  decide
}

def poly_148_iso_4 : Polyomino := [(0,2), (1,1), (1,2), (2,1), (3,0), (3,1), (3,2)]
theorem poly_148_iso_4_loser : defeated_by poly_148_iso_4 PavingH = true := by {
  decide
}

def poly_148_iso_5 : Polyomino := [(0,0), (1,0), (1,1), (1,2), (2,0), (2,2), (2,3)]
theorem poly_148_iso_5_loser : defeated_by poly_148_iso_5 PavingH = true := by {
  decide
}

def poly_148_iso_6 : Polyomino := [(0,0), (0,1), (0,3), (1,1), (1,2), (1,3), (2,3)]
theorem poly_148_iso_6_loser : defeated_by poly_148_iso_6 PavingH = true := by {
  decide
}

def poly_148_iso_7 : Polyomino := [(0,0), (0,2), (0,3), (1,0), (1,1), (1,2), (2,0)]
theorem poly_148_iso_7_loser : defeated_by poly_148_iso_7 PavingH = true := by {
  decide
}

