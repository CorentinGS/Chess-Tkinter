import numpy as np
from numpy import ndarray
import const


def distance_min_2d(pos_1: tuple[int, int], pos_2: tuple[int, int]) -> int:
    """
    :param pos_1: first position
    :param pos_2: second position
    :return: distance between pos_1 and pos_2
    :rtype: int
    """
    return min(abs(pos_1[0] - pos_2[0]), abs(pos_1[1] - pos_2[1]))


def init_board(is_white: bool = True) -> ndarray:
    """
    :param is_white: is player white ?
    :return: initial board array
    :rtype: ndarray
    """
    board: ndarray = np.zeros((8, 8), dtype='int32')
    if not is_white:
        board[0] = const.initial_white_row_2
        for x in range(const.ROWS):
            board[1][x] = const.PIECE_P_W
            board[6][x] = const.PIECE_P_B

        board[7] = const.initial_black_row_2
    else:
        board[0] = const.initial_black_row
        for x in range(const.ROWS):
            board[1][x] = const.PIECE_P_B
            board[6][x] = const.PIECE_P_W

        board[7] = const.initial_white_row

    return board
