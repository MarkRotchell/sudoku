import pprint
from datetime import datetime
from random import shuffle
import time

'''Sample grids'''

game = [[0, 4, 0, 0, 0, 0, 1, 7, 9],
        [0, 0, 2, 0, 0, 8, 0, 5, 4],
        [0, 0, 6, 0, 0, 5, 0, 0, 8],
        [0, 8, 0, 0, 7, 0, 9, 1, 0],
        [0, 5, 0, 0, 9, 0, 0, 3, 0],
        [0, 1, 9, 0, 6, 0, 0, 4, 0],
        [3, 0, 0, 4, 0, 0, 7, 0, 0],
        [5, 7, 0, 1, 0, 0, 2, 0, 0],
        [9, 2, 8, 0, 0, 0, 0, 6, 0]]

game2 = [[7, 9, 0, 0, 0, 0, 0, 0, 3],
         [4, 0, 0, 0, 0, 0, 0, 6, 0],
         [8, 0, 1, 0, 0, 4, 0, 0, 2],
         [0, 0, 5, 0, 0, 0, 0, 0, 0],
         [3, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 4, 0, 0, 0, 6, 2, 0, 9],
         [2, 0, 0, 0, 3, 0, 5, 0, 6],
         [0, 3, 0, 6, 0, 5, 4, 2, 1],
         [0, 0, 0, 0, 0, 0, 3, 0, 0]]

game3 = [[1, 0, 0, 0, 0, 7, 0, 9, 0],
         [0, 3, 0, 0, 2, 0, 0, 0, 8],
         [0, 0, 9, 6, 0, 0, 5, 0, 0],
         [0, 0, 5, 3, 0, 0, 9, 0, 0],
         [0, 1, 0, 0, 8, 0, 0, 0, 2],
         [6, 0, 0, 0, 0, 4, 0, 0, 0],
         [3, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 4, 0, 0, 0, 0, 0, 0, 7],
         [0, 0, 7, 0, 0, 0, 3, 0, 0]]

multiple_solutions_game = [[7, 9, 0, 0, 0, 0, 0, 0, 0],
                           [4, 0, 0, 0, 0, 0, 0, 6, 0],
                           [8, 0, 1, 0, 0, 4, 0, 0, 2],
                           [0, 0, 5, 0, 0, 0, 0, 0, 0],
                           [3, 0, 0, 1, 0, 0, 0, 0, 0],
                           [0, 4, 0, 0, 0, 6, 2, 0, 9],
                           [2, 0, 0, 0, 3, 0, 5, 0, 6],
                           [0, 3, 0, 6, 0, 5, 4, 2, 1],
                           [0, 0, 0, 0, 0, 0, 3, 0, 0]]


def print_grid_as_lists(grid):
    """Prints out a Sudoku Grid to the console

    :param grid: the sudoku puzzle grid - a 9 x 9 list of lists of ints
    """
    pprint.PrettyPrinter().pprint(grid)


def print_sudoku(grid):
    """Print grid in sudoku-like format
    TODO: improve this - it's hacky
    :param grid: the sudoku puzzle grid to be printed - a 9 x 9 list of lists of ints
    """
    for i, row in enumerate(grid):
        row = [' ' if cell == 0 else str(cell) for cell in row]
        blocks = [row[n:n + 3] for n in [0, 3, 6]]
        print(' | '.join(' '.join(block) for block in blocks))
        if i in [2, 5]:
            print('-' * 21)


def print_grid_as_line(grid):
    """Cell values as contiguous one-line string

    :param grid: the sudoku puzzle grid to be flattened - a 9 x 9 list of lists of ints
    :return: (str) a single line containing 81 numbers with 0 for blank
    """
    return ''.join(''.join(str(cell) for cell in row) for row in grid)


def box(grid, row, col):
    """List of values in the same 3x3 grid as the target cell

    :param grid: the sudoku puzzle grid - a 9 x 9 list of lists of ints
    :param row: (int) the row index of the target cell (0-8)
    :param col: (int) the column index of the target cell (0-8)
    :return: (list of ints) the 9 values in the same 3x3 box as the target cell
    """
    box_r = 3 * (row // 3)
    box_c = 3 * (col // 3)
    return [grid[i][j] for i in range(box_r, box_r + 3) for j in range(box_c, box_c + 3)]


def box_not_row_or_col(grid, row, col):
    """List of values in the same 3x3 grid as the target cell, but not the same row or column

    :param grid: the sudoku puzzle grid - a 9 x 9 list of lists of ints
    :param row: (int) the row index of the target cell (0-8)
    :param col: (int) the column index of the target cell (0-8)
    :return: (list of ints) the 4 values in the same 3x3 box as the target cell but not the same row or col
    """
    return [grid[row // 3 * 3 + (row + i) % 3][col // 3 * 3 + (col + i) % 3] for i in [1, 2] for j in [1, 2]]


def column(grid, col):
    """List of values in the target column

    :param grid: the sudoku puzzle grid - a 9 x 9 list of lists of ints
    :param col: (int) the column index of the target cell (0-8)
    :return: (list of ints) the 9 values in the same column as the target cell
    """
    return [row[col] for row in grid]


def candidate_is_possible(grid, row, col, candidate):
    """Whether the candidate does not already occur in the same row, column or 3x3 box as the target cell

    :param grid: the sudoku puzzle grid - a 9 x 9 list of lists of ints
    :param row: (int) the row index of the target cell (0-8)
    :param col: (int) the column index of the target cell (0-8)
    :param candidate: (int) candidate value to be checked (1-9)
    :return: (bool) True if candidate does not appear in the same row, col or box as the target cell
    """
    # return grid[row].count(candidate) == 0 and \
    #        column(grid, col).count(candidate) == 0 and \
    #        box(grid, row, col).count(candidate) == 0
    return (candidate not in grid[row]) and (candidate not in column(grid, col)) and (
            candidate not in box_not_row_or_col(grid, row, col))


def next_empty_cell(grid):
    """Coordinates of the next cell which isn't already filled in

    :Raises: StopIteration if there are no empty cells left (i.e. the puzzle is solved)

    :param grid: the sudoku puzzle grid - a 9 x 9 list of lists of ints
    :return: (2-tuple of ints) row, col indices of the next empty grid
    """
    return next((row, col) for row in range(9) for col in range(9) if grid[row][col] == 0)


def solver(grid):
    """Returns a solution to the sudoku puzzle

    :param grid: the sudoku puzzle grid to be solved - a 9 x 9 list of lists of ints
    :return: the solved sudoku puzzle grid - a 9 x 9 list of lists of ints
    """
    try:
        row, col = next_empty_cell(grid)
    except StopIteration:
        # no more empty cells - grid is solved, return a copy
        return [row[:] for row in grid]
    for candidate in range(1, 10):
        if candidate_is_possible(grid, row, col, candidate):
            grid[row][col] = candidate
            solution = solver(grid)
            grid[row][col] = 0
            if solution:
                return solution


def solution_count(grid):
    """Number of possible solutions for the puzzle

    :param grid: the sudoku puzzle grid to be solved - a 9 x 9 list of lists of ints
    :return: (int) the number of possible solutions
    """
    try:
        row, col = next_empty_cell(grid)
    except StopIteration:
        # no more empty cells - grid is solved, return a copy
        return 1
    solutions = 0
    for candidate in range(1, 10):
        if candidate_is_possible(grid, row, col, candidate):
            grid[row][col] = candidate
            solutions += solution_count(grid)
    grid[row][col] = 0
    return solutions


def has_multiple_solutions(grid):
    """Whether a sudoku puzzle has ore than one solution

    :param grid: the sudoku puzzle grid to be solved - a 9 x 9 list of lists of ints
    :return: (bool) True if the puzzle has multiple solutions
    """

    class MultipleSolutionsGrid(Exception):
        pass

    def check_for_multiple_solutions(grid):
        try:
            row, col = next_empty_cell(grid)
        except StopIteration:
            # no more empty cells - grid is solved, return a copy
            return 1
        solutions = 0
        for candidate in range(1, 10):
            if candidate_is_possible(grid, row, col, candidate):
                grid[row][col] = candidate
                solutions += check_for_multiple_solutions(grid)
                if solutions > 1:
                    raise MultipleSolutionsGrid
        grid[row][col] = 0
        return solutions

    try:
        check_for_multiple_solutions([row[:] for row in grid])
        return False
    except MultipleSolutionsGrid:
        return True


def empty_grid():
    """An empty (all zeros) 9 x 9 grid

    :return: a 9 x 9 list of lists of int, all with value 0
    """
    return [[0 for _ in range(9)] for __ in range(9)]


def randomised_solver(grid):
    """Returns a solution to the sudoku puzzle with candidate values for each cell attemped in a random order

    Useful for filling in empty grids to create random magic squares

    :param grid: the sudoku puzzle grid to be solved - a 9 x 9 list of lists of ints
    :return: the solved sudoku puzzle grid - a 9 x 9 list of lists of ints
    """
    try:
        row, col = next_empty_cell(grid)
    except StopIteration:
        # no more empty cells - grid is solved, return a copy
        return [row[:] for row in grid]
    candidates = list(range(1, 10))
    shuffle(candidates)
    for candidate in candidates:
        if candidate_is_possible(grid, row, col, candidate):
            grid[row][col] = candidate
            solution = randomised_solver(grid)
            grid[row][col] = 0
            if solution:
                return solution


def new_puzzle():
    """Generate a new sudoku puzzle

    :return: the sudoku puzzle grid to be solved - a 9 x 9 list of lists of ints
    """
    grid = randomised_solver(empty_grid())
    cells = [(row, col) for row in range(9) for col in range(4)] + [(row, 4) for row in range(5)]
    cells = [((row, col), (8 - row, 8 - col)) for row, col in cells]
    shuffle(cells)
    for (r1, c1), (r2, c2) in cells:
        candidate_grid = [row[:] for row in grid]
        candidate_grid[r1][c1] = 0
        candidate_grid[r2][c2] = 0
        if not has_multiple_solutions(candidate_grid):
            grid = candidate_grid
    return grid


def count_clues(grid):
    """The number of non-blanks in the puzzle

    :param grid: the sudoku puzzle grid to be analysed - a 9 x 9 list of lists of ints
    :return: (int) the number of clues which are not blank (i.e. not 0)
    """
    return sum(sum(1 for cell in row if cell != 0) for row in grid)


print_sudoku(game)
print()
print_sudoku(solver(game))
