from tkinter import Frame, BOTH, Canvas, PhotoImage, Event, messagebox

from numpy import ndarray

import const
import game
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
        # Init
        super().__init__()
        # Default values
        self.legal_moves: list = []
        self.img = None
        self.pack(fill=BOTH, expand=True)
        # Compute square size
        self.square_size: float = game.MyGame.app_instance.width / const.COLUMNS
        # Setup canvas
        self.canvas: Canvas = Canvas(game.MyGame.app_instance.root,
                                     height=game.MyGame.app_instance.height,
                                     width=game.MyGame.app_instance.width)
        # Color theme
        self.color: Color = Color()
        # Win settings
        self.winfo_toplevel().title("ChessBoard GUI 1.0")
        self.winfo_toplevel().resizable(False, False)
        # Images name
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
        # Bind events
        self.canvas.bind("<Button-1>", self.click)

        # Render board
        self.render_board()

    def display_legal_moves(self, piece, current_column: int, current_row: int):
        """
        Display legals moves on board
        """
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
        """
        On Click Event
        """

        # Makes sure it's player turn
        if not game.MyGame.player_turn:
            return

        # Check for game over
        if game.MyGame.chess_engine.board.is_game_over():
            # Display result
            game.MyGame.chess_engine.board.result()
            messagebox.showinfo(
                "Game is over",
                f"Checkmate: {game.MyGame.chess_engine.board.result()}"
            )
            # Restart game
            game.MyGame.restart_game()

        # Delete canvas using tag
        self.canvas.delete("selected")

        # Get current column, row and piece
        current_column = round(abs(event.x - self.square_size / 2) / self.square_size)
        current_row = round(abs(event.y - self.square_size / 2) / self.square_size)
        piece = Piece.get_piece_at_position((current_column, current_row))

        # Check if piece is empty
        if type(piece) is not Empty and game.MyGame.is_white is piece.is_white:
            # Display legal moves of selected piece
            self.display_legal_moves(piece, current_column, current_row)

        # if a piece is selected
        elif self.selected_Piece:
            # Check if it's a legal move
            if (current_column, current_row) in self.legal_moves:
                # Move piece
                if game.MyGame.chess.move_piece(self.selected_Piece, (current_column, current_row)):
                    game.MyGame.player_turn = False  # Change turn
                    game.MyGame.gui.render_pieces(game.MyGame.chess.board)  # Render board
                    # Updates the canvas to prevent engine from making the GUI lagging while analyzing the game.
                    game.MyGame.app_instance.root.update()

                    if game.MyGame.player_turn is False:
                        # Play engine move
                        game.MyGame.play_engine()
            # Reset values
            self.selected_Piece = None
            self.legal_moves = []

    def piece_to_img_name(self, piece: int) -> PhotoImage:
        """
        Returns the img for a piece
        :param piece: Piece to get the img
        """
        # Caching image
        if piece not in pieces_images_dic:
            pieces_images_dic[piece] = PhotoImage(file=f"./images/{self.pieces_images_name[piece]}.png")

            pieces_images_dic[piece] = pieces_images_dic[piece].subsample(
                int(pieces_images_dic[piece].width() // self.square_size),
                int(pieces_images_dic[piece].height() // self.square_size)
            )

        return pieces_images_dic[piece]

    def render_pieces(self, board: ndarray):
        self.canvas.delete("piece")

        # Render all pieces on the board
        for y in range(const.COLUMNS):
            for x in range(const.ROWS):
                if board[y][x] != 0:
                    piece = Piece(str(board[y][x])[0] == '1', (x, y), board[y][x])
                    self.draw_piece(piece)

    def draw_piece(self, piece: Piece):
        # Draw a piece
        self.canvas.create_image(piece.coords[0] * self.square_size + self.square_size // 2,
                                 piece.coords[1] * self.square_size + self.square_size // 2,
                                 image=self.piece_to_img_name(piece.piece_type), tag="piece")

    def render_board(self):
        # Render board

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
