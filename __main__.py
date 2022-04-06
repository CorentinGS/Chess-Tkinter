from callback import update_tkinter_chess_board
from chess import ChessGame

from tkinstance import AppInstance
from ui import UI, GUI

WIDTH: int = 1000
HEIGHT: int = 1000


def main():
    ChessGame.init_board()

    AppInstance.set_dimensions(WIDTH, HEIGHT)
    GUI.__init__()
    GUI.render_board()

    update_tkinter_chess_board()

    AppInstance.root.mainloop()


main()
