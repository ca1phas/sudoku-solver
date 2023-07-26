from typing import Optional
from solver import Csp, Variable, Arcs, Constraint


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
                cvars = constraint[0]
                if x in cvars:
                    for k in cvars:
                        if k != x and k != y:
                            arcs.add((k, x))

    # Return True as arc consistency is maintained
    return True


def get_arcs(csp: Csp, x: Optional[Variable] = None, y: Optional[Variable] = None):
    """
    Return all arcs given the `csp`, `x` and `y`

    arc = (a, b) where a and b are `Variable`

    if `x` is provided, return arcs where a is `x` only

    if `y` is provided, return arcs wehre b is `y` only

    if `x` and `y` are proived, return arcs with (`x`, `y`) only
    """

    constraints = csp[2]

    arcs: Arcs = set()
    for constraint in constraints:
        if x or y:
            cvars = constraint[0]
            if x in cvars or y in cvars:
                arcs.update(constraint_to_arcs(constraint, x=x, y=y))
        else:
            arcs.update(constraint_to_arcs(constraint))

    return arcs


def constraint_to_arcs(
    constraint: Constraint,
    x: Optional[Variable] = None,
    y: Optional[Variable] = None,
):
    """
    Return all arcs given a constraint

    arc = (a, b) where a and b are `Variable`

    if `x` is provided, return arcs where a is `x` only

    if `y` is provided, return arcs wehre b is `y` only

    if `x` and `y` are proived, return arcs with (`x`, `y`) only
    """

    arcs: Arcs = set()
    cvars = constraint[0]

    if x and y:
        if x in cvars and y in cvars:
            arcs.add((x, y))
        return arcs

    for i, cx in enumerate(cvars):
        if x and cx != x:
            continue

        for cy in cvars[i + 1 :]:
            if y and cy != y:
                continue

            arcs.add((cx, cy))
            arcs.add((cy, cx))

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
