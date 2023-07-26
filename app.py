import time
import random
import pandas as pd
import numpy as np

from solver import solve_sudoku, SIZE


def main():
    # df = pd.read_csv("./data/sudoku.csv")
    # choices = df.values.tolist()

    # for sudoku, answer in choices:
    #     # Convert them into an numpy array
    #     npsudoku = np.array([*sudoku], dtype=np.int8).reshape(SIZE, SIZE)
    #     npanswer = np.array([*answer], dtype=np.int8).reshape(SIZE, SIZE)

    #     if not valid_solution(npanswer, solve_sudoku(npsudoku)):
    #         raise RuntimeError("Invalid solution")

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
    print("Solution: ")
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
    df = pd.read_csv("./data/sudoku.csv")
    choice = random.choice(df.values.tolist())
    sudoku = [*choice[0]]
    answer = [*choice[1]]

    # Convert them into an numpy array
    npsudoku = np.array(sudoku, dtype=np.int8).reshape(SIZE, SIZE)
    npanswer = np.array(answer, dtype=np.int8).reshape(SIZE, SIZE)

    # Return the sudoku and the answer
    return npsudoku, npanswer


def valid_solution(answer, solution):
    return np.array_equal(answer, solution)


if __name__ == "__main__":
    main()
