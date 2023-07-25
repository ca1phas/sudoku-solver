import math
from typing import Callable

# Size must be a square number
SIZE = 9

Square = tuple[int, int]
Domains = dict[Square, set[int]]
Constrain = tuple[list[Square], Callable[[tuple[Square, ...], list[int]], bool]]
Csp = tuple[Domains, list[Constrain]]
Arc = tuple[Square, Square]


def solve_sudoku(sudoku):
    # Get constraint satisfaction problem
    csp = (get_domains(sudoku), get_constraints())

    # Maintain arc consistency
    # result = ac3(csp)

    # Backtracking
    solution = None

    return solution


def get_domains(sudoku):
    """
    Return domains

    domains -> dict[key: tuple(row, col), value: set of available values]
    """

    domains: Domains = {}

    values = set(range(1, SIZE + 1))
    for row in range(SIZE):
        for col in range(SIZE):
            # Initialize domain values
            init_value = sudoku[row, col]
            if init_value:
                domains[row, col] = values - {init_value}
            else:
                domains[row, col] = values

    return domains


def get_constraints():
    constraints: list[Constrain] = []

    # Row constraints
    for row in range(SIZE):
        squares = [(row, col) for col in range(SIZE)]
        constraints.append((squares, all_diff))

    # Column constraints
    for col in range(SIZE):
        squares = [(row, col) for row in range(SIZE)]
        constraints.append((squares, all_diff))

    # Square constraints
    subgrid_size = int(math.sqrt(SIZE))
    if subgrid_size**2 != SIZE:
        raise RuntimeError("SIZE of sudoku must be a square number")

    for subgrid_row in range(subgrid_size):
        # Get row indexes
        row_start = subgrid_row * subgrid_size
        row_end = row_start + subgrid_size

        for subgrid_col in range(subgrid_size):
            # Get column indexes
            col_start = subgrid_col * subgrid_size
            col_end = col_start + subgrid_size

            # Get squares indexes
            squares: list[tuple[int, int]] = []
            for row in range(row_start, row_end):
                for col in range(col_start, col_end):
                    squares.append((row, col))

            constraints.append((squares, all_diff))

    return constraints


def constrain_to_arcs(constrain: Constrain):
    arcs: list[Arc] = []
    sqrs = constrain[0]

    for i, sqrx in enumerate(sqrs):
        for sqry in sqrs[i + 1 :]:
            arcs.append((sqrx, sqry))

    return arcs


def all_diff(vars: tuple[Square, ...], values: list[int]):
    # If no. vars == no. unique values, all different
    return len(vars) == len(set(values))
