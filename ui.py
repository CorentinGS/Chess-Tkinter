from tkinter import Frame, BOTH, Canvas

import const
from theme import Color
from tkinstance import AppInstance


class UI(Frame):

    @property
    def square_size(self):
        return self._square_size

    @square_size.setter
    def square_size(self, value):
        self._square_size = value

    def __init__(self):
        super().__init__()
        self.pack(fill=BOTH, expand=True)
        self.square_size: float = AppInstance.width / const.COLUMNS
        self.canvas: Canvas = Canvas(AppInstance.root, height=AppInstance.height, width=AppInstance.width)
        self.color: Color = Color()
        self.winfo_toplevel().title("ChessBoard")
        self.winfo_toplevel().resizable(False, False)

        self.render_board()

    def render_board(self):

        self.canvas.delete("all")

        self.draw_grid()

        self.canvas.pack(side="top", anchor="center", fill=BOTH, expand=True, )

    def draw_grid(self):
        for y in range(const.ROWS):
            for x in range(const.COLUMNS):
                if (x - y) % 2 == 0:
                    current_color = self.color.white
                else:
                    current_color = self.color.black

                self.canvas.create_rectangle(
                    x * self.square_size,
                    y * self.square_size,
                    x * self.square_size + self.square_size,
                    y * self.square_size + self.square_size,
                    fill=current_color,
                    outline="",
                )
