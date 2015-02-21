import chess


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
    while not b.is_game_over():
        if display:
            print(str(b) + '\n\n')

        if num_kings(b) != 2:
            error = BoardException("Incorrect number of kings!")
            error.board = b
            raise error

        m = best_move(b)
        b.push(m)

    if display and b.is_stalemate():
        print("STALEMATE")
