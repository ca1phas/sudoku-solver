from typing import TypeVar, Callable

from csp import CSP, Variable

T = TypeVar("T")
Arc = tuple[T, T]
Arcs = set[Arc]
ArcFunc = Callable[[T, set[T]], bool]


def ac3(csp: CSP, arcs: Arcs, arc_func: ArcFunc):
    while arcs:
        x, y = arcs.pop()

        if _revise(csp, x, y, arc_func):
            if len(csp.domains) == 0:
                return False
            for k in csp.get_neighbours(x) - {y}:
                arcs.add((k, x))

    return True


def _revise(csp: CSP, x: Variable, y: Variable, arc_func: ArcFunc):
    revised = False
    for xvalue in csp.domains[x].copy():
        yvalues = {csp.assignments[y]} if csp.assignments != None else csp.domains[y]
        if not arc_func(xvalue, yvalues):
            csp.remove_domain_value(x, xvalue)
            revised = True
    return revised
