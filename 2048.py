from game import Game


def main():
    while True:
        game = Game()
        game.start()
        game.take_screenshot()
        if game.board.biggest_tile() != 2048:
            game.close()


if __name__ == '__main__':
    main()
