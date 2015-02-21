import random
import chess


def fresh_board():
    """Return a fresh chess board; white to move."""
    return chess.Bitboard()


def weight(board):
    """Return the weight of a board as a float."""
    return random.choice([1.0, 2.0, 3.0])  # TODO: implement


def next_boards(board):
    """
    Return a generator for producing possible next moves from a given
    board.
    """
    for m in board.legal_moves:
        board.push(m)
        yield chess.Bitboard(board.fen())  # create new board object
        board.pop()
