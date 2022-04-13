from typing import Tuple

import const
import game
from utils.utils import distance_min_2d


def is_empty(value: int) -> bool:
    """
    :rtype: bool
    :param value: Piece value identifier
    :return: is piece empty
    """
    return value == const.PIECE_NONE


def is_rook(value: int) -> bool:
    """
    :rtype: bool
    :param value: Piece value identifier
    :return: is piece rook
    """
    return str(value)[1] == '2'


def is_queen(value: int) -> bool:
    """
    :rtype: bool
    :param value: Piece value identifier
    :return: is piece queen
    """
    return str(value)[1] == '1'


def is_king(value: int) -> bool:
    """
    :rtype: bool
    :param value: Piece value identifier
    :return: is piece king
    """
    return str(value)[1] == '0'


def is_bishop(value: int) -> bool:
    """
    :rtype: bool
    :param value: Piece value identifier
    :return: is piece bishop
    """
    return str(value)[1] == '4'


def is_knight(value: int) -> bool:
    """
    :rtype: bool
    :param value: Piece value identifier
    :return: is piece knight
    """
    return str(value)[1] == '3'


def is_pawn(value: int) -> bool:
    """
    :rtype: bool
    :param value: Piece value identifier
    :return: is piece pawn
    """
    return str(value)[1] == '5'


def is_white(value: int) -> bool:
    """
    :rtype: bool
    :param value: Piece value identifier
    :return: is piece white
    """
    return str(value)[0] == '1'


class Piece:

    def __init__(self, is_piece_white: bool, coords: Tuple[int, int], piece_type: int):
        """
        :param is_piece_white: is piece white ? 
        :param coords: piece coords on array
        :param piece_type: piece type identifier
        """

        self.is_white: bool = is_piece_white
        self.coords: Tuple[int, int] = coords
        self.piece_type = piece_type

    @staticmethod
    def get_piece_at_position(pos: Tuple[int, int]):
        """
        :param pos: position to check
        :return: piece at given pos
        :rtype: Piece | Empty | King | Queen | Knight | Bishop | Pawn | Rook
        """

        value = game.MyGame.chess.board[pos[1]][pos[0]]
        if is_empty(value):
            return Empty((pos[0], pos[1]))
        if is_rook(value):
            return Rook(is_white(value), (pos[0], pos[1]))
        if is_bishop(value):
            return Bishop(is_white(value), (pos[0], pos[1]))
        if is_pawn(value):
            return Pawn(is_white(value), (pos[0], pos[1]))
        if is_queen(value):
            return Queen(is_white(value), (pos[0], pos[1]))
        if is_king(value):
            return King(is_white(value), (pos[0], pos[1]))
        if is_knight(value):
            return Knight(is_white(value), (pos[0], pos[1]))

        return Empty((pos[0], pos[1]))

    def legal_row(self) -> list:
        """
        Legal row square
        """
        legal_coords: list = []
        for x in range(0, self.coords[0]):
            target = Piece.get_piece_at_position((self.coords[0] - x - 1, self.coords[1]))
            if type(target) is Empty:
                legal_coords.append(target.coords)
            elif target.is_white is self.is_white:
                break
            else:
                legal_coords.append(target.coords)
                break

        for x in range(self.coords[0], 7):
            target = Piece.get_piece_at_position((x + 1, self.coords[1]))
            if type(target) is Empty:
                legal_coords.append(target.coords)
            elif target.is_white is self.is_white:
                break
            else:
                legal_coords.append(target.coords)
                break

        return legal_coords

    def legal_column(self) -> list:
        """
        Legal column square
        """
        legal_coords: list = []
        for y in range(0, self.coords[1]):
            target = Piece.get_piece_at_position((self.coords[0], self.coords[1] - y - 1))
            if type(target) is Empty:
                legal_coords.append(target.coords)
            elif target.is_white is self.is_white:
                break
            else:
                legal_coords.append(target.coords)
                break

        for y in range(self.coords[1], 7):
            target = Piece.get_piece_at_position((self.coords[0], y + 1))
            if type(target) is Empty:
                legal_coords.append(target.coords)
            elif target.is_white is self.is_white:
                break
            else:
                legal_coords.append(target.coords)
                break

        return legal_coords

    def legal_diagonal(self) -> list:
        """
        Legal diagonals square
        """
        legal_coords: list[Tuple[int, int]] = []
        for y in range(0, distance_min_2d(self.coords, (0, 0))):
            target = Piece.get_piece_at_position((self.coords[0] - y - 1, self.coords[1] - y - 1))
            if type(target) is Empty:
                legal_coords.append(target.coords)
            elif target.is_white is self.is_white:
                break
            else:
                legal_coords.append(target.coords)
                break

        for y in range(0, distance_min_2d(self.coords, (0, 7))):
            target = Piece.get_piece_at_position((self.coords[0] - y - 1, self.coords[1] + y + 1))
            if type(target) is Empty:
                legal_coords.append(target.coords)
            elif target.is_white is self.is_white:
                break
            else:
                legal_coords.append(target.coords)
                break

        for y in range(0, distance_min_2d(self.coords, (7, 7))):
            target = Piece.get_piece_at_position((self.coords[0] + y + 1, self.coords[1] + y + 1))
            if type(target) is Empty:
                legal_coords.append(target.coords)
            elif target.is_white is self.is_white:
                break
            else:
                legal_coords.append(target.coords)
                break

        for y in range(0, distance_min_2d(self.coords, (7, 0))):
            target = Piece.get_piece_at_position((self.coords[0] + y + 1, self.coords[1] - y - 1))
            if type(target) is Empty:
                legal_coords.append(target.coords)
            elif target.is_white is self.is_white:
                break
            else:
                legal_coords.append(target.coords)
                break

        return legal_coords


class Empty(Piece):
    def __init__(self, coords: Tuple[int, int]):
        self.piece_type = const.PIECE_NONE
        super().__init__(False, coords, self.piece_type)


class Rook(Piece):
    def __init__(self, is_piece_white: bool, coords: Tuple[int, int]):
        self.piece_type = const.PIECE_R_W if is_piece_white else const.PIECE_R_B

        super().__init__(is_piece_white, coords, self.piece_type)

    def legal_moves(self):
        legal_coords: list[Tuple[int, int]] = self.legal_row() + self.legal_column()

        return legal_coords


class Bishop(Piece):
    def __init__(self, is_piece_white: bool, coords: Tuple[int, int]):
        self.piece_type = const.PIECE_B_W if is_piece_white else const.PIECE_B_B

        super().__init__(is_piece_white, coords, self.piece_type)

    def legal_moves(self):
        return self.legal_diagonal()


class Pawn(Piece):
    def __init__(self, is_piece_white: bool, coords: Tuple[int, int]):
        self.piece_type = const.PIECE_P_W if is_piece_white else const.PIECE_P_B

        super().__init__(is_piece_white, coords, self.piece_type)

    def legal_moves(self):
        legal_coords: list[Tuple[int, int]] = []
        diff = -1 if self.is_white is game.MyGame.is_white else 1
        target = Piece.get_piece_at_position((self.coords[0], self.coords[1] + diff))
        if type(target) is Empty:
            legal_coords.append(target.coords)
        if self.coords[1] in [1, 6]:
            target = Piece.get_piece_at_position((self.coords[0], self.coords[1] + diff * 2))
            if type(target) is Empty:
                legal_coords.append(target.coords)

        legal_coords = legal_coords + self.legal_take_pawn()

        return legal_coords

    def legal_take_pawn(self, presume: bool = False) -> list:
        legal_coords: list[Tuple[int, int]] = []
        diff = -1 if self.is_white is game.MyGame.is_white else 1

        if not self.coords[0] + 1 > 7:
            target = Piece.get_piece_at_position((self.coords[0] + 1, self.coords[1] + diff))
            if presume:
                legal_coords.append(target.coords)
            else:
                if not type(target) is Empty and target.is_white is not self.is_white:
                    legal_coords.append(target.coords)

        if not self.coords[0] - 1 < 0:
            target = Piece.get_piece_at_position((self.coords[0] - 1, self.coords[1] + diff))
            if presume:
                legal_coords.append(target.coords)
            else:
                if not type(target) is Empty and target.is_white is not self.is_white:
                    legal_coords.append(target.coords)

        return legal_coords


class Queen(Piece):
    def __init__(self, is_piece_white: bool, coords: Tuple[int, int]):
        self.piece_type = const.PIECE_Q_W if is_piece_white else const.PIECE_Q_B
        super().__init__(is_piece_white, coords, self.piece_type)

    def legal_moves(self):
        legal_coords: list[Tuple[int, int]] = self.legal_row() + \
                                              self.legal_column() + \
                                              self.legal_diagonal()
        return legal_coords


class Knight(Piece):
    def __init__(self, is_piece_white: bool, coords: Tuple[int, int]):
        self.piece_type = const.PIECE_N_W if is_piece_white else const.PIECE_N_B
        super().__init__(is_piece_white, coords, self.piece_type)

    def legal_moves(self):
        legal_coords: list[Tuple[int, int]] = []
        diff = [
            (1, -2),
            (1, 2),
            (-1, -2),
            (-1, 2),
            (2, -1),
            (2, 1),
            (-2, -1),
            (-2, 1)
        ]
        for value in diff:
            x, y = value
            if self.coords[0] + x > 7 or self.coords[0] + x < 0 or \
                    self.coords[1] + y > 7 or self.coords[1] + y < 0:
                continue
            target = Piece.get_piece_at_position((self.coords[0] + x, self.coords[1] + y))
            if type(target) is Empty or target.is_white is not self.is_white:
                legal_coords.append(target.coords)

        return legal_coords


class King(Piece):
    def __init__(self, is_piece_white: bool, coords: Tuple[int, int]):
        self.piece_type = const.PIECE_K_W if is_piece_white else const.PIECE_K_B
        super().__init__(is_piece_white, coords, self.piece_type)

    def legal_moves(self, presume: bool = False):
        legal_coords: list[Tuple[int, int]] = []
        for x in range(3):
            for y in range(3):
                if x == 1 and y == 1 or \
                        self.coords[0] - 1 + x > 7 or self.coords[0] - 1 + x < 0 or \
                        self.coords[1] - 1 + y > 7 or self.coords[1] - 1 + y < 0:
                    continue
                target = Piece.get_piece_at_position((self.coords[0] - 1 + x, self.coords[1] - 1 + y))
                if presume:
                    legal_coords.append(target.coords)
                else:
                    if type(target) is Empty or target.is_white is not self.is_white:
                        legal_coords.append(target.coords)

        if not presume:
            if game.MyGame.chess.short_castle:
                target = Piece.get_piece_at_position((7, 7))
                if type(target) is Rook and target.is_white is self.is_white and not self.is_check():
                    legal_coords.append((6, 7))
            if game.MyGame.chess.long_castle:
                target = Piece.get_piece_at_position((0, 7))
                if type(target) is Rook and target.is_white is self.is_white and not self.is_check():
                    legal_coords.append((2, 7))

        return legal_coords

    def is_check(self) -> bool:
        for x in range(8):
            for y in range(8):
                target = Piece.get_piece_at_position((x, y))
                if self.makes_check(target):
                    return True
        return False

    def makes_check(self, attacker) -> bool:
        if attacker.is_white is not self.is_white and not type(attacker) is Empty:
            if type(attacker) is Pawn:
                if self.coords in attacker.legal_take_pawn(True):
                    return True

            elif type(attacker) is King:
                if self.coords in attacker.legal_moves(True):
                    return True
            else:
                if self.coords in attacker.legal_moves():
                    return True
        return False
