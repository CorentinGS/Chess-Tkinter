import numpy as np
from numpy import ndarray

import const

initial_white_row = [const.PIECE_R_W, const.PIECE_N_W, const.PIECE_B_W, const.PIECE_Q_W, const.PIECE_K_W,
                     const.PIECE_B_W, const.PIECE_N_W, const.PIECE_R_W]

initial_black_row = [const.PIECE_R_B, const.PIECE_N_B, const.PIECE_B_B, const.PIECE_Q_B, const.PIECE_K_B,
                     const.PIECE_B_B, const.PIECE_N_B, const.PIECE_R_B]


class Chess:
    is_white: bool

    def __init__(self, is_white: bool = True):
        self.is_white: bool = is_white
        self.board: ndarray = np.zeros((8, 8), dtype='int32')

    def init_board(self) -> ndarray:
        board: ndarray = np.zeros((8, 8), dtype='int32')
        if not self.is_white:
            board[0] = initial_white_row
            for x in range(const.ROWS):
                board[1][x] = const.PIECE_P_W
                board[6][x] = const.PIECE_P_B

            board[7] = initial_black_row
        else:
            board[0] = initial_black_row
            for x in range(const.ROWS):
                board[1][x] = const.PIECE_P_B
                board[6][x] = const.PIECE_P_W

            board[7] = initial_white_row

        self.board = board
        return self.board

    def move_piece(self, init_pos: tuple[int, int], final_pos: tuple[int, int]):
        self.board[final_pos[0]][final_pos[1]] = self.board[init_pos[0]][init_pos[1]]
        self.board[init_pos[0]][init_pos[1]] = 0


ChessGame = Chess()
