import time
import random
import numpy as np
import pandas as pd
from math import sqrt

from csp import CSP, Domains, Assignments, Constraints, Domain
from ac3 import Arcs, ac3

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
    # Setup CSP Solver for the sudoku
    csp = get_sudoku_csp(sudoku)

    # Maintain arc consistency
    ac3(
        csp=csp,
        arcs=get_suduko_arcs(csp),
        arc_func=satisfy_arc_constraint,
    )

    # Return solution by backtracking search


def get_sudoku_csp(sudoku):
    def all_diff(assignment: dict):
        return len(assignment.keys()) == len(set(assignment.values()))

    vars = set()
    constraints: Constraints = set()
    domains: Domains = {}
    assignments: Assignments = {}

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
            domains[var] = set() if sudoku[var] else {(i + 1) for i in range(SIZE)}

            # Add column constraint
            if row == 0:
                cvars = {(r, col) for r in size_range}
                constraints.add((frozenset(cvars), all_diff))

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
        vars=vars,
        domains=domains,
        assignments=assignments,
        constraints=constraints,
    )


def get_suduko_arcs(csp: CSP):
    arcs: Arcs = set()
    for vars, _ in csp.constraints:
        for var in vars:
            for var2 in vars:
                if var != var2:
                    arcs.add((var, var2))
    return arcs


def satisfy_arc_constraint(xvalue: int, yvalues: Domain):
    """
    Return `True` if there are two unique values i.e.
    `x` and `y` have different values
    """
    for yvalue in yvalues:
        if yvalue != xvalue:
            return True
    return False


def valid_solution(answer, solution):
    return np.array_equal(answer, solution)


if __name__ == "__main__":
    main()
