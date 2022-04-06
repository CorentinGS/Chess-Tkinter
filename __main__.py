from chess import ChessGame
from tkinstance import AppInstance
from ui import UI

WIDTH: int = 1000
HEIGHT: int = 1000


def main():

    print(ChessGame.board)

    AppInstance.set_dimensions(WIDTH, HEIGHT)
    UI()
    AppInstance.root.mainloop()


main()
