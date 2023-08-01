import time
import random
import numpy as np
import pandas as pd
from math import sqrt

from csp import CSP, Variables, Domains, Constraints

SIZE = 9


def main():
    # df = pd.read_csv("./data/sudoku.csv")
    # choices = df.values.tolist()

    # for sudoku, answer in choices:
    #     # Convert them into an numpy array
    #     npsudoku = np.array([*sudoku], dtype=np.int8).reshape(SIZE, SIZE)
    #     npanswer = np.array([*answer], dtype=np.int8).reshape(SIZE, SIZE)

    #     if not valid_solution(npanswer, solve_sudoku(npsudoku)):
    #         raise RuntimeError("Invalid solution")

    # Get a sudoku
    print("Getting the sudoku...")
    sudoku, answer = get_sudoku()
    print("Sudoku: ")
    print(sudoku)

    # Solve the sudoku
    print("Solving sudoku")
    start_time = time.time()
    solution = solve_sudoku(sudoku)
    end_time = time.time()

    # Check the solution
    print("Solution: ")
    print(solution)
    if valid_solution(answer, solution):
        print("Correct solution")
    else:
        print("Incorrect solution")

    # Display statistics
    time_taken = end_time - start_time
    print(f"Time take to solve: {time_taken}s")


def get_sudoku():
    # Get a random sudoku and its answer
    df = pd.read_csv("./data/sudoku.csv")
    choice = random.choice(df.values.tolist())
    sudoku = [*choice[0]]
    answer = [*choice[1]]

    # Convert them into an numpy array
    sudoku = np.array(sudoku, dtype=np.int8).reshape(SIZE, SIZE)
    answer = np.array(answer, dtype=np.int8).reshape(SIZE, SIZE)

    # Return the sudoku and the answer
    return sudoku, answer


def solve_sudoku(sudoku):
    # Setup CSP for the sudoku
    csp = get_sudoku_csp(sudoku)

    # Maintain arc consistency
    csp

    # Return solution by backtracking search


def get_sudoku_csp(sudoku):
    def all_diff(vars: list[tuple[int, int]], values: list[int]):
        return len(vars) == len(set(values))

    vars = set()
    assignments = {}
    domains: Domains = {}
    constraints: Constraints = set()

    size_range = range(SIZE)
    for row in size_range:
        rvars = set()

        for col in size_range:
            var = (row, col)

            # Add row variable
            rvars.add(var)

            # Add variable
            vars.add(var)

            # Set assignment
            assignments[var] = sudoku[var] or None

            # Set domain
            domains[var] = set() if sudoku[var] else {i for i in range(SIZE)}

            # Add column constraint
            if row == 0:
                cvars = frozenset((r, col) for r in size_range)
                constraints.add((cvars, all_diff))

        # Add row constraint
        constraints.add((frozenset(rvars), all_diff))

    # Add square constraints
    subgrid = int(sqrt(SIZE))
    if subgrid**2 != SIZE:
        raise RuntimeError("SIZE must be a square number")
    subgrid_range = range(subgrid)
    for srow in subgrid_range:
        row_start = srow * subgrid
        row_end = srow * subgrid + subgrid

        for scol in subgrid_range:
            col_start = scol * subgrid
            col_end = scol * subgrid + subgrid

            svars = set()
            for row in range(row_start, row_end):
                for col in range(col_start, col_end):
                    svars.add((row, col))
            constraints.add((frozenset(svars), all_diff))

    return CSP(
        vars=frozenset(vars),
        domains=domains,
        constraints=constraints,
    )


def valid_solution(answer, solution):
    return np.array_equal(answer, solution)


if __name__ == "__main__":
    main()
