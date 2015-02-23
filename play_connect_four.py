import connect_four as c4
import ai


if __name__ == "__main__":
    white = adversarial_search(c4.weight, c4.valid_moves, c4.play, 3)
    black = adversarial_search(c4.weight, c4.valid_moves, c4.play, 3)

    c4.play_game(white, black, display=True)


