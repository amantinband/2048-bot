from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import algorithm
from board import Board


class Game:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://2048game.com')
        time.sleep(0.5)
        self.web_page = self.driver.find_element_by_tag_name('html')

        self.board = Board()
        self.board.populate_from_web_page(self.web_page.find_element_by_class_name('tile-container'))

    def take_screenshot(self, file_name=None):
        if file_name is None:
            file_name = str(self.board.biggest_tile()) + '.png'
        self.driver.save_screenshot(file_name)

    def add_new_tile(self):
        tile = self.web_page.find_element_by_class_name("tile-new")
        return self.board.add_new_tile(tile)

    def print_game_status(self):
        print("current board:")
        self.board.print_board()

    def move(self):
        boards = {Keys.ARROW_LEFT: self.board.peek_left_arrow_pressed(),
                  Keys.ARROW_RIGHT: self.board.peek_right_arrow_pressed(),
                  Keys.ARROW_UP: self.board.peek_up_arrow_pressed(),
                  Keys.ARROW_DOWN: self.board.peek_down_arrow_pressed()}

        valid_boards = {}
        for (key, board) in boards.items():
            if board.board_changed:
                valid_boards[key] = board

        max_score = 0
        winning_board = None
        winning_key = None

        for (key, board) in valid_boards.items():
            board_score = algorithm.compute_board_score(board, key)

            if board_score > max_score:
                max_score = board_score
                winning_board = board
                winning_key = key

        self.web_page.send_keys(winning_key)
        self.board = winning_board

    def start(self):
        while len(self.web_page.find_elements_by_class_name('game-over')) == 0:
            self.move()
            time.sleep(0.15)
            if self.board.biggest_tile() == 2048:
                return

            added_successfully = self.add_new_tile()
            while not added_successfully:
                time.sleep(0.5)
                added_successfully = self.add_new_tile()
        self.driver.close()


