from random import shuffle


def valid_num(board, row, col, num):
    """
    Check if a number is valid in a given cell by checking the row and colume and box.
    :param board: 2D list of numbers
    :param row: row index
    :param col: column index
    :param num: number to check
    :return: True if valid, False otherwise
    """
    if num in board[row]:
        return False

    for i in range(9):
        if board[i][col] == num:
            return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, (box_row + 3)):
        for j in range(box_col, (box_col + 3)):
            if board[i][j] == num:
                return False

    return True


def empty_cell_exists(board):
    """
    Check if there is an empty cell in the board.
    :param board: 2D list of numbers
    :return: True if empty, False otherwise
    """
    for row in board:
        if 0 in row:
            return True

    return False


def generate_board(board):
    """
    Generate a new board by back_tracking(recursion)
    :param board: 2D list of numbers
    :return: 2D list of numbers
    """
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(0, 81):
        row = i // 9
        col = i % 9
        if board[row][col] == 0:
            shuffle(nums)
            for num in nums:
                if valid_num(board, row, col, num):
                    board[row][col] = num
                    if not empty_cell_exists(board):
                        return True
                    elif generate_board(board):
                        return True
            break
    board[row][col] = 0
    return False


def remove_cells(board, difficulty):
    """
    Remove specific cells from the board depending on difficulty.
    :param board: 2D list of numbers
    :param difficulty: difficulty level
    :return: 2D list of numbers
    """
    row = 0
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while row < 9:
        shuffle(nums)
        for i in range(difficulty):
            col = nums[i]
            board[row][col] = ' '

        row += 1


def check_sudoku(game):
    """
    Check if the given answer from user is valid.
    :param game: 2D list of numbers
    :return: True if valid, False otherwise
    """
    n = len(game)
    if n < 1:
        return False
    for i in range(0, n):
        horizontal = []
        vertical = []
        for k in range(0, n):
            if game[k][i] in vertical:
                return False
            vertical.append(game[k][i])
            if game[i][k] in horizontal:
                return False
            horizontal.append(game[i][k])
    return True
