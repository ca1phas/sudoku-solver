import time
import pandas as pd
from suduko_solver import SudokuSolver, Board


SIZE = 9


def main():
    board = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
    ]
    print("Solving...")
    start = time.time()
    solver = SudokuSolver(board)
    solver.solve()
    print(f"Time taken: {time.time() - start}")

    # df = pd.read_csv("./data/sudoku.csv")
    # choices = df.values.tolist()

    # print("Solving...")
    # start = time.time()
    # for i in range(1000):
    #     sudoku_str, answer_str = choices[i]

    #     # Convert sudoku into an array
    #     sudoku = []
    #     answer = []
    #     for row in range(SIZE):
    #         sudoku_rvalues = []
    #         answer_rvalues = []
    #         for col in range(SIZE):
    #             index = row * SIZE + col
    #             sudoku_rvalues.append(int(sudoku_str[index]))
    #             answer_rvalues.append(int(answer_str[index]))
    #         sudoku.append(sudoku_rvalues)
    #         answer.append(answer_rvalues)

    #     solution = SudokuSolver(sudoku).solve()
    #     if not solution or not valid_solution(answer, solution):
    #         raise RuntimeError("Invalid solution")
    # print(f"Time taken: {time.time() - start}")


def valid_solution(answer: Board, solution: Board):
    for row in range(SIZE):
        for col in range(SIZE):
            if solution[row][col] != answer[row][col]:
                return False
    return True


if __name__ == "__main__":
    main()
