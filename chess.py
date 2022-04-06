import numpy as np
from numpy import ndarray

import callback
import const
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

    def move_piece(self, piece:Piece, final_pos: tuple[int, int]):
        if self.en_passant:
            self.en_passant = False
        self.board[final_pos[1]][final_pos[0]] = self.board[piece.coords[1]][piece.coords[0]]
        self.board[piece.coords[1]][piece.coords[0]] = 0
        if piece.is_pawn() and abs(piece.coords[1] - final_pos[1]) == 2:
            self.en_passant = True
        callback.update_tkinter_chess_board()

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

        target = self.get_piece_at_position((piece.coords[0] + 1, piece.coords[1] + diff))
        if not target.is_empty() and target.is_white() is not piece.is_white():
            legal_coords.append(target.coords)

        target = self.get_piece_at_position((piece.coords[0] - 1, piece.coords[1] + diff))
        if not target.is_empty() and target.is_white() is not piece.is_white():
            legal_coords.append(target.coords)

        if self.en_passant:
            target = self.get_piece_at_position((piece.coords[0] + 1, piece.coords[1]))
            if not target.is_empty():
                if target.is_pawn() and target.is_white() is not piece.is_white():
                    legal_coords.append((piece.coords[0] + 1, piece.coords[1] + diff))
            target = self.get_piece_at_position((piece.coords[0] - 1, piece.coords[1]))
            if not target.is_empty():
                if target.is_pawn() and target.is_white() is not piece.is_white():
                    legal_coords.append((piece.coords[0] - 1, piece.coords[1] + diff))

        return legal_coords

    def legal_queen(self, piece: Piece) -> list:
        legal_coords: list[tuple[int, int]] = self.legal_row(piece) + self.legal_column(piece) + self.legal_diagonal(
            piece)
        return legal_coords

    def legal_king(self, piece: Piece) -> list:
        legal_coords: list[tuple[int, int]] = []
        for x in range(3):
            for y in range(3):
                if x == 1 and y == 1 or \
                        piece.coords[0] - 1 + x > 7 or piece.coords[0] - 1 + x < 0 or \
                        piece.coords[1] - 1 + y > 7 or piece.coords[1] - 1 + y < 0:

                    continue
                target = self.get_piece_at_position((piece.coords[0] - 1 + x, piece.coords[1] - 1 + y))
                if target.is_empty() or target.is_white() is not piece.is_white():
                    legal_coords.append(target.coords)

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
