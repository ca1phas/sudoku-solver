from typing import TypeAlias, TypeVar, Callable

T = TypeVar("T")

Domain = set[T]
Variable: TypeAlias = T
Variables = set[Variable]
Assignments = dict[Variable, T]
Domains = dict[Variable, Domain]
Relation = Callable[[Assignments], bool]
Constraint = tuple[frozenset[Variable], Relation]
Constraints = set[Constraint]


class CSP:
    def __init__(
        self,
        vars: Variables,
        domains: Domains,
        constraints: Constraints,
        assignments: Assignments = {},
    ):
        self._vars = vars
        self._domains = domains
        self._constraints = constraints
        self._assignments = assignments

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

    def remove_domain_value(self, var, value):
        if var in self.domains:
            self._domains[var].remove(value)

    def consistent_assignment(self, new_assignments: Assignments = {}):
        for vars, rel in self.constraints:
            values = {}
            for var in vars:
                if var in new_assignments:
                    values[var] = new_assignments[var]
                elif self.assignments[var] != None:
                    values[var] = self.assignments[var]
            if not rel(values):
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
