import pprint

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


def print_board(board):
    pprint.PrettyPrinter().pprint(board)


def box(board, row, col):
    box_r = 3 * (row // 3)
    box_c = 3 * (col // 3)
    return [board[i][j] for i in range(box_r, box_r + 3) for j in range(box_c, box_c + 3)]


def column(board, col):
    return [row[col] for row in board]


def candidate_is_possible(board, row, col, candidate):
    return board[row].count(candidate) == 0 and \
           column(board, col).count(candidate) == 0 and \
           box(board, row, col).count(candidate) == 0



def next_empty_cell(board):
    return next((row, col) for row in range(9) for col in range(9) if board[row][col] == 0)



def solver(board):
    try:
        row, col = next_empty_cell(board)
    except:
        # no more empty cells - board is solved, return a copy
        return [row[:] for row in board]
    for candidate in range(1, 10):
        if candidate_is_possible(board, row, col, candidate):
            board[row][col] = candidate
            solution = solver(board)
            board[row][col] = 0
            if solution:
                return solution

print_board(game2)
print_board(solver(game2))