import sys

from weight import piece_value_weight, random_weight
import ai
import util


if __name__ == "__main__":
    white = ai.generate(util.possible_actions, piece_value_weight)
    black = ai.generate(util.possible_actions, random_weight)



    white_wins = 0
    black_wins = 0
    ties = 0

    total_games = int(sys.argv[1])
    for x in range(total_games):
        print("\r{} Ties, {} White, {} Black".format(ties, white_wins, black_wins))
        b = util.play_game(white, black, display=False)
        if b.is_checkmate():
            if util.white_wins(b):
                white_wins += 1
            else:
                black_wins += 1
        else:
            ties += 1



