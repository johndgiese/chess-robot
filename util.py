from itertools import cycle

import chess
from ai import adversarial_search


def num_kings(board):
    return len([True for p in board.pieces if p == chess.KING])


class BoardException(Exception):
    board = None


def possible_actions(board):
    actions = list(board.legal_moves)
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
        print(m)
        
        b.push(m)

        if display:
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


def update_progress(progress):
    print('\r{0}%'.format(progress))


def generate_move_function(weight_func, steps_ahead):
    return adversarial_search(weight_func, possible_actions, step, steps_ahead)


