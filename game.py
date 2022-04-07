import const
from engine.engine import ChessEngine
from numpy_chess import Chess
from pieces import Piece
from tkinstance import TkInstance
import ui

WIDTH: int = 1000
HEIGHT: int = 1000


class Game:
    chess: Chess
    chess_engine: ChessEngine
    app_instance: TkInstance
    gui: ui.UI

    def __init__(self, is_white: bool = True):
        self.is_white: bool = is_white
        self.player_turn: bool = is_white

        self.game_state: int = const.GAME_IN_PROGRESS

    def start_game(self):
        self.chess = Chess()
        self.chess.board = Chess.init_board(self.chess)
        self.chess_engine = ChessEngine()

        self.app_instance = TkInstance()
        self.app_instance.set_dimensions(WIDTH, HEIGHT)

        self.gui = ui.UI()
        self.gui.render_board()
        self.gui.render_pieces(self.chess.board)

        self.app_instance.root.mainloop()

    def play_engine(self):
        pos1, pos2 = self.chess_engine.play_bot_move()
        if self.chess.move_piece(Piece.get_piece_at_position(pos1), pos2):
            self.player_turn = True


MyGame = Game()
