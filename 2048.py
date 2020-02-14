from game import Game


def main():
    while True:
        game = Game()
        game.start()
        game.take_screenshot()


if __name__ == '__main__':
    main()
