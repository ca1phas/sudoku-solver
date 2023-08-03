import time
import random
import numpy as np
import pandas as pd
from math import sqrt
from statistics import mean

from csp import CSP, Domains, Assignments, Constraints, Domain, Variables
from ac3 import ac3, Arcs
from backtrack import backtracking_search

# from inferences import assign_singles


SIZE = 9


def main():
    df = pd.read_csv("./data/sudoku.csv")
    choices = df.values.tolist()

    print("Solving...")
    all_time_taken = []
    for i in range(10000):
        sudoku, answer = choices[i]

        # Convert them into an numpy array
        npsudoku = np.array([*sudoku], dtype=np.int8).reshape(SIZE, SIZE)
        npanswer = np.array([*answer], dtype=np.int8).reshape(SIZE, SIZE)

        start_time = time.time()
        solution = solve_sudoku(npsudoku)
        end_time = time.time()
        all_time_taken.append(end_time - start_time)

        if not valid_solution(npanswer, solution):
            raise RuntimeError("Invalid solution")
    print(f"Average time taken: {mean(all_time_taken)*1000}ms")


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

    # Get solution by inferences
    if inference(csp):
        return assignments_to_solution(csp.assignments)

    # Get solution by backtracking search
    assignments = {}
    if not csp.complete_assignment():
        assignments = backtracking_search(csp)
        if assignments == None:
            return sudoku
    return assignments_to_solution(csp.assignments, assignments)


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
            domains[var] = set() if sudoku[var] else init_domain()

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
        arc_func=satisfy_arc_constraint,
        lcv_hfunc=get_sudoku_cv,
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


def get_sudoku_cv(dvalue: int, neighbours: Variables, domains: Domains):
    """
    Return the constraining value of the `dvalue` based on `ndomains`

    `dvalue` = domain value
    `ndomains` = neighbour domains
    """
    count = 0
    for nvar in neighbours:
        if dvalue in domains[nvar]:
            count += 1
    return count


def valid_solution(answer, solution):
    return np.array_equal(answer, solution)


def init_domain():
    return {(i + 1) for i in range(SIZE)}


def inference(csp: CSP):
    """
    Complete assignment by inferences
    """

    # Maintain arc consistency
    ac3(csp, get_suduko_arcs(csp))
    if csp.complete_assignment():
        return True

    # Assign all variables with hidden single
    # assign_singles(csp, init_domain)
    # if csp.complete_assignment():
    #     return True

    return False


def assignments_to_solution(
    assignments: Assignments, new_assignments: Assignments = {}
):
    solution = []
    for row in range(SIZE):
        rvalues = []
        for col in range(SIZE):
            var = row, col
            if not new_assignments:
                rvalues.append(assignments[var])
            else:
                rvalues.append(
                    new_assignments[var] if var in new_assignments else assignments[var]
                )
        solution.append(rvalues)
    return solution


if __name__ == "__main__":
    main()
