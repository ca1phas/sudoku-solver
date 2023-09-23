from math import sqrt
from enum import Enum
from typing import List, Tuple

Board = List[List[int]]
Cell = Tuple[int, int]


class _SudokuErrorCode(Enum):
    INVALID_FORMAT = 1
    INVALID_LENGTH = 2
    INVALID_DIGIT = 3
    INVALID_BOARD = 4


class _Sudoku:
    _size = 9
    _empty_cell_value = 0
    _bsize = int(sqrt(_size))  # box size
    _range_size = range(_size)
    _range_bsize = range(_bsize)
    _valid_digits = {i for i in range(_size + 1)}

    def __init__(self, board: Board):
        self._board = board
        valid, code = self._validate()
        if not valid and code:
            self._handle_error(code)

    def _validate(self):
        """
        Validate the board

        Return (`True`, `None`) if the board is a valid

        Otherwise, return (`False`, `error_code`)
        """
        # Ensure board is of correct format, correct size and correct digits
        if not isinstance(self._board, List):
            return False, _SudokuErrorCode.INVALID_FORMAT
        if len(self._board) != self._size:
            return False, _SudokuErrorCode.INVALID_LENGTH
        for row in self._board:
            if not isinstance(row, List):
                return False, _SudokuErrorCode.INVALID_FORMAT

            if len(row) != self._size:
                return False, _SudokuErrorCode.INVALID_LENGTH

            for cell in row:
                if not isinstance(cell, int):
                    return False, _SudokuErrorCode.INVALID_FORMAT

                if cell not in self._valid_digits:
                    return False, _SudokuErrorCode.INVALID_DIGIT

        # Ensure board is consistent
        if not self._consistent():
            return False, _SudokuErrorCode.INVALID_BOARD

        return True, None

    def _consistent(self):
        """
        Return `True` if all rules of sudoku is satisfied

        Otherwise, return `False`
        """
        row_numbers = [[False for _ in self._range_size] for _ in self._range_size]
        col_numbers = [[False for _ in self._range_size] for _ in self._range_size]
        box_numbers = [[False for _ in self._range_size] for _ in self._range_size]

        for row in self._range_size:
            for col in self._range_size:
                cell = self._board[row][col]
                if cell == self._empty_cell_value:
                    continue

                value_index = cell - 1

                if row_numbers[row][value_index]:
                    return False

                if col_numbers[col][value_index]:
                    return False

                box = (row // self._bsize) * self._bsize + col // self._bsize
                if box_numbers[box][value_index]:
                    """
                    box: row, column
                    0: 0-2, 0-2
                    1: 0-2, 3-5
                    2: 0-2, 6-8
                    3: 3-5, 0-2
                    4: 3-5, 3-5
                    5: 3-5, 6-8
                    6: 6-8, 0-2
                    7: 6-8, 3-5
                    8: 6-8, 6-8
                    """
                    return False

                row_numbers[row][value_index] = True
                col_numbers[col][value_index] = True
                box_numbers[box][value_index] = True

        return True

    def _handle_error(self, code: _SudokuErrorCode):
        match code:
            case _SudokuErrorCode.INVALID_FORMAT:
                raise TypeError(f"The board must be a {Board}")
            case _SudokuErrorCode.INVALID_LENGTH:
                raise TypeError("Size of board must be 9x9")
            case _SudokuErrorCode.INVALID_DIGIT:
                raise ValueError(
                    """
                    Board's cell must be a digit of 0 to 9
                    (0 for empty cell)
                    """
                )
            case _SudokuErrorCode.INVALID_BOARD:
                raise ValueError("Board is invalid")
            case _:
                raise Exception("Unknown error code")


class SudokuSolver(_Sudoku):
    def solve(self):
        """
        Return the completed board if there is a solution

        Return None if there is no solution
        """

        blanks = self._get_blanks()
        are_blanks_filled = [False for _ in range(len(blanks))]
        blank_fillers = self._calculate_blank_cell_fillers(blanks)
        return self._get_solution(
            self._get_board_copy(),
            blanks,
            blank_fillers,
            are_blanks_filled,
        )

    def _get_blanks(self):
        blanks: List[Tuple[int, int]] = []
        for i in self._range_size:
            for j in self._range_size:
                if self._board[i][j] == self._empty_cell_value:
                    blanks.append((i, j))
        return blanks

    def _calculate_blank_cell_fillers(self, blanks: List[Cell]):
        valid_fillers = [
            [[True for _ in self._range_size] for _ in self._range_size]
            for _ in self._range_size
        ]
        for row, col in blanks:
            for i in self._range_size:
                same_row = self._board[row][i]
                same_col = self._board[i][col]
                if same_row and i != col:
                    valid_fillers[row][col][same_row - 1] = False
                if same_col and i != row:
                    valid_fillers[row][col][same_col - 1] = False
            box_row = row // self._bsize * self._bsize
            box_col = col // self._bsize * self._bsize
            for r_offset in self._range_bsize:
                for c_offset in self._range_bsize:
                    row_index = box_row + r_offset
                    col_index = box_col + c_offset

                    if row_index == row and col_index == col:
                        continue
                    cell = self._board[row_index][col_index]
                    if cell:
                        valid_fillers[row][col][cell - 1] = False
        return valid_fillers

    def _get_solution(
        self,
        board: Board,
        blanks: List[Cell],
        blank_fillers: List[List[List[bool]]],
        are_blanks_filled: List[bool],
    ) -> Board | None:
        chosen_blank = None
        chosen_blank_index = 0
        min_filler_count = None
        for i, blank in enumerate(blanks):
            row, col = blank
            if are_blanks_filled[i]:
                continue
            valid_filler_count = sum(blank_fillers[row][col])
            if valid_filler_count == 0:
                return None  # Cell cannot be filled with any number, no solution
            if not min_filler_count or valid_filler_count < min_filler_count:
                min_filler_count = valid_filler_count
                chosen_blank = blank
                chosen_blank_index = i

        if not chosen_blank:
            # All blanks are filled
            return board

        row, col = chosen_blank

        # Declare chosen blank as filled
        are_blanks_filled[chosen_blank_index] = True

        # Get the neighbors affected by the filling of the current cell
        revert_list = [False for _ in range(len(blanks))]

        for digit in self._range_size:
            # Only try filling this cell with valid fillers
            if not blank_fillers[row][col][digit]:
                continue

            # Test number in this cell, digit + 1 used as number is zero-indexed
            board[row][col] = digit + 1

            for i, blank in enumerate(blanks):
                if blank == chosen_blank:
                    continue

                blank_row, blank_col = blank

                if (
                    self._is_neighbor(chosen_blank, blank)
                    and blank_fillers[blank_row][blank_col][digit]
                ):
                    blank_fillers[blank_row][blank_col][digit] = False
                    revert_list[i] = True
                else:
                    revert_list[i] = False

            solution = self._get_solution(
                board, blanks, blank_fillers, are_blanks_filled
            )
            if solution:
                return solution

            # No solution found for this `digit`
            # Revalidating the `digit` as fillers for neighbors
            for i, blank in enumerate(blanks):
                if revert_list[i]:
                    blank_row, blank_col = blank
                    blank_fillers[blank_row][blank_col][digit] = True

        # No solution with the board
        # Redeclare chosen cell as empty
        board[row][col] = self._empty_cell_value
        are_blanks_filled[chosen_blank_index] = False

        return None

    def _is_neighbor(self, x: Cell, y: Cell):
        """
        Return `True` if `x` and `y` are neighbours

        Otherwise, return `False`
        """

        rowx, colx = x
        rowy, coly = y

        if rowx == rowy or colx == coly:
            return True

        browx, bcolx = rowx // self._bsize, colx // self._bsize
        browy, bcoly = rowy // self._bsize, coly // self._bsize
        return browx == browy and bcolx == bcoly

    def _get_board_copy(self):
        """
        Return a deep copy of the board
        """
        return [[cell for cell in row] for row in self._board]
