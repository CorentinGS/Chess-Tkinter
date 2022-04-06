from time import sleep

from callback import update_tkinter_chess_board
from chess import ChessGame

from tkinstance import AppInstance
from ui import GUI

WIDTH: int = 1000
HEIGHT: int = 1000


def main():
    ChessGame.is_white = True
    ChessGame.init_board()

    AppInstance.set_dimensions(WIDTH, HEIGHT)
    GUI.__init__()
    GUI.render_board()

    update_tkinter_chess_board()

    AppInstance.root.mainloop()


main()
