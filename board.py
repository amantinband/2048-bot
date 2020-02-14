from selenium.webdriver.common.keys import Keys

from tile import Tile

BOARD_SIZE = 4
EMPTY_TILE = 0


def get_tile_position(tile):
    i_pos = 3
    j_pos = 2
    position_array = tile.get_attribute('class').split()[2].split('-')
    return int(position_array[i_pos]) - 1, int(position_array[j_pos]) - 1


class Board:
    def __init__(self):
        self.board = [[Tile(0) for i in range(0, BOARD_SIZE)] for j in range(0, BOARD_SIZE)]
        self.board_changed = False

    def populate_from_web_page(self, web_page):
        tiles = web_page.find_elements_by_class_name("tile-new")
        for tile in tiles:
            i, j = get_tile_position(tile)
            self.board[i][j].value = int(tile.text)

    def set_value(self, i, j, value):
        self.board[i][j].value = value

    def get_tile(self, i, j):
        return self.board[i][j]

    def get_value(self, i, j):
        return self.board[i][j].value

    def clone(self):
        cloned_board = Board()
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE):
                cloned_board.set_value(i, j, self.get_value(i, j))

        return cloned_board

    def rotate_right(self):
        rotated_board = Board()
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE):
                rotated_board.set_value(i, j, self.get_value(BOARD_SIZE - 1 - j, i))
                rotated_board.get_tile(i, j).is_merged = self.get_tile(BOARD_SIZE-1-j, i).is_merged

        self.board = rotated_board.board

    def last_row_has_empty_spot(self):
        for col in range(0, BOARD_SIZE):
            if self.get_value(BOARD_SIZE - 1, col) == 0:
                return True
        return False

    def get_most_bottom_tile_position(self, row, col):
        for i in range(BOARD_SIZE - 1, row, -1):
            if self.board[i][col].value == 0:
                return i
        return row

    def press_down_arrow(self):
        pressed_board = Board()
        for i in range(BOARD_SIZE - 1, -1, -1):
            for j in range(0, BOARD_SIZE):
                val = self.get_value(i, j)
                if val != 0:
                    if i == (BOARD_SIZE - 1):  # already in most bottom row, just copy to same position
                        pressed_board.set_value(i, j, val)
                    else:
                        new_row = pressed_board.get_most_bottom_tile_position(i, j)
                        if new_row == (BOARD_SIZE - 1):  # most bottom row
                            pressed_board.set_value(BOARD_SIZE-1, j, val)
                            self.board_changed = True
                        elif (pressed_board.board[new_row + 1][j].value == val) and \
                                (not pressed_board.board[new_row + 1][j].is_merged):  # tile can be merged
                            pressed_board.set_value(new_row+1, j, val*2)
                            pressed_board.get_tile(new_row+1, j).is_merged = True
                            self.board_changed = True
                        elif new_row == i:  # tile cant be moved down, just copy to same position
                            pressed_board.set_value(i, j, val)
                        else:
                            pressed_board.set_value(new_row, j, val)
                            self.board_changed = True

        self.board = pressed_board.board  # update board

    def rotate_right_n(self, n):
        for i in range(0, n):
            self.rotate_right()

    def peek_right_arrow_pressed(self):
        arrow_pressed_board = self.clone()
        arrow_pressed_board.rotate_right_n(1)
        arrow_pressed_board.press_down_arrow()
        arrow_pressed_board.rotate_right_n(3)
        return arrow_pressed_board

    def peek_down_arrow_pressed(self):
        arrow_pressed_board = self.clone()
        arrow_pressed_board.press_down_arrow()
        return arrow_pressed_board

    def peek_left_arrow_pressed(self):
        arrow_pressed_board = self.clone()
        arrow_pressed_board.rotate_right_n(3)
        arrow_pressed_board.press_down_arrow()
        arrow_pressed_board.rotate_right_n(1)
        return arrow_pressed_board

    def peek_up_arrow_pressed(self):
        arrow_pressed_board = self.clone()
        arrow_pressed_board.rotate_right_n(2)
        arrow_pressed_board.press_down_arrow()
        arrow_pressed_board.rotate_right_n(2)
        return arrow_pressed_board

    def get_biggest_bottom(self):
        for col in range(BOARD_SIZE - 2, -1, -1):
            if self.get_value(BOARD_SIZE - 1, col) != EMPTY_TILE:
                return self.get_value(BOARD_SIZE - 1, col)
        return -1

    def get_biggest_right(self):
        for row in range(BOARD_SIZE - 2, -1, -1):
            if self.get_value(row, BOARD_SIZE - 1) != EMPTY_TILE:
                return self.get_value(row, BOARD_SIZE - 1)
        return -1

    def print_board(self):
        print('---------------------')
        for line in self.board:
            for tile in line:
                print(tile.value, end=' ')
            print()
        print('---------------------')

    def biggest_tile(self):
        biggest_tile = 0
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE):
                if self.get_value(i, j) > biggest_tile:
                    biggest_tile = self.get_value(i, j)
        return biggest_tile

    def add_new_tile(self, tile):
        try:
            i, j = get_tile_position(tile)
            self.set_value(i, j, int(tile.text))
            return True
        except ValueError:
            return False
