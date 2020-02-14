import threading
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
            file_name = self.board.biggest_tile().__str__() + '.png'
        self.driver.save_screenshot(file_name)

    def add_new_tile(self):
        tile = self.web_page.find_element_by_class_name("tile-new")
        return self.board.add_new_tile(tile)

    def print_game_status(self):
        print("current board:")
        self.board.print_board()

    def create_boards(self):
        board_left = self.board.clone()
        board_right = self.board.clone()
        board_up = self.board.clone()
        board_down = self.board.clone()

        threads = [threading.Thread(target=board_left.press_left()),
                   threading.Thread(target=board_right.press_right()),
                   threading.Thread(target=board_up.press_up()),
                   threading.Thread(target=board_down.press_down())]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        boards = {Keys.ARROW_LEFT: board_left,
                  Keys.ARROW_RIGHT: board_right,
                  Keys.ARROW_UP: board_up,
                  Keys.ARROW_DOWN: board_down}

        return boards

    def move(self):
        boards = self.create_boards()

        valid_boards = {}
        for (key, board) in boards.items():
            if board.board_changed:
                valid_boards[key] = board

        max_score = 0
        winning_board = None
        winning_key = None

        for (key, board) in valid_boards.items():
            if board.score > max_score:
                max_score = board.score
                winning_board = board
                winning_key = key

        self.web_page.send_keys(winning_key)
        self.board = winning_board

    def start(self):
        while len(self.web_page.find_elements_by_class_name('game-over')) == 0:
            self.move()
            time.sleep(0.08)
            if self.board.biggest_tile() == 2048:
                break

            added_successfully = self.add_new_tile()
            while not added_successfully:
                time.sleep(0.5)
                added_successfully = self.add_new_tile()

    def close(self):
        self.driver.close()
