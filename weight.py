from functools import lru_cache, reduce
import random
import chess
from util import *
from db_cache import memoize_weight_with_db


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


def avoid_tie_when_winning(func):
    def decorated(b):
        score = func(b)
        if is_tie(b):
            if score > 0:
                return -10000
            else:
                return 10000
        else:
            return score
    return decorated


@memoize_weight_with_db
@avoid_tie_when_winning
@handle_checkmate
def weight(board):
    pv = 2*piece_value_weight(board)
    cc = control_center_weight(board)/5
    ic = check_weight(board)
    ak = attack_king_weight(board)/8
    aq = attack_queen_weight(board)/20
    ps = pawn_structure_weight(board)/4
    kp = protect_king(board)

    return pv + cc + ic + ak + aq + ps + kp


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
            (chess.C3, 0.1), (chess.D3, 0.2), (chess.E3, 0.2), (chess.F3, 0.1),
            (chess.C4, 0.3), (chess.D4, 0.4), (chess.E4, 0.4), (chess.F4, 0.3),
            (chess.C5, 0.5), (chess.D5, 0.9), (chess.E5, 0.8), (chess.F5, 0.3),
            (chess.C6, 0.5), (chess.D6, 0.7), (chess.E6, 0.6), (chess.F6, 0.4),
        ]
    else:
        center_squares = [
            (chess.C3, 0.5), (chess.D3, 0.7), (chess.E3, 0.6), (chess.F3, 0.4),
            (chess.C4, 0.5), (chess.D4, 0.9), (chess.E4, 0.8), (chess.F4, 0.3),
            (chess.C5, 0.3), (chess.D5, 0.4), (chess.E5, 0.4), (chess.F5, 0.3),
            (chess.C6, 0.1), (chess.D6, 0.2), (chess.E6, 0.2), (chess.F6, 0.1),
        ]

    return sum_list([s[1]*attackers(color, board, s[0]) for s in center_squares])


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


@white_minus_black
def pawn_structure_weight(color, board):
    pawn_squares = [s for p, s in get_piece_squares(board) if p.piece_type == chess.PAWN and p.color == color]
    num_pawns = len(pawn_squares)

    if num_pawns == 0:
        return 0

    # doubled pawns are bad
    pawns_per_file = [len([s for s in pawn_squares if chess.file_index(s) == f]) for f in range(7)]
    doubled_pawns = sum_list([ppf - 1 for ppf in pawns_per_file if ppf != 0])

    protecting_pawns = sum_list([1 for s in pawn_squares for ps in pawn_squares if s in pawn_protecting_squares(color, ps)])

    # divide out by number of pawns as this is less important the fewer pawns you have
    return (-doubled_pawns*4 + protecting_pawns*2)/num_pawns


@white_minus_black
def protect_king(color, board):
    king_square = [s for p, s in get_piece_squares(board) if p.piece_type == chess.KING and p.color == color][0]
    near_king = adjacent_squares(king_square)
    
    p_near_king = filter(lambda p: p.color == color, get_pieces(board, on=near_king))
    other_near_king = len(list(p_near_king))
    pawn_near_king = len(list(filter(lambda p: p.piece_type == chess.PAWN, p_near_king)))

    king_in_middle = {
        0: 0.0,
        1: 0.1,
        2: 0.2,
        3: 0.5,
        4: 0.6,
        5: 0.3,
        6: 0.2,
        7: 0.0,
    }[chess.file_index(king_square)]

    return (pawn_near_king + other_near_king/3 - king_in_middle)/20

