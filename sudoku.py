import pprint
from datetime import datetime

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

def print_grid(grid):
    """Prints out a Sudoku Grid to the console

    :param grid: the sudoku puzzle grid - a 9 x 9 list of lists of ints
    """
    pprint.PrettyPrinter().pprint(grid)


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
    return grid[row].count(candidate) == 0 and \
           column(grid, col).count(candidate) == 0 and \
           box(grid, row, col).count(candidate) == 0


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

class MultipleSolutionsGrid(Exception):
    pass

def has_multiple_solutions(grid):
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

