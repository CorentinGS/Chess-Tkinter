import const
import sys
import ui
from engine.engine import ChessEngine
from numpy_chess import Chess
from pieces import Piece
from tkinstance import TkInstance

WIDTH: int = 1000
HEIGHT: int = 1000


class Game:
    chess: Chess
    chess_engine: ChessEngine
    app_instance: TkInstance
    gui: ui.UI

    def __init__(self, is_white: bool = True):
        """
        :param is player white:
        """
        self.is_white: bool = is_white
        self.player_turn: bool = is_white

        self.game_state: int = const.GAME_IN_PROGRESS

    def start_game(self):
        """
        Start the game
        """
        self.chess = Chess()
        self.chess.board = self.chess.init_board(self.is_white)
        self.chess_engine = ChessEngine()

        self.app_instance = TkInstance()
        self.app_instance.set_dimensions(WIDTH, HEIGHT)
        self.app_instance.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.gui = ui.UI()

        self.gui.render_board()
        self.gui.render_pieces(self.chess.board)

        if self.is_white is False:
            self.play_engine()

        self.app_instance.root.mainloop()

    def restart_game(self):
        self.chess_engine.init_board()
        del self.chess
        self.chess = Chess()
        self.chess.board = self.chess.init_board(self.is_white)
        self.is_white = not self.is_white
        self.gui.render_pieces(self.chess.board)

        if self.is_white is False:
            self.play_engine()

    def on_closing(self):
        self.chess_engine.engine.close()
        self.app_instance.root.destroy()
        sys.exit()

    def play_engine(self):
        """
        Play engine move
        """
        pos1, pos2 = self.chess_engine.play_bot_move()
        if self.chess.move_piece(Piece.get_piece_at_position(pos1), pos2, True):
            self.player_turn = True


MyGame = Game()
