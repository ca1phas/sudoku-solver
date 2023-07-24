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
    start_time = time.time()
    solution = solve_sudoku(sudoku)
    end_time = time.time()

    # Check the solution
    if valid_solution(answer, solution):
        time_taken = end_time - start_time

        print(solution)
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


def solve_sudoku(sudoku):
    ...


def valid_solution(answer, solution):
    ...


if __name__ == "__main__":
    main()
