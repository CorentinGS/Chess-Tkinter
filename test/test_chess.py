from unittest import TestCase

from numpy import array, int32

from chess import init_board

initial_board = array([[12, 13, 14, 11, 10, 14, 13, 12],
                       [15, 15, 15, 15, 15, 15, 15, 15],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [15, 15, 15, 15, 15, 15, 15, 15],
                       [12, 13, 14, 11, 10, 14, 13, 12]], dtype=int32)


class TestChess(TestCase):

    def test_init_board(self):
        self.assertEqual(init_board().all(), initial_board.all())
