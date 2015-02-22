from functools import lru_cache, reduce
import random
import chess
from util import *


def handle_checkmate(func):
    def decorated(board):
        if board.is_checkmate():
            if white_wins(board):
                return 10000000.0
            else:
                return -10000000.0
        else:
            return func(board)
    return decorated


@handle_checkmate
def random_weight(board):
    """Return the weight of a board as a float."""
    return random.choice([1.0, 2.0, 3.0])  # TODO: implement


@lru_cache(maxsize=10000)
@handle_checkmate
def weight(board):
    pv = piece_value_weight(board)
    cc = control_center_weight(board)
    cw = check_weight(board)
    akw = attack_king_weight(board)
    aqw = attack_queen_weight(board)
    return pv + cc/10 + cw + akw/8 + aqw/10



PIECE_WEIGHTS = {
    chess.NONE: 0,
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 8,
    chess.KING: 0,
}


@white_minus_black
def piece_value_weight(color, board):
    score = 0
    for p in filter(lambda p: p.color == color, get_pieces(board)):
        score += PIECE_WEIGHTS[p.piece_type]
    return score


@white_minus_black
def control_center_weight(color, board):
    if color == chess.WHITE:
        center_squares = [
            chess.C4, chess.D4, chess.E4, chess.F4,
            chess.C5, chess.D5, chess.E5, chess.F5,
            chess.C6, chess.D6, chess.E6, chess.F6,
        ]
    else:
        center_squares = [
            chess.C3, chess.D3, chess.E3, chess.F3,
            chess.C4, chess.D4, chess.E4, chess.F4,
            chess.C5, chess.D5, chess.E5, chess.F5,
        ]
    return sum_list([attackers(color, board, s) for s in center_squares])


def check_weight(board):
    if board.is_check():
        return -1 if whites_turn(board) else 1
    else:
        return 0


@white_minus_black
def attack_king_weight(color, board):
    king_square = [s for p, s in get_piece_squares(board) if p.piece_type == chess.KING and p.color == color][0]
    near_king = adjacent_squares(king_square)
    opposite_color = chess.BLACK if color == chess.WHITE else chess.WHITE
    pressure_on_king = sum_list([attackers(opposite_color, board, s) for s in near_king])
    return -pressure_on_king


@white_minus_black
def attack_queen_weight(color, board):
    try:
        queen_square = [s for p, s in get_piece_squares(board) if p.piece_type == chess.QUEEN and p.color == color][0]
    except IndexError:
        return 0

    near_queen = adjacent_squares(queen_square)
    opposite_color = chess.BLACK if color == chess.WHITE else chess.WHITE
    pressure_on_queen = sum_list([attackers(opposite_color, board, s) for s in near_queen])
    return -pressure_on_queen

