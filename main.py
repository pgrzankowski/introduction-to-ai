from minimax import Game


def main():
    game = Game(algorithm='minimax')
    game.run()
    game.plot_times()


if __name__ == "__main__":
    main()