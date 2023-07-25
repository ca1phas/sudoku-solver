import time
import random
import pandas as pd
import numpy as np

from solver import solve_sudoku, SIZE


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
    npsudoku = np.array(sudoku, np.int8).reshape(SIZE, SIZE)
    npanswer = np.array(answer, np.int8).reshape(SIZE, SIZE)

    # Return the sudoku and the answer
    return npsudoku, npanswer


def valid_solution(answer, solution):
    return np.array_equal(answer, solution)


if __name__ == "__main__":
    main()
