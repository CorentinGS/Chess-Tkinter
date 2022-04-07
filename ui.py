from tkinter import Frame, BOTH, Canvas, PhotoImage, Event, messagebox

from numpy import ndarray

import const
import game
from engine.engine import MyChessEngine
from pieces import Piece, Empty
from utils.theme import Color

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
        self.legal_moves: list = []
        self.img = None
        self.pack(fill=BOTH, expand=True)
        self.square_size: float = game.MyGame.app_instance.width / const.COLUMNS
        self.canvas: Canvas = Canvas(game.MyGame.app_instance.root,
                                     height=game.MyGame.app_instance.height,
                                     width=game.MyGame.app_instance.width)
        self.color: Color = Color()
        self.winfo_toplevel().title("ChessBoard GUI 1.0")
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

        self.selected_Piece = None

        self.canvas.bind("<Button-1>", self.click)

        self.render_board()

    def display_legal_moves(self, piece, current_column, current_row):
        self.selected_Piece = piece
        self.canvas.create_rectangle(current_column * self.square_size, current_row * self.square_size,
                                     current_column * self.square_size + self.square_size,
                                     current_row * self.square_size + self.square_size, outline="#887CE6",
                                     tags="selected")

        self.legal_moves: list = piece.legal_moves()
        for pos in self.legal_moves:
            x, y = pos
            self.canvas.create_oval(
                x * self.square_size + self.square_size // 2 - self.square_size * 0.2,
                y * self.square_size + self.square_size // 2 - self.square_size * 0.2,
                x * self.square_size + self.square_size // 2 + self.square_size * 0.2,
                y * self.square_size + self.square_size // 2 + self.square_size * 0.2,
                fill="#887CE6",
                outline="", tags="selected"
            )
            self.canvas.tag_raise("piece")

    def click(self, event: Event):
        if not game.MyGame.player_turn:
            return

        if game.MyGame.chess_engine.board.is_game_over():
            game.MyGame.chess_engine.board.result()
            messagebox.showinfo(
                "Game is over",
                f"Checkmate: {game.MyGame.chess_engine.board.result()}"
            )
            game.MyGame.restart_game()

        self.canvas.delete("selected")

        current_column = round(abs(event.x - self.square_size / 2) / self.square_size)
        current_row = round(abs(event.y - self.square_size / 2) / self.square_size)
        piece = Piece.get_piece_at_position((current_column, current_row))

        if type(piece) is not Empty and game.MyGame.is_white is piece.is_white:
            self.display_legal_moves(piece, current_column, current_row)

        elif self.selected_Piece:
            if (current_column, current_row) in self.legal_moves:
                if game.MyGame.chess.move_piece(self.selected_Piece, (current_column, current_row)):
                    game.MyGame.player_turn = False
                    game.MyGame.gui.render_pieces(game.MyGame.chess.board)
                    game.MyGame.app_instance.root.update()

                    if game.MyGame.player_turn is False:
                        game.MyGame.play_engine()

            self.selected_Piece = None
            self.legal_moves = []

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
                    piece = Piece(str(board[y][x])[0] == '1', (x, y), board[y][x])
                    self.draw_piece(piece)

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
