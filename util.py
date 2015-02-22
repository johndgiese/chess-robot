from functools import reduce
from itertools import cycle
import random

import chess
from ai import adversarial_search


def white_minus_black(func):
    def decorated(*args, **kwargs):
        return func(chess.WHITE, *args, **kwargs) - func(chess.BLACK, *args, **kwargs)
    return decorated


def num_kings(board):
    return len([True for p in board.pieces if p == chess.KING])


class BoardException(Exception):
    board = None


def possible_actions(board):
    if board.is_game_over():
        return []
    else:
        actions = list(board.legal_moves)
        random.shuffle(actions)
        return actions

def step(board, move):
    new_board = chess.Bitboard(board.fen())
    new_board.push(move)
    return new_board


def play_game(white_move_func, black_move_func, display=False):
    b = chess.Bitboard()
    if display:
        print(str(b) + '\n\n')

    whites_turn = True
    while not b.is_game_over():
        if whites_turn:
            m = white_move_func(b)
        else:
            m = black_move_func(b)
        whites_turn = not whites_turn
        
        b.push(m)

        if display:
            print('\n' + str(m))
            print(str(b) + '\n\n')

    if display:
        if b.is_stalemate():
            print("STALEMATE")
        elif b.is_insufficient_material():
            print("INSUFFICIENT MATERIAL")
        elif b.is_seventyfive_moves():
            print("75 MOVES DRAW")
        elif b.is_fivefold_repitition():
            print("5-FOLD REPITITION")
        elif b.is_checkmate():
            print("CHECKMATE")

    return b


def whites_turn(board):
    return board.turn == chess.WHITE


def white_wins(board):
    return board.is_checkmate() and whites_turn(board)


def generate_move_function(is_white, weight_func, steps_ahead):
    if is_white:
        weight = weight_func
    else:
        weight = lambda b: -weight_func(b)

    return adversarial_search(weight, possible_actions, step, steps_ahead)


def attackers(color, board, square):
    return len(board.attackers(color, square))


attacker_imbalance = white_minus_black(attackers)


def on_board(squares):
    return filter(lambda x: 0 <= x < 64, squares)


def adjacent_squares(square):
    return on_board([
        square - 1,
        square + 1,

        square - 9,
        square - 8,
        square - 7,

        square + 9,
        square + 8,
        square + 7,
    ])


def sum_list(summands):
    return reduce(lambda x, y: x + y, summands, 0)


def get_piece_squares(board):
    for s in chess.SQUARES:
        p = board.piece_at(s)
        if not p is None:
            yield p, s

def get_pieces(board):
    return filter(lambda x: not x is None, [board.piece_at(s) for s in chess.SQUARES])

