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
            score += (board.get_value(i, j) * (2 if board.get_tile(i, j).is_merged else 0.8)) * ((i + 1) ** 2) * (
                    (j + 1) ** 2)

    if not board.biggest_in_corner():
        score /= 10

    for i in range(0, Board.BOARD_SIZE - 1):
        for j in range(0, Board.BOARD_SIZE):
            if board.get_value(i, j) == board.get_value(i + 1, j):
                score += board.get_value(i, j) ** 2
                score *= 1.7
            elif board.get_value(i, j) > board.get_value(i+1, j):
                score *= 0.9

    if key == Keys.ARROW_DOWN:
        score *= 2 ** board.number_of_merged_tiles()
        score *= 2.5 if board.get_value(Board.BOARD_SIZE - 1, 0) == Board.EMPTY_TILE else 1.5

    if not board.last_row_has_empty_spot() and key == Keys.ARROW_LEFT:
        if board.biggest_in_corner():
            score *= 1.2
        else:
            score *= 0.5

    return score
