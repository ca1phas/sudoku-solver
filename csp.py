from typing import TypeAlias, TypeVar, Callable, Optional

T = TypeVar("T")

Domain = set[T]
Variable: TypeAlias = T
Variables = set[Variable]
Assignments = dict[Variable, T]
Domains = dict[Variable, Domain]
Relation = Callable[[Assignments], bool]
Constraint = tuple[frozenset[Variable], Relation]
Constraints = set[Constraint]

ArcFunc = Callable[[T, set[T]], bool]


class CSP:
    def __init__(
        self,
        vars: Variables,
        domains: Domains,
        constraints: Constraints,
        assignments: Assignments = {},
        arc_func: Optional[ArcFunc] = None,
    ):
        self._vars = vars
        self._domains = domains
        self._constraints = constraints
        self._assignments = assignments
        self._arc_func = arc_func

    @property
    def vars(self):
        return self._vars

    @property
    def domains(self):
        return self._domains

    @property
    def constraints(self):
        return self._constraints

    @property
    def assignments(self):
        return self._assignments

    @property
    def arc_func(self):
        return self._arc_func

    def add_domain_values(self, var, values: set):
        if var in self.domains:
            self._domains[var].union(values)

    def remove_domain_values(self, var, values: set):
        if var in self.domains:
            self._domains[var].difference(values)

    def consistent_assignment(self, new_assignments: Assignments = {}):
        for vars, rel in self.constraints:
            assignments = {}
            for var in vars:
                if var in new_assignments:
                    assignments[var] = new_assignments[var]
                elif self.assignments[var] != None:
                    assignments[var] = self.assignments[var]
            if not rel(assignments):
                return False
        return True

    def complete_assignment(self, new_assignments: Assignments = {}):
        for var in self._vars:
            if self.assignments[var] != None:
                continue
            if var in new_assignments and new_assignments[var] != None:
                continue
            return False
        return True

    def get_neighbours(self, var: Variable):
        neighbours = set()
        for vars, _ in self.constraints:
            if var in vars:
                neighbours = neighbours.union(vars)
        neighbours.discard(var)
        return neighbours
