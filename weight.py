from functools import lru_cache, reduce
import random
import chess
import util


def handle_checkmate(func):
    def decorated(board):
        if board.is_checkmate():
            if util.white_wins(board):
                return 10000000.0
            else:
                return -10000000.0
        else:
            return func(board)
    return decorated


@lru_cache(maxsize=1000)
@handle_checkmate
def random_weight(board):
    """Return the weight of a board as a float."""
    return random.choice([1.0, 2.0, 3.0])  # TODO: implement


@lru_cache(maxsize=1000)
@handle_checkmate
def weight(board):
    pv = piece_value_weight(board)
    cc = control_center_weight(board)
    return pv + cc/10



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


def control_center_weight(board):
    center_squares = [
        chess.C3, chess.D3, chess.E3, chess.F3,
        chess.C4, chess.D4, chess.E4, chess.F4,
        chess.C5, chess.D5, chess.E5, chess.F5,
        chess.C6, chess.D6, chess.E6, chess.F6,
    ]
    return reduce(lambda x, y: x + y, [util.attacker_imbalance(board, s) for s in center_squares])
