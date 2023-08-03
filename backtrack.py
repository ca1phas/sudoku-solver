from copy import deepcopy
from random import choice
from csp import CSP, Assignments, Variable
from ac3 import ac3, Arcs


def backtracking_search(csp: CSP):
    return _backtrack(csp, {})


def _backtrack(csp: CSP, assignments: Assignments):
    if csp.complete_assignment(assignments):
        return assignments

    var = _select_unassigned_variable(csp, assignments)

    for value in _order_domain_values(csp, var, assignments):
        if csp.consistent_assignment(
            new_assignments={**assignments, var: value},
            svar=var,
        ):
            assignments[var] = value

            # Maintain Arc Consistency
            # new_csp = _mac(csp, var, assignments)
            # if new_csp != None:
            #     old_csp = csp
            #     csp = new_csp
            #     result = _backtrack(csp, assignments)
            #     if result != None:
            #         return result
            #     csp = old_csp

            result = _backtrack(csp, assignments)
            if result != None:
                return result
            assignments.pop(var)
    return None


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
    if not csp.lcv_hfunc:
        raise RuntimeError("Cannot order domain values without csp.lcv_hfunc")

    dvalues = {}
    uneighbours = _get_unassigned_variables(csp, assignments).union(
        csp.get_neighbours(var)
    )
    for dvalue in csp.domains[var]:
        dvalues[dvalue] = csp.lcv_hfunc(dvalue, uneighbours, csp.domains)
    return sorted(dvalues.keys(), key=lambda k: dvalues[k])


def _mac(csp: CSP, var: Variable, assignments: Assignments):
    """
    Maintain arc consistency

    Return the new domains of unassigned variables if there are new inferences

    Return `None` if there is no new inference
    """

    uvars = _get_unassigned_variables(csp, assignments)
    uneighbours = uvars.intersection(csp.get_neighbours(var))
    arcs: Arcs = {(n, var) for n in uneighbours}

    new_domains = {**csp.domains}
    for uvar in uvars:
        new_domains[uvar] = deepcopy(csp.domains[uvar])
    new_csp = CSP(
        vars=csp.vars,
        arc_func=csp.arc_func,
        lcv_hfunc=csp.lcv_hfunc,
        constraints=csp.constraints,
        domains=new_domains,
        assignments={
            **csp.assignments,
            **assignments,
        },
    )

    if not ac3(new_csp, arcs):
        return None
    return new_csp
