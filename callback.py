import numpy as np

from chess import Chess, ChessGame
from ui import UI, GUI


def update_tkinter_chess_board():
    GUI.render_pieces(ChessGame.board)


