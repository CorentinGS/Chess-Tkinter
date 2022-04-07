from unittest import TestCase

import numpy as np
from numpy import array, int32, ndarray

import const
from utils import utils
from utils.utils import init_board, distance_min_2d

initial_board_white = array([[22, 23, 24, 21, 20, 24, 23, 22],
                             [25, 25, 25, 25, 25, 25, 25, 25],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [15, 15, 15, 15, 15, 15, 15, 15],
                             [12, 13, 14, 11, 10, 14, 13, 12]], dtype=int32)

initial_board_black = array([[12, 13, 14, 10, 11, 14, 13, 12],
                             [15, 15, 15, 15, 15, 15, 15, 15],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [25, 25, 25, 25, 25, 25, 25, 25],
                             [22, 23, 24, 20, 21, 24, 23, 22]], dtype=int32)

positions = {
    1: (0, 0),
    2: (7, 7),
    3: (3, 4),
    4: (0, 7)
}


class Test(TestCase):

    def test_init_board(self):
        self.assertIsNone(np.testing.assert_array_equal(utils.init_board(True), initial_board_white))
        self.assertIsNone(np.testing.assert_array_equal(utils.init_board(False), initial_board_black))

    def test_distance_min_2d(self):
        self.assertEqual(distance_min_2d(positions[1], positions[2]), 7)
        self.assertEqual(distance_min_2d(positions[1], positions[3]), 3)
        self.assertEqual(distance_min_2d(positions[1], positions[4]), 0)
        self.assertEqual(distance_min_2d(positions[2], positions[3]), 3)
        self.assertEqual(distance_min_2d(positions[4], positions[3]), 3)
