from typing import Callable
from csp import CSP


def assign_singles(csp: CSP, init_domain: Callable[[], set]):
    # For assigning hidden singles
    for vars, _ in csp.constraints:
        unique_values = init_domain()
        for var in vars:
            # Assign hidden single
            domain = csp.domains[var]
            if domain:
                unique_values = unique_values.difference(domain)

                no_uvalues = len(unique_values)
                if no_uvalues == 0:
                    break
                if no_uvalues == 1:
                    value = unique_values.pop()
                    csp.domains[var] = set()
                    csp.assignments[var] = value
                    break
