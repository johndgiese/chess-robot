from jinja2 import Template

from weight import weight
import ai
from util import play_game, possible_actions, BoardException


if __name__ == "__main__":
    best_move = ai.generate(possible_actions, weight)

    test_template = Template(open("one_king_tests/test.template.py", "r").read())

    num_tests = 0
    while num_tests < 3:
        try:
            play_game(best_move, display=False)
        except BoardException as e:
            board = e.board
            test_file = open("one_king_tests/test_{}.py".format(str(num_tests).zfill(3)), "w")
            test_file.write(test_template.render(moves=board.move_stack))
            num_tests += 1



