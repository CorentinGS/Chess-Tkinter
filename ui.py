from tkinter import Frame, BOTH, Canvas, PhotoImage

from numpy import ndarray

import const
from chess import ChessGame
from pieces import Piece
from theme import Color
from tkinstance import AppInstance

pieces_images_dic = {}


class UI(Frame):

    @property
    def square_size(self):
        return self._square_size

    @square_size.setter
    def square_size(self, value):
        self._square_size = value

    def __init__(self):
        super().__init__()
        self.img = None
        self.pack(fill=BOTH, expand=True)
        self.square_size: float = AppInstance.width / const.COLUMNS
        self.canvas: Canvas = Canvas(AppInstance.root, height=AppInstance.height, width=AppInstance.width)
        self.color: Color = Color()
        self.winfo_toplevel().title("ChessBoard")
        self.winfo_toplevel().resizable(False, False)
        self.pieces_images_name = {
            const.PIECE_K_W: "king_white",
            const.PIECE_Q_W: "queen_white",
            const.PIECE_R_W: "rook_white",
            const.PIECE_N_W: "knight_white",
            const.PIECE_B_W: "bishop_white",
            const.PIECE_P_W: "pawn_white",
            const.PIECE_K_B: "king_black",
            const.PIECE_Q_B: "queen_black",
            const.PIECE_R_B: "rook_black",
            const.PIECE_N_B: "knight_black",
            const.PIECE_B_B: "bishop_black",
            const.PIECE_P_B: "pawn_black",
        }
        self.pieces = []

        self.render_board()

    def piece_to_img_name(self, piece: int) -> PhotoImage:
        if piece not in pieces_images_dic:
            pieces_images_dic[piece] = PhotoImage(file=f"./images/{self.pieces_images_name[piece]}.png")

            pieces_images_dic[piece] = pieces_images_dic[piece].subsample(
                int(pieces_images_dic[piece].width() // self.square_size),
                int(pieces_images_dic[piece].height() // self.square_size)
            )

        return pieces_images_dic[piece]

    def render_pieces(self, board: ndarray):
        self.canvas.delete("piece")

        for y in range(const.COLUMNS):
            for x in range(const.ROWS):
                if board[y][x] != 0:
                    self.draw_piece(Piece(board[y][x], (x, y)))

    def draw_piece(self, piece: Piece):
        self.canvas.create_image(piece.coords[0] * self.square_size + self.square_size // 2,
                                 piece.coords[1] * self.square_size + self.square_size // 2,
                                 image=self.piece_to_img_name(piece.piece_type), tag="piece")

    def render_board(self):

        self.canvas.delete("all")

        self.draw_grid()

        self.canvas.pack(side="top", anchor="center")

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


GUI = UI()
