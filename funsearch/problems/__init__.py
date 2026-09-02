"""Problem specifications and evaluation suites for FunSearch."""

from funsearch.problems import cap_set
from funsearch.problems import bin_packing
from funsearch.problems import admissible_set
from funsearch.problems import snakey
from funsearch.problems import snakey_breaker
from funsearch.problems import straightomino

PROBLEMS = {
    "cap_set": cap_set,
    "bin_packing": bin_packing,
    "admissible_set": admissible_set,
    "snakey": snakey,
    "snakey_breaker": snakey_breaker,
    "straightomino": straightomino,
    "i5": straightomino,
}

__all__ = ["PROBLEMS", "cap_set", "bin_packing", "admissible_set", "snakey", "straightomino"]
