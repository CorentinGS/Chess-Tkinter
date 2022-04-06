import numpy as np
from numpy import ndarray

import const


def init_board():
    board: ndarray = np.zeros((8, 8), dtype='int32')
    for y in (0, 1, 6, 7):
        if y in [0, 7]:
            board[y] = [const.PIECE_R, const.PIECE_N, const.PIECE_B, const.PIECE_Q, const.PIECE_K,
                        const.PIECE_B, const.PIECE_N, const.PIECE_R]
        else:
            for x in range(const.ROWS):
                board[y][x] = const.PIECE_P

    return board


class Chess:

    def __init__(self):
        self.board: ndarray = init_board()


ChessGame = Chess()
