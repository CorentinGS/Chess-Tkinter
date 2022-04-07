from numpy_chess import ChessGame
from ui import GUI


def update_tkinter_chess_board():
    GUI.render_pieces(ChessGame.board)

