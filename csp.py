from typing import Callable

Variable = tuple[int, int]
Variables = dict[Variable, int]
Domains = dict[Variable, set[int]]
Relation = Callable[[list[Variable], list[int]], bool]
Constraint = tuple[tuple[Variable], Relation]
Constraints = list[Constraint]
Csp = tuple[Variables, Domains, Constraints]
Arc = tuple[Variable, Variable]
Arcs = set[Arc]
