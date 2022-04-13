import numpy as np
from numpy import ndarray

import game
from engine.engine import get_uci
from pieces import Piece, Pawn, King, Rook, Empty
import const
from utils import utils
from typing import Tuple



class Chess:

    def __init__(self):
        # Setup default chess game logic
        self.board: ndarray = np.zeros((8, 8), dtype='int32')
        self.en_passant: bool = False
        self.short_castle: bool = True
        self.long_castle: bool = True

    def init_board(self, is_white: bool = True) -> ndarray:
        """
        :param is_white: is player white ?
        :return: initial board array
        :rtype: ndarray
        """
        self.board = utils.init_board(is_white)
        return self.board

    def get_king(self) -> Tuple[int, int]:
        """
        Gets king position
        :return: King position
        """
        value = const.PIECE_K_W if game.MyGame.is_white else const.PIECE_K_B
        index: list = list(np.vstack(np.where(self.board == value)).T[0])
        return index[1], index[0]

    def move_piece(self, piece: Piece, final_pos: Tuple[int, int], escape: bool = False) -> bool:
        """
        Moves a piece on the board
        :param piece: Piece to move
        :param final_pos: Final position of the piece
        :param escape: Should we escape some logic
        :return: Error check
        """
        # Check type
        if type(piece) is Empty:
            return False

        # En_passant logic
        if self.en_passant:
            self.en_passant = False

        # Store old position in case of rollback
        keep = self.board[final_pos[1]][final_pos[0]]

        # Update board with new positions
        self.board[final_pos[1]][final_pos[0]] = self.board[piece.coords[1]][piece.coords[0]]
        self.board[piece.coords[1]][piece.coords[0]] = 0

        if not escape:
            # Get the king
            king = Piece.get_piece_at_position(self.get_king())
            # Check for check position
            if type(king) is King and king.is_check():
                # Rollback and cancel the move
                self.board[piece.coords[1]][piece.coords[0]] = self.board[final_pos[1]][final_pos[0]]
                self.board[final_pos[1]][final_pos[0]] = keep
                return False

        # Render new position
        game.MyGame.gui.render_pieces(game.MyGame.chess.board)

        if not escape:
            # Update engine position
            game.MyGame.chess_engine.board.push_uci(get_uci(piece.coords, final_pos))

        # Update en_passant logic
        if type(piece) is Pawn and abs(piece.coords[1] - final_pos[1]) == 2:
            self.en_passant = True

        # Update castling logic
        if type(piece) is King:
            if piece.is_white is game.MyGame.is_white:
                self.short_castle, self.long_castle = False, False
            # Move rook if castling
            if piece.coords[0] - final_pos[0] == -2:
                target = Piece.get_piece_at_position((7, piece.coords[1]))
                self.move_piece(target, (final_pos[0] - 1, final_pos[1]), True)
            elif piece.coords[0] - final_pos[0] == 2:
                target = Piece.get_piece_at_position((0, piece.coords[1]))
                self.move_piece(target, (final_pos[0] + 1, final_pos[1]), True)
        # Update castling logic
        elif type(piece) is Rook and piece.coords == (7, 7):
            if game.MyGame.is_white:
                self.short_castle = False
            else:
                self.long_castle = False
        # Update castling logic
        elif type(piece) is Rook and piece.coords == (0, 7):
            if game.MyGame.is_white:
                self.long_castle = False
            else:
                self.short_castle = False

        return True
