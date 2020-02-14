from selenium.webdriver.common.keys import Keys
import board as Board


def compute_board_score(board, key):
    if key == Keys.ARROW_UP:
        return 1

    if board.last_row_has_empty_spot() and key == Keys.LEFT:
        return 2

    score = 0
    for i in range(0, Board.BOARD_SIZE):
        for j in range(0, Board.BOARD_SIZE):
            score += (board.get_value(i, j) ** (3 if board.get_tile(i, j).is_merged else 1.5)) * ((i + 2) ** 2) * (
                    (j + 2.5) ** 2)
            if board.get_tile(i, j).is_merged:
                if key == Keys.ARROW_DOWN:
                    score *= 1.6

    for i in range(0, Board.BOARD_SIZE-1):
        for j in range(0, Board.BOARD_SIZE):
            if board.get_value(i, j) == board.get_value(i+1, j):
                score += board.get_value(i, j) ** 4
                score *= 1.5

    if key == Keys.ARROW_DOWN:
        score *= 1.5

    return score
