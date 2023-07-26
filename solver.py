from math import sqrt
from copy import deepcopy
from random import choice
from typing import Callable

# Size must be a square number
SIZE = 9

Variable = tuple[int, int]
Variables = dict[Variable, int]
Domains = dict[Variable, set[int]]
Constraint = tuple[list[Variable], Callable[[list[Variable], list[int]], bool]]
Constraints = list[Constraint]
Csp = tuple[Variables, Domains, Constraints]
Arc = tuple[Variable, Variable]
Arcs = set[Arc]

from mac import ac3, get_arcs


def solve_sudoku(sudoku):
    # Initialize csp
    csp = get_sudoku_csp(sudoku)

    # Maintain arc consistency
    if not ac3(csp):
        return

    # Backtracking
    assignment = backtracking_search(csp)

    # Return solution
    return assignment


def get_sudoku_csp(sudoku) -> Csp:
    vars: Variables = {}
    domains: Domains = {}
    constraints: Constraints = []

    dvalues = set(range(1, SIZE + 1))

    # Initialize variables, domains and constraints(row + column)
    for row in range(SIZE):
        row_vars = []

        for col in range(SIZE):
            init = sudoku[row, col]

            # Initialize variables
            vars[row, col] = init

            # Initialize domains
            domains[row, col] = set() if init else dvalues.copy()

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
    return vars, domains, constraints


def backtracking_search(csp: Csp):
    return backtrack(csp, {})


def backtrack(csp: Csp, assignment: Variables) -> Variables | None:
    complete_assignment = len(assignment) == len(csp[0])
    if complete_assignment:
        return assignment

    var = select_unassigned_variable(csp, assignment)

    for value in order_domain_values(csp, var, assignment):
        if consistent_assignment(csp, assignment, var, value):
            assignment[var] = value
            inferences = inference(csp, var, assignment)
            if inferences:
                # for ivar in inferences:
                #     assignment[ivar] = inferences[ivar]
                result = backtrack(csp, assignment)
                if result:
                    return result
                # for ivar in inferences:
                #     assignment.pop(ivar)
            assignment.pop(var)

    return None


def select_unassigned_variable(csp: Csp, assignment: Variables) -> Variable:
    # Get list of unassigned variable(s)
    domains = csp[1]
    uvars = get_unassigned_variables(csp, assignment)
    if len(uvars) == 1:
        return uvars.pop()

    # Get MRV(Minimum remaining values) variable(s)
    mrv = SIZE
    mrv_vars = []
    for var in uvars:
        # Get remainining value
        rv = len(domains[var])
        if rv < mrv:
            mrv = rv
            mrv_vars = [var]
        elif rv == mrv:
            mrv_vars.append(var)
    if len(mrv_vars) == 1:
        return mrv_vars[0]

    # Get MDV(Maximum degree values) variable(s)
    mdv = 0
    mdv_vars = []
    for var in mrv_vars:
        # Get degree value
        neighbours = get_neighbours(csp, var)
        dv = len(neighbours.intersection(uvars)) - 1  # -1 for var itself
        if dv > mdv:
            mdv = dv
            mdv_vars = [var]
        elif dv == mdv:
            mdv_vars.append(var)
    if len(mdv_vars) == 1:
        return mdv_vars[0]

    return choice(mdv_vars)


def order_domain_values(csp: Csp, var: Variable, assignment: Variables) -> list[int]:
    domains = csp[1]
    cvalues: list[tuple[int, int]] = []  # tuple[dvalue, cvalue]

    for dvalue in domains[var]:
        # Get unassigned neighbours
        uvars = get_unassigned_variables(csp, assignment)
        neighbours = get_neighbours(csp, var)
        uneighbours = neighbours.intersection(uvars)

        # Get constraining value
        cvalue = 0
        for uneighour in uneighbours:
            if dvalue in domains[uneighour]:
                cvalue += 1

        cvalues.append((dvalue, cvalue))

    svalues = [dvalue for dvalue, _ in sorted(cvalues, key=lambda cvalue: cvalue[1])]
    return svalues


def get_unassigned_variables(csp: Csp, assignment: Variables):
    vars = csp[0]
    return [var for var in vars if vars[var] == 0 and var not in assignment]


def get_neighbours(csp: Csp, var: Variable):
    neighbours: set[Variable] = set()
    for cvars, _ in csp[2]:
        if var in cvars:
            neighbours = neighbours.union(set(cvars))
    neighbours.discard(var)

    return neighbours


def consistent_assignment(
    csp: Csp, assignment: Variables, var: Variable, value: int
) -> bool:
    vars, _, constraints = csp

    # Ensure `value` of the `var` satisfies all constraints
    for constraint in constraints:
        if var in constraint:
            # Get the list of variables in a constraint
            cvars = constraint[0]

            # Get list of values of the variables
            values = [value]
            for cvar in cvars:
                cvar_value = vars[cvar]
                if cvar_value:
                    values.append(cvar_value)
                elif cvar in assignment:
                    values.append(assignment[cvar])

            # Ensure `value` of the `var` satisfies the constraint function
            cfunc = constraint[1]
            if not cfunc(cvars, values):
                return False

    return True


def inference(csp: Csp, var: Variable, assignment: Variables):
    vars, domains, constriants = csp

    # Update csp after value assignment
    # new_domains: Domains = deepcopy(domains)
    # new_vars: Variables = deepcopy(variables)
    for var in assignment:
        domains[var] = set()
        vars[var] = assignment[var]
    # new_csp: Csp = (new_vars, new_domains, constriants)

    # Maintain arc consistency after value assignment
    return ac3(csp, get_arcs(csp, y=var))


def all_diff(vars: list[Variable], values: list[int]):
    return len(vars) == len(tuple(values))
