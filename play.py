from weight import piece_value_weight
from util import play_game, possible_actions, generate_move_function


if __name__ == "__main__":
    best_move = generate_move_function(piece_value_weight, 2)
    play_game(best_move, best_move, display=True)

