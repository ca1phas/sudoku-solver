from math import sqrt
from copy import deepcopy
from random import choice
from typing import Callable, Optional

from pprint import pprint

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


def ac3(csp: Csp, arcs: Arcs | None = None):
    vars, domains, constraints = csp

    # Initialize all the arcs in csp if arcs is given
    if not arcs:
        arcs = get_arcs(csp)

    while arcs:
        x, y = arcs.pop()

        if revise(csp, x, y):
            # If domain of x is empty after revision,
            # Return False as there is no solution
            if not domains[x]:
                return False
            # If domain of x is not empty after revision
            # Re/check all arcs with x bar except (x, k) & (y, x)
            for constraint in constraints:
                vars = constraint[0]
                if x in vars:
                    for k in vars:
                        if k != x and k != y:
                            arcs.add((k, x))

    # Return True as arc consistency is maintained
    return True


def get_arcs(csp: Csp, x: Optional[Variable] = None, y: Optional[Variable] = None):
    """
    Return all arcs given all constraints and

    arc = (a, b) where a and b are `Variable`

    `is_x` = if `True` and `x` is provided, include arcs where a is `x` only

    `is_y` = if `True` and `y` is provided, include arcs wehre b is `y` only

    `is_xy` = if `True` and `x` and `y` are proived,
    return arcs with the single arc (`x`, `y`) if `x` and `y` in the constraint
    """

    vars, _, constraints = csp

    arcs: Arcs = set()
    for constraint in constraints:
        cvars = constraint[0]
        if x or y:
            if x in cvars or y in cvars:
                arcs.update(constraint_to_arcs(constraint, x=x, y=y))
        else:
            # If no variable is provided, get all arcs
            for cvar in cvars:
                # If cvar does not have a value
                if not vars[cvar]:
                    arcs.update(constraint_to_arcs(constraint, x=cvar))

    return arcs


def constraint_to_arcs(
    constraint: Constraint,
    x: Optional[Variable] = None,
    y: Optional[Variable] = None,
    is_x: Optional[bool] = True,
    is_y: Optional[bool] = True,
    is_xy: Optional[bool] = True,
):
    """
    Return all arcs given a constraint

    arc = (a, b) where a and b are `Variable`

    `is_x` = if `True` and `x` is provided, include arcs where a is `x` only

    `is_y` = if `True` and `y` is provided, include arcs wehre b is `y` only

    `is_xy` = if `True` and `x` and `y` are proived,
    return arcs with the single arc (`x`, `y`) if `x` and `y` in the constraint
    """

    arcs: Arcs = set()
    cvars = constraint[0]

    only_want_xy = x and y and is_xy
    if only_want_xy:
        if x in cvars and y in cvars:
            arcs.add((x, y))
        return arcs

    only_want_x = x and is_x
    only_want_y = y and is_y
    for i, cx in enumerate(cvars):
        if only_want_x and cx != x:
            continue

        for cy in cvars[i + 1 :]:
            if only_want_y and cy != y:
                continue

            arcs.add((cx, cy))

    return arcs


def revise(csp: Csp, x: Variable, y: Variable):
    domains = csp[1]

    revised = False
    for xvalue in domains[x].copy():
        if not satisfy_arc_constraint(csp, xvalue, y):
            domains[x].remove(xvalue)
            revised = True
    return revised


def satisfy_arc_constraint(csp: Csp, xvalue: int, y: Variable):
    """
    Return `True` if there is a domain value of `y`
    that can satisfy the constraints if `x` is `xvalue`
    arc = (`x`, `y`)

    Constraints:
    1. If `y` has a value, it does not equal to `xvalue`
    2. Else, `y` has a domain value(s) that does not equal to `xvalue`
    """

    vars, domains, _ = csp

    yvalue = vars[y]

    if not yvalue or yvalue != xvalue:
        for yvalue in domains[y]:
            if yvalue != xvalue:
                break
        return True

    return False


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
                for ivar in inferences:
                    assignment[ivar] = inferences[ivar]
                result = backtrack(csp, assignment)
                if result:
                    return result
                for ivar in inferences:
                    assignment.pop(ivar)
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


def inference(csp: Csp, var: Variable, assignment: Variables) -> Variables | None:
    variables, domains, constriants = csp

    # Update domains and variables
    new_domains: Domains = deepcopy(domains)
    new_vars: Variables = deepcopy(variables)
    for var in assignment:
        new_domains[var] = set()
        new_vars[var] = assignment[var]

    new_csp: Csp = (new_vars, new_domains, constriants)
    ac3(new_csp, get_arcs(new_csp, y=var))


def all_diff(vars: list[Variable], values: list[int]):
    return len(vars) == len(tuple(values))
