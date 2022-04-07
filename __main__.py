from time import sleep

import const
from callback import update_tkinter_chess_board
from numpy_chess import ChessGame

from engine.engine import MyChessEngine
from pieces import Piece

from tkinstance import AppInstance
from ui import GUI

WIDTH: int = 1000
HEIGHT: int = 1000


def main():
    ChessGame.is_white = True
    ChessGame.init_board()

    MyChessEngine.__init__()

    AppInstance.set_dimensions(WIDTH, HEIGHT)
    GUI.__init__()
    GUI.render_board()

    update_tkinter_chess_board()

    AppInstance.root.mainloop()


main()
