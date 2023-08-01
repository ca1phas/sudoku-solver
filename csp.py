from typing import TypeVar, Callable

T = TypeVar("T")

Domain = set[T]
Variables = frozenset[T]
Domains = dict[T, Domain]
Relation = Callable[[list[T], list[T]], bool] | set[tuple[T, ...]]
Constraint = tuple[Variables, Relation]
Constraints = set[Constraint]


class CSP:
    def __init__(
        self,
        vars: Variables,
        domains: Domains,
        constraints: Constraints,
    ) -> None:
        self._vars = vars
        self._domains = domains
        self._constraints = constraints

    @property
    def vars(self):
        return self._vars

    @property
    def domains(self):
        return self._domains

    @property
    def constraints(self):
        return self._constraints
