from unittest import TestCase

import numpy as np
from numpy import array, int32

from chess import ChessGame

initial_board_white = array([[22, 23, 24, 21, 20, 24, 23, 22],
                             [25, 25, 25, 25, 25, 25, 25, 25],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [15, 15, 15, 15, 15, 15, 15, 15],
                             [12, 13, 14, 11, 10, 14, 13, 12]], dtype=int32)

initial_board_black = array([[12, 13, 14, 11, 10, 14, 13, 12],
                             [15, 15, 15, 15, 15, 15, 15, 15],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [25, 25, 25, 25, 25, 25, 25, 25],
                             [22, 23, 24, 21, 20, 24, 23, 22]], dtype=int32)


class TestChess(TestCase):

    def test_init_board_white(self):
        ChessGame.is_white = True
        self.assertIsNone(np.testing.assert_array_equal(ChessGame.init_board(), initial_board_white))

    def test_init_board_black(self):
        ChessGame.is_white = False
        self.assertIsNone(np.testing.assert_array_equal(ChessGame.init_board(), initial_board_black))
