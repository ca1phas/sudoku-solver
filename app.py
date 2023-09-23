import time
import pandas as pd
from pprint import pprint
from suduko_solver import SudokuSolver, Board


SIZE = 9
SAMPLE_SIZE = 1000


def main():
    solve_world_hardest()
    solve_sudokus(SAMPLE_SIZE)


def solve_world_hardest():
    # World Hardest Sudoku
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
    print("The World Hardest Sudoku:")
    pprint(board)
    print("Solving the world hardest sudoku...")
    start = time.time()
    solver = SudokuSolver(board)
    solution = solver.solve()
    time_taken = "{0:0.4f}".format(time.time() - start)
    print("Solution:")
    pprint(solution)
    print(f"Time taken: {time_taken}s")


def solve_sudokus(sample_size):
    print(f"Fetching {sample_size} sudokus...")
    df = pd.read_csv("./data/sudoku.csv")
    choices = df.values.tolist()

    print(f"Solving {sample_size} sudokus...")
    start = time.time()
    for i in range(sample_size):
        sudoku_str, answer_str = choices[i]

        # Convert sudoku into an array
        sudoku = []
        answer = []
        for row in range(SIZE):
            sudoku_rvalues = []
            answer_rvalues = []
            for col in range(SIZE):
                index = row * SIZE + col
                sudoku_rvalues.append(int(sudoku_str[index]))
                answer_rvalues.append(int(answer_str[index]))
            sudoku.append(sudoku_rvalues)
            answer.append(answer_rvalues)

        solution = SudokuSolver(sudoku).solve()
        if not solution or not valid_solution(answer, solution):
            raise RuntimeError("Invalid solution")
    time_taken = "{0:0.4f}".format(time.time() - start)
    print(f"Time taken for 1000 sudokus: {time_taken}s")
    print(f"Average time taken per sudoku: {float(time_taken) / sample_size}s")


def valid_solution(answer: Board, solution: Board):
    for row in range(SIZE):
        for col in range(SIZE):
            if solution[row][col] != answer[row][col]:
                return False
    return True


if __name__ == "__main__":
    main()
