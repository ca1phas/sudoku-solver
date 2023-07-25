SIZE = 9


def solve_sudoku(sudoku):
    # Get domains
    domains = get_domains(sudoku)

    solution = None

    return solution


def get_domains(sudoku):
    """
    Return domain as dict

    key = tuple(row, col), value = set of available values
    """
    domains: dict[tuple[int, int], set[int]] = {}
    values = set(range(1, SIZE + 1))

    for row in range(SIZE):
        for col in range(SIZE):
            init_value = sudoku[row, col]

            if init_value:
                domains[row, col] = values - {init_value}
            else:
                domains[row, col] = values

    return domains


def all_diff(vars, values):
    # If no. vars == no. unique values, all different
    return len(vars) == len(set(values))
