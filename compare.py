import sys

from weight import weight
import util


if __name__ == "__main__":
    white = util.generate_move_function(True, weight, 2)
    black = util.generate_move_function(False, weight, 1)

    white_wins = 0
    black_wins = 0
    ties = 0

    total_games = int(sys.argv[1])
    for x in range(total_games):
        print("\r{} Ties, {} White, {} Black".format(ties, white_wins, black_wins))
        b = util.play_game(white, black, display=True)
        if b.is_checkmate():
            if util.white_wins(b):
                white_wins += 1
            else:
                black_wins += 1
        else:
            ties += 1



