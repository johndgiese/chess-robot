from weight import weight, random_weight
from util import play_game, possible_actions, generate_move_function


if __name__ == "__main__":
    white = generate_move_function(weight, 3)
    black = generate_move_function(random_weight, 3)
    play_game(white, black, display=True)

