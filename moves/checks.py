import numpy as np

import const
from pieces import Piece


def get_king(game):
    value = const.PIECE_K_W if game.is_white else const.PIECE_K_B
    index: list = list(np.vstack(np.where(game.board == value)).T[0])
    return Piece.get_piece_at_position(game.board, (index[1], index[0]))