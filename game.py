import const
import sys
import ui
from engine.engine import ChessEngine
from numpy_chess import Chess
from pieces import Piece
from tkinstance import TkInstance

# Tkinter const
WIDTH: int = 1000
HEIGHT: int = 1000


# Game class
class Game:
    chess: Chess
    chess_engine: ChessEngine
    app_instance: TkInstance
    gui: ui.UI

    def __init__(self, is_white: bool = True):
        """
        :param is_white: is player white
        """
        self.is_white: bool = is_white
        self.player_turn: bool = is_white

        self.game_state: int = const.GAME_IN_PROGRESS

    def start_game(self):
        """
        Start the game
        """

        # Setup logic
        self.chess = Chess()
        self.chess.board = self.chess.init_board(self.is_white)

        # Start chess engine
        self.chess_engine = ChessEngine()

        # Tkinter instance
        self.app_instance = TkInstance()
        self.app_instance.set_dimensions(WIDTH, HEIGHT)
        self.app_instance.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Chess GUI
        self.gui = ui.UI()

        # Render GUI
        self.gui.render_board()
        self.gui.render_pieces(self.chess.board)

        # Makes engine plays the first move if player is black
        if self.is_white is False:
            self.play_engine()

        # Main loooooooooooooooooooooooooooooooooooooooooooop
        self.app_instance.root.mainloop()

    def restart_game(self):
        """
        Restart game
        """
        # Change color
        # self.is_white = not self.is_white # Was used as testing but it should be asked to the user

        # Init board
        self.chess_engine.init_board()
        # Delete old structs
        del self.chess
        # Chess logic
        self.chess = Chess()
        self.chess.board = self.chess.init_board(self.is_white)
        # Render pieces
        self.gui.render_pieces(self.chess.board)

        # Makes engine plays the first move if player is black
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
