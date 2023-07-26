from math import sqrt
from copy import deepcopy
from random import choice


# Size must be a square number
SIZE = 9

from csp import Variable, Variables, Domains, Constraints, Csp
from mac import ac3, get_arcs


def solve_sudoku(sudoku):
    # Initialize csp
    csp = get_sudoku_csp(sudoku)

    # Maintain arc consistency
    if not ac3(csp):
        return

    # Backtracking
    assignment = backtracking_search(csp)

    # Ensure there is a solution
    if not assignment:
        raise RuntimeError("Cannot solve sudoku")

    # Return solution
    solution = deepcopy(sudoku)
    for var in assignment:
        row, col = var
        solution[row][col] = assignment[var]
    return solution


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
                constraints.append(
                    (tuple([(r, col) for r in range(SIZE)]), sudoku_cfunc)
                )

        # Add row constraint
        constraints.append((tuple(row_vars), sudoku_cfunc))

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

            constraints.append((tuple(square_vars), sudoku_cfunc))

    # Return csp
    return vars, domains, constraints


def sudoku_cfunc(vars: list[Variable], values: list[int]):
    """
    Sudoku constrain function

    Ensure all `values` of `vars` are unique
    """
    return len(vars) == len(set(values))


def backtracking_search(csp: Csp):
    return backtrack(csp, {})


def backtrack(csp: Csp, assignment: Variables) -> Variables | None:
    uvar = select_unassigned_variable(csp, assignment)

    # Assignment complete if there is no unassigned variable
    if not uvar:
        return assignment

    for value in order_domain_values(csp, uvar, assignment):
        if consistent_assignment(csp, assignment, uvar, value):
            assignment[uvar] = value

            result = backtrack(csp, assignment)
            if result:
                return result

            assignment.pop(uvar)

    return None


def select_unassigned_variable(csp: Csp, assignment: Variables) -> Variable | None:
    # Get list of unassigned variable(s)
    domains = csp[1]
    uvars = get_unassigned_variables(csp, assignment)
    if not len(uvars):
        return
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
        dv = len(neighbours.intersection(uvars))
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
        cvars = constraint[0]
        if var in cvars:
            # Get list of assigned variables and their values
            avars = [var]
            avalues = [value]
            for cvar in cvars:
                cvar_value = vars[cvar]
                if cvar_value:
                    avalues.append(cvar_value)
                    avars.append(cvar)
                elif cvar in assignment:
                    avalues.append(assignment[cvar])
                    avars.append(cvar)

            # Ensure `value` of the `var` satisfies the constraint function
            cfunc = constraint[1]
            if not cfunc(avars, avalues):
                return False

    return True


def inference(csp: Csp, var: Variable, assignment: Variables):
    vars, domains, _ = csp

    # Update csp after value assignment
    # new_domains: Domains = deepcopy(domains)
    # new_vars: Variables = deepcopy(variables)
    for var in assignment:
        domains[var] = set()
        vars[var] = assignment[var]
    # new_csp: Csp = (new_vars, new_domains, constriants)

    # Maintain arc consistency after value assignment
    return ac3(csp, get_arcs(csp, y=var))
