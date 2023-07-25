import numpy as np
from math import sqrt
from typing import Callable, Any


# Size must be a square number
SIZE = 9

Variable = tuple[int, int]
Variables = dict[Variable, int]
Domains = dict[Variable, set[int]]
Constraint = tuple[list[Variable], Callable[[list[Variable], list[int]], bool]]
Constraints = list[Constraint]
Csp = tuple[Variables, Domains, Constraints]


def solve_sudoku(sudoku):
    # Initialize csp
    csp = get_sudoku_csp(sudoku)

    # Maintain arc consistency

    # Backtracking

    # Return solution
    return


def get_sudoku_csp(sudoku) -> Csp:
    variables: Variables = {}
    domains: Domains = {}
    constraints: Constraints = []

    dvalues = set(range(1, SIZE + 1))

    # Initialize variables, domains and constraints(row + column)
    for row in range(SIZE):
        row_vars = []

        for col in range(SIZE):
            init = sudoku[row, col]

            # Initialize variables
            variables[row, col] = init

            # Initialize domains
            domains[row, col] = set() if init else dvalues

            # Get row variable
            row_vars.append((row, col))

            # Get column constraint if it is the first row
            if not row:
                constraints.append(([(r, col) for r in range(SIZE)], all_diff))

        # Add row constraint
        constraints.append((row_vars, all_diff))

    # Initialize constraints(square)
    square_size = int(sqrt(SIZE))
    if square_size**2 != SIZE:
        raise RuntimeError("SIZE of sudoku must be a square number")
    for srow in range(square_size):
        start_row = srow * square_size
        end_row = start_row + square_size

        for scol in range(square_size):
            start_col = scol * square_size
            end_col = start_col + square_size

            square_vars = [
                (r, c)
                for r in range(start_row, end_row)
                for c in range(start_col, end_col)
            ]

            constraints.append((square_vars, all_diff))

    # Return csp
    return variables, domains, constraints


def all_diff(vars: list[Variable], values: list[int]):
    return len(vars) == len(tuple(values))
