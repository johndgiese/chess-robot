import chess
from weight import piece_value_weight


def num_kings(board):
    return len([True for p in board.pieces if p == chess.KING])


class BoardException(Exception):
    board = None


def possible_actions(board):
    for a in board.legal_moves:
        new_board = chess.Bitboard(board.fen())
        new_board.push(a)
        yield a, new_board


def play_game(best_move, display=False):
    b = chess.Bitboard()
    if display:
        print(str(b) + '\n\n')

    while not b.is_game_over():
        m = best_move(b)
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
