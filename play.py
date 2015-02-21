from weight import weight
import ai
from util import play_game, possible_actions


if __name__ == "__main__":
    best_move = ai.generate(possible_actions, weight)
    play_game(best_move, display=True)

