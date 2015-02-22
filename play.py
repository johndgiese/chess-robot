from weight import piece_value_weight
import ai
from util import play_game, possible_actions


if __name__ == "__main__":
    best_move = ai.generate(possible_actions, piece_value_weight)
    play_game(best_move, display=True)

