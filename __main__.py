from tkinstance import AppInstance
from ui import UI

WIDTH: int = 1000
HEIGHT: int = 1000


def main():
    AppInstance.set_dimensions(WIDTH, HEIGHT)
    UI()
    AppInstance.root.mainloop()


main()
