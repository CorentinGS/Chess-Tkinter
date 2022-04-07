import numpy as np
from numpy import ndarray

import callback
import const
from engine.engine import get_uci, MyChessEngine
from pieces import Piece
from utils import distance_min_2d

initial_white_row = [const.PIECE_R_W, const.PIECE_N_W, const.PIECE_B_W, const.PIECE_Q_W, const.PIECE_K_W,
                     const.PIECE_B_W, const.PIECE_N_W, const.PIECE_R_W]

initial_white_row_2 = [const.PIECE_R_W, const.PIECE_N_W, const.PIECE_B_W, const.PIECE_K_W, const.PIECE_Q_W,
                       const.PIECE_B_W, const.PIECE_N_W, const.PIECE_R_W]

initial_black_row = [const.PIECE_R_B, const.PIECE_N_B, const.PIECE_B_B, const.PIECE_Q_B, const.PIECE_K_B,
                     const.PIECE_B_B, const.PIECE_N_B, const.PIECE_R_B]

initial_black_row_2 = [const.PIECE_R_B, const.PIECE_N_B, const.PIECE_B_B, const.PIECE_K_B, const.PIECE_Q_B,
                       const.PIECE_B_B, const.PIECE_N_B, const.PIECE_R_B]


class Chess:
    is_white: bool

    def __init__(self, is_white: bool = True):
        self.is_white: bool = is_white
        self.board: ndarray = np.zeros((8, 8), dtype='int32')
        self.player_turn: bool = is_white
        self.en_passant: bool = False
        self.short_castle: bool = True
        self.long_castle: bool = True

    def init_board(self) -> ndarray:
        board: ndarray = np.zeros((8, 8), dtype='int32')
        if not self.is_white:
            board[0] = initial_white_row_2
            for x in range(const.ROWS):
                board[1][x] = const.PIECE_P_W
                board[6][x] = const.PIECE_P_B

            board[7] = initial_black_row_2
        else:
            board[0] = initial_black_row
            for x in range(const.ROWS):
                board[1][x] = const.PIECE_P_B
                board[6][x] = const.PIECE_P_W

            board[7] = initial_white_row

        self.board = board
        return self.board

    def is_check_mate(self) -> bool:
        king = self.get_king()
        king_piece: Piece = self.get_piece_at_position(king)
        if self.is_check(king_piece):
            for pos in self.legal_king(king_piece):
                target: Piece = self.get_piece_at_position(pos)
                if not self.is_check(target):
                    return False
            return True

        return False

    def is_check(self, king: Piece) -> bool:
        for x in range(8):
            for y in range(8):
                target: Piece = self.get_piece_at_position((x, y))
                if target.is_white() is not self.is_white and not target.is_empty():
                    if target.is_pawn():
                        if king.coords in self.legal_take_pawn(target, True):
                            return True

                    elif target.is_king():
                        if king.coords in self.legal_king(target, True):
                            return True
                    else:
                        if king.coords in self.legal_moves(target):
                            return True

        return False

    def get_king(self) -> tuple[int, int]:
        value = const.PIECE_K_W if self.is_white else const.PIECE_K_B
        index: list = list(np.vstack(np.where(self.board == value)).T[0])
        return index[1], index[0]

    def move_piece(self, piece: Piece, final_pos: tuple[int, int], escape: bool = False):
        if self.en_passant:
            self.en_passant = False
        keep = self.board[final_pos[1]][final_pos[0]]
        self.board[final_pos[1]][final_pos[0]] = self.board[piece.coords[1]][piece.coords[0]]
        self.board[piece.coords[1]][piece.coords[0]] = 0
        king = self.get_king()
        king_piece: Piece = self.get_piece_at_position(king)
        if self.is_check(king_piece):
            self.board[piece.coords[1]][piece.coords[0]] = self.board[final_pos[1]][final_pos[0]]
            self.board[final_pos[1]][final_pos[0]] = keep
            return

        if piece.is_empty():
            return

        callback.update_tkinter_chess_board()

        if not escape:
            MyChessEngine.play_move(get_uci(piece.coords, final_pos, self.is_white))

        if piece.is_pawn() and abs(piece.coords[1] - final_pos[1]) == 2:
            self.en_passant = True
        if piece.is_king():
            if piece.is_white() is self.is_white:
                self.short_castle, self.long_castle = False, False

            if piece.coords[0] - final_pos[0] == -2:
                target = self.get_piece_at_position((7, piece.coords[1]))
                self.move_piece(target, (final_pos[0] - 1, final_pos[1]), True)
            elif piece.coords[0] - final_pos[0] == 2:
                target = self.get_piece_at_position((0, piece.coords[1]))
                self.move_piece(target, (final_pos[0] + 1, final_pos[1]), True)

        elif piece.is_rook() and piece.coords == (7, 7):
            if self.is_white:
                self.short_castle = False
            else:
                self.long_castle = False

        elif piece.is_rook() and piece.coords == (0, 7):
            if self.is_white:
                self.long_castle = False
            else:
                self.short_castle = False

    def get_piece_at_position(self, pos: tuple[int, int]) -> Piece:
        return Piece(self.board[pos[1]][pos[0]], (pos[0], pos[1]))

    def legal_row(self, piece) -> list:
        legal_coords: list[tuple[int, int]] = []
        for x in range(0, piece.coords[0]):
            target = self.get_piece_at_position((piece.coords[0] - x - 1, piece.coords[1]))
            if target.is_empty():
                legal_coords.append(target.coords)
            elif target.is_white() is piece.is_white():
                break
            else:
                legal_coords.append(target.coords)
                break

        for x in range(piece.coords[0], 7):
            target = self.get_piece_at_position((x + 1, piece.coords[1]))
            if target.is_empty():
                legal_coords.append(target.coords)
            elif target.is_white() is piece.is_white():
                break
            else:
                legal_coords.append(target.coords)
                break

        return legal_coords

    def legal_column(self, piece) -> list:
        legal_coords: list[tuple[int, int]] = []
        for y in range(0, piece.coords[1]):
            target = self.get_piece_at_position((piece.coords[0], piece.coords[1] - y - 1))
            if target.is_empty():
                legal_coords.append(target.coords)
            elif target.is_white() is piece.is_white():
                break
            else:
                legal_coords.append(target.coords)
                break

        for y in range(piece.coords[1], 7):
            target = self.get_piece_at_position((piece.coords[0], y + 1))
            if target.is_empty():
                legal_coords.append(target.coords)
            elif target.is_white() is piece.is_white():
                break
            else:
                legal_coords.append(target.coords)
                break

        return legal_coords

    def legal_diagonal(self, piece) -> list:
        legal_coords: list[tuple[int, int]] = []
        for y in range(0, distance_min_2d(piece.coords, (0, 0))):
            target = self.get_piece_at_position((piece.coords[0] - y - 1, piece.coords[1] - y - 1))
            if target.is_empty():
                legal_coords.append(target.coords)
            elif target.is_white() is piece.is_white():
                break
            else:
                legal_coords.append(target.coords)
                break

        for y in range(0, distance_min_2d(piece.coords, (0, 7))):
            target = self.get_piece_at_position((piece.coords[0] - y - 1, piece.coords[1] + y + 1))
            if target.is_empty():
                legal_coords.append(target.coords)
            elif target.is_white() is piece.is_white():
                break
            else:
                legal_coords.append(target.coords)
                break

        for y in range(0, distance_min_2d(piece.coords, (7, 7))):
            target = self.get_piece_at_position((piece.coords[0] + y + 1, piece.coords[1] + y + 1))
            if target.is_empty():
                legal_coords.append(target.coords)
            elif target.is_white() is piece.is_white():
                break
            else:
                legal_coords.append(target.coords)
                break

        for y in range(0, distance_min_2d(piece.coords, (7, 0))):
            target = self.get_piece_at_position((piece.coords[0] + y + 1, piece.coords[1] - y - 1))
            if target.is_empty():
                legal_coords.append(target.coords)
            elif target.is_white() is piece.is_white():
                break
            else:
                legal_coords.append(target.coords)
                break

        return legal_coords

    def legal_rook(self, piece: Piece) -> list:
        legal_coords: list[tuple[int, int]] = self.legal_row(piece) + self.legal_column(piece)

        return legal_coords

    def legal_bishop(self, piece: Piece) -> list:
        return self.legal_diagonal(piece)

    def legal_take_pawn(self, piece: Piece, presume: bool = False) -> list:
        legal_coords: list[tuple[int, int]] = []
        diff = -1 if piece.is_white() is self.is_white else 1

        if not piece.coords[0] + 1 > 7:
            target = self.get_piece_at_position((piece.coords[0] + 1, piece.coords[1] + diff))
            if presume:
                legal_coords.append(target.coords)
            else:
                if not target.is_empty() and target.is_white() is not piece.is_white():
                    legal_coords.append(target.coords)

        if not piece.coords[0] - 1 < 0:
            target = self.get_piece_at_position((piece.coords[0] - 1, piece.coords[1] + diff))
            if presume:
                legal_coords.append(target.coords)
            else:
                if not target.is_empty() and target.is_white() is not piece.is_white():
                    legal_coords.append(target.coords)

        return legal_coords

    def legal_pawn(self, piece: Piece) -> list:
        legal_coords: list[tuple[int, int]] = []
        diff = -1 if piece.is_white() is self.is_white else 1
        target = self.get_piece_at_position((piece.coords[0], piece.coords[1] + diff))
        if target.is_empty():
            legal_coords.append(target.coords)
        if piece.coords[1] in [1, 6]:
            target = self.get_piece_at_position((piece.coords[0], piece.coords[1] + diff * 2))
            if target.is_empty():
                legal_coords.append(target.coords)

        legal_coords = legal_coords + self.legal_take_pawn(piece)

        if self.en_passant:
            if not piece.coords[0] + 1 > 7:
                target = self.get_piece_at_position((piece.coords[0] + 1, piece.coords[1]))
                if not target.is_empty():
                    if target.is_pawn() and target.is_white() is not piece.is_white():
                        legal_coords.append((piece.coords[0] + 1, piece.coords[1] + diff))
            if not piece.coords[0] - 1 < 0:
                target = self.get_piece_at_position((piece.coords[0] - 1, piece.coords[1]))

                if not target.is_empty():
                    if target.is_pawn() and target.is_white() is not piece.is_white():
                        legal_coords.append((piece.coords[0] - 1, piece.coords[1] + diff))

        return legal_coords

    def legal_queen(self, piece: Piece) -> list:
        legal_coords: list[tuple[int, int]] = self.legal_row(piece) + self.legal_column(piece) + self.legal_diagonal(
            piece)
        return legal_coords

    def legal_king(self, piece: Piece, presume: bool = False) -> list:
        legal_coords: list[tuple[int, int]] = []
        for x in range(3):
            for y in range(3):
                if x == 1 and y == 1 or \
                        piece.coords[0] - 1 + x > 7 or piece.coords[0] - 1 + x < 0 or \
                        piece.coords[1] - 1 + y > 7 or piece.coords[1] - 1 + y < 0:
                    continue
                target = self.get_piece_at_position((piece.coords[0] - 1 + x, piece.coords[1] - 1 + y))
                if presume:
                    legal_coords.append(target.coords)
                else:
                    if (target.is_empty() or target.is_white() is not piece.is_white()) and not self.is_check(target):
                        legal_coords.append(target.coords)

        if not presume:
            if self.short_castle:
                target = self.get_piece_at_position((7, 7))
                if target.is_rook() and target.is_white() is piece.is_white() and not self.is_check(target):
                    legal_coords.append((6, 7))
            if self.long_castle:
                target = self.get_piece_at_position((0, 7))
                if target.is_rook() and target.is_white() is piece.is_white() and not self.is_check(target):
                    legal_coords.append((2, 7))

        return legal_coords

    def legal_knight(self, piece: Piece) -> list:
        legal_coords: list[tuple[int, int]] = []
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
            if piece.coords[0] + x > 7 or piece.coords[0] + x < 0 or \
                    piece.coords[1] + y > 7 or piece.coords[1] + y < 0:
                continue
            target = self.get_piece_at_position((piece.coords[0] + x, piece.coords[1] + y))
            if target.is_empty() or target.is_white() is not piece.is_white():
                legal_coords.append(target.coords)

        return legal_coords

    def legal_moves(self, piece: Piece) -> list:
        if piece.is_rook():
            return self.legal_rook(piece)
        elif piece.is_bishop():
            return self.legal_bishop(piece)
        elif piece.is_pawn():
            return self.legal_pawn(piece)
        elif piece.is_queen():
            return self.legal_queen(piece)
        elif piece.is_king():
            return self.legal_king(piece)
        elif piece.is_knight():
            return self.legal_knight(piece)

        return []


ChessGame = Chess()


def play_move(pos1: tuple[int, int], pos2: tuple[int, int]):
    ChessGame.move_piece(ChessGame.get_piece_at_position(pos1), pos2)
