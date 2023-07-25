import math
from typing import Callable


# Size must be a square number
SIZE = 9

Square = tuple[int, int]
Domains = dict[Square, set[int]]
Constrain = tuple[tuple[Square], Callable[[tuple[Square, ...], list[int]], bool]]
Csp = tuple[tuple[Square], Domains, tuple[Constrain]]
Arc = tuple[Square, Square]


def solve_sudoku(sudoku):
    ...
