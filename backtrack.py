from random import choice
from csp import CSP, Assignments, Variable, Domains


def backtracking_search(csp: CSP):
    return _backtrack(csp, {})


def _backtrack(csp: CSP, assignments: Assignments):
    if csp.complete_assignment(assignments):
        return assignments

    var = _select_unassigned_variable(csp, assignments)

    for value in _order_domain_values(csp, var, assignments):
        if csp.consistent_assignment(new_assignments={**assignments, var: value}):
            assignments[var] = value
            inferences = _inference(csp, var, assignments)
            if inferences != None:
                _add_inferences(csp, inferences)
                result = _backtrack(csp, assignments)
                if result != None:
                    return result
                _remove_inferences(csp, inferences)

            assignments.pop(var)


def _select_unassigned_variable(csp: CSP, assignments: Assignments):
    uvars = _get_unassigned_variables(csp, assignments)

    # Get the Minimum-Remaining-Values unassigned variables
    mrv = 10**10
    mrv_vars = set()
    for uvar in uvars:
        no_values = len(csp.domains[uvar])
        if no_values < mrv:
            mrv = no_values
            mrv_vars = {uvar}
        elif no_values == mrv:
            mrv_vars.add(uvar)
    if len(mrv_vars) == 1:
        return mrv_vars.pop()

    # Get the Maximum-Degree unassigned variables
    md = 0
    md_vars = set()
    for mrv_var in mrv_vars:
        neighbours = csp.get_neighbours(mrv_var)
        no_degree = len(neighbours - uvars)

        if no_degree > md:
            md = no_degree
            md_vars = {mrv_var}
        elif no_degree == md:
            md_vars.add(mrv_var)
    if len(md_vars) == 1:
        return md_vars.pop()

    return choice(list(md_vars))


def _get_unassigned_variables(csp: CSP, assignments: Assignments):
    uvars = set()
    for var in csp.vars:
        if csp.assignments[var] == None and var not in assignments:
            uvars.add(var)
    return uvars


def _order_domain_values(csp: CSP, var: Variable, assignments: Assignments):
    uvars = _get_unassigned_variables(csp, assignments)
    uneighbours = uvars.union(csp.get_neighbours(var))
    dvalues = csp.domains[var]

    return dvalues


def _inference(csp: CSP, var: Variable, assignments: Assignments) -> dict:
    ...


def _add_inferences(csp: CSP, inferences: Domains):
    """
    Return previous domains of changed variables after adding inferences to the csp
    """
    ...


def _remove_inferences(csp: CSP, inferences: Domains):
    ...
