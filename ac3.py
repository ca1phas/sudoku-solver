from typing import TypeVar

from csp import CSP, Variable

T = TypeVar("T")
Arc = tuple[T, T]
Arcs = set[Arc]


def ac3(csp: CSP, arcs: Arcs):
    while arcs:
        x, y = arcs.pop()

        if _revise(csp, x, y):
            if len(csp.domains) == 0:
                return False
            for k in csp.get_neighbours(x) - {y}:
                arcs.add((k, x))

    return True


def _revise(csp: CSP, x: Variable, y: Variable):
    if not csp.arc_func:
        raise RuntimeError("Please provide an arc_func to revise arcs")

    revised = False
    for xvalue in csp.domains[x].copy():
        yvalues = {csp.assignments[y]} if csp.assignments != None else csp.domains[y]
        if not csp.arc_func(xvalue, yvalues):
            csp.remove_domain_values(x, {xvalue})
            revised = True
    return revised
