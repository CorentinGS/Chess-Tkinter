from tkinter import Tk


class TkInstance:
    def __init__(self, width: int = 0, height: int = 0):
        self.root: Tk = Tk()
        self.width: int = width
        self.height: int = height

    def set_dimensions(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

