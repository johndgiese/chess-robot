from weight import weight
import chess
import ai


def possible_actions(board):
    for a in board.legal_moves:
        new_board = chess.Bitboard(board.fen())
        new_board.push(a)
        yield a, new_board


best_move = ai.generate(possible_actions, weight)


if __name__ == "__main__":

    b = chess.Bitboard()

    while not b.is_game_over():
        print(str(b) + '\n\n')
        m = best_move(b)
        b.push(m)
            
