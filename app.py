import time
import random
import pandas as pd
import numpy as np

from solver import solve_sudoku, SIZE


def main():
    # Get a sudoku
    # print("Getting the sudoku...")
    # sudoku, answer = get_sudoku()
    # print("Sudoku: ")
    # print(sudoku)
    sudoku = [
        [0, 0, 0, 0, 3, 6, 9, 4, 5],
        [0, 0, 0, 7, 9, 1, 6, 8, 2],
        [0, 0, 0, 5, 4, 8, 1, 7, 3],
        [2, 6, 5, 8, 1, 7, 3, 9, 4],
        [3, 7, 8, 4, 2, 9, 5, 1, 6],
        [9, 1, 4, 3, 6, 5, 8, 2, 7],
        [4, 5, 1, 9, 7, 3, 2, 6, 8],
        [8, 2, 9, 6, 5, 4, 7, 3, 1],
        [7, 3, 6, 1, 8, 2, 4, 5, 9],
    ]
    answer = [
        [1, 8, 7, 2, 3, 6, 9, 4, 5],
        [5, 4, 3, 7, 9, 1, 6, 8, 2],
        [6, 9, 2, 5, 4, 8, 1, 7, 3],
        [2, 6, 5, 8, 1, 7, 3, 9, 4],
        [3, 7, 8, 4, 2, 9, 5, 1, 6],
        [9, 1, 4, 3, 6, 5, 8, 2, 7],
        [4, 5, 1, 9, 7, 3, 2, 6, 8],
        [8, 2, 9, 6, 5, 4, 7, 3, 1],
        [7, 3, 6, 1, 8, 2, 4, 5, 9],
    ]

    # Solve the sudoku
    print("Solving sudoku")
    start_time = time.time()
    solution = solve_sudoku(np.array(sudoku))
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
    npsudoku = np.array(sudoku).reshape(SIZE, SIZE)
    npanswer = np.array(answer).reshape(SIZE, SIZE)

    # Return the sudoku and the answer
    return npsudoku, npanswer


def valid_solution(answer, solution):
    return np.array_equal(answer, solution)


if __name__ == "__main__":
    main()
