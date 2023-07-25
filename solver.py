import time
import random
import pandas as pd
import numpy as np


def main():
    # Get a sudoku
    print("Getting the sudoku...")
    sudoku, answer = get_sudoku()
    print("Sudoku: ")
    print(sudoku)

    # Solve the sudoku
    print("Solving sudoku")
    start_time = time.time()
    solution = solve_sudoku(sudoku)
    end_time = time.time()

    # Check the solution
    print(solution)
    if valid_solution(answer, solution):
        print("Correct solution")
    else:
        print("Incorrect solution")

    # Display statistics
    time_taken = end_time - start_time
    print(f"Time take to solve: {time_taken}s")


def get_sudoku():
    # Get a random sudoku and its answer
    df = pd.read_csv("sudoku.csv")
    choice = random.choice(df.values.tolist())
    sudoku = [*choice[0]]
    answer = [*choice[1]]

    # Convert them into an numpy array
    npsudoku = np.array(sudoku, np.int8).reshape(9, 9)
    npanswer = np.array(answer, np.int8).reshape(9, 9)

    # Return the sudoku and the answer
    return npsudoku, npanswer


def get_domains(sudoku):
    """
    Return domain as dict

    key = tuple(row, col), value = set of available values
    """
    domains: dict[tuple[int, int], set[int]] = {}
    values = set(range(1, 10))

    for row in range(9):
        for col in range(9):
            init_value = sudoku[row, col]

            if init_value:
                domains[row, col] = values - {init_value}
            else:
                domains[row, col] = values

    return domains


def get_constraints():
    ...


def all_diff(vars, values):
    # If no. vars == no. unique values, all different
    return len(vars) == len(set(values))


def solve_sudoku(sudoku):
    # Get domains and constraints
    domains = get_domains(sudoku)
    constraints = get_constraints()

    print(domains)

    solution = None

    return solution


def valid_solution(answer, solution):
    return np.array_equal(answer, solution)


if __name__ == "__main__":
    main()
