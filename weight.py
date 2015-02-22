import random
import chess


def random_weight(board):
    """Return the weight of a board as a float."""
    return random.choice([1.0, 2.0, 3.0])  # TODO: implement


PIECE_WEIGHTS = {
    chess.NONE: 0,
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 8,
    chess.KING: 0,
}


def piece_value_weight(board):
    score = 0
    pieces = filter(lambda x: not x is None, [board.piece_at(s) for s in chess.SQUARES])
    for p in pieces:
        score += (1 if p.color == chess.WHITE else -1)*PIECE_WEIGHTS[p.piece_type]
    return score



