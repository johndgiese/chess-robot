from functools import reduce
from itertools import cycle
import random

import chess
from ai import adversarial_search
import weight as weight_mod


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

    move_functions = cycle([white_move_func, black_move_func])
    while not b.is_game_over():
        move_function = next(move_functions)
        m = move_function(b)
        
        b.push(m)

        if display:
            print('\n' + str(m))
            print(str(b))
            weight_mod.weight(b)
            print('\n\n')

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

    adjs = [
        square - 8,
        square + 8,
    ]

    if chess.file_index(square) != 0:
        adjs.append(square - 9)
        adjs.append(square - 1)
        adjs.append(square + 7)
    if chess.file_index(square) != 7:
        adjs.append(square - 7)
        adjs.append(square + 1)
        adjs.append(square + 9)

    return on_board(adjs)


def sum_list(summands):
    return reduce(lambda x, y: x + y, summands, 0)


def get_piece_squares(board):
    for s in chess.SQUARES:
        p = board.piece_at(s)
        if not p is None:
            yield p, s


def get_pieces(board, on=chess.SQUARES):
    return filter(lambda x: not x is None, [board.piece_at(s) for s in on])


def pawn_protecting_squares(color, protected_square):
    if color == chess.WHITE:
        if chess.file_index(protected_square) == 0:
            return [protected_square - 7]
        elif chess.file_index(protected_square) == 7:
            return [protected_square - 9]
        else:
            return [protected_square - 9, protected_square - 7]
    else:
        if chess.file_index(protected_square) == 0:
            return [protected_square + 9]
        elif chess.file_index(protected_square) == 7:
            return [protected_square + 7]
        else:
            return [protected_square + 9, protected_square + 7]


def is_tie(board):
    return board.is_game_over() and not board.is_checkmate()

