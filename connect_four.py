import copy
from termcolor import colored


class ConnectFourBoard(object):
    def __init__(self, cols, rows, num):
        self.cols = cols
        self.rows = rows
        self.num = num
        self.bins = [[] for c in range(cols)]
        self.current_player = 0

    def __copy__(self):
        new_board = ConnectFourBoard(self.cols, self.rows, self.num)
        new_board.bins = self.bins
        new_board.current_player = self.current_player

    def __str__(self):
        reversed_bins = [b[::-1] for b in self.bins]
        rows_as_strs = [[] for r in range(self.rows)]
        for rs in rows_as_strs:
            for b in reversed_bins:
                p = b.pop()
                if p is None:
                    char = "."
                elif p == 0:
                    char = colored("o", "red")
                elif p == 1:
                    char = colored("o", "blue")
                rs.append(char + " ")
        return "\n".join(["".join(r) for r in rows_as_strs[::-1]])


def play(old_board, move):
    board = copy(old_board)

    col, player = move
    board.bins[col].append(player)
    board.current_player = (board.current_player + 1) % 2
    return board


def valid_moves(board):
    return [col for col, b in enumerate(board.bins) if len(b) < board.rows]



def play_game(white_move_func, black_move_func, display=False):
    b = chess.Bitboard()
    if display:
        print(str(b) + '\n\n')

    move_functions = cycle([white_move_func, black_move_func])
    while not b.is_game_over():
        move_function = next(move_functions)
        m = move_function(b)
        b = play(b, m)

    return b
