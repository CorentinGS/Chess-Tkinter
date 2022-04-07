import chess
import chess.engine

import game

fileDict = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


def get_uci(init: tuple[int, int], end: tuple[int, int]) -> str:
    is_white = game.MyGame.is_white
    file1 = fileDict[init[0]] if is_white else fileDict[7 - init[0]]
    file2 = fileDict[end[0]] if is_white else fileDict[7 - end[0]]
    row1 = init[1] + 1 if not is_white else 7 - init[1] + 1
    row2 = end[1] + 1 if not is_white else 7 - end[1] + 1

    return f"{file1}{row1}{file2}{row2}"


def uci_to_numpy(uci: str) -> (tuple[int, int], tuple[int, int]):
    is_white = game.MyGame.is_white
    x1 = fileDict.index(uci[0]) if is_white else 7 - fileDict.index(uci[0])
    x2 = fileDict.index(uci[2]) if is_white else 7 - fileDict.index(uci[2])
    y1 = int(uci[1]) - 1 if  not is_white else 7 - int(uci[1]) + 1
    y2 = int(uci[3]) - 1 if  not is_white else 7 - int(uci[3]) + 1
    return (x1, y1), (x2, y2)


class ChessEngine:
    def __init__(self):
        self.board: chess.Board = chess.Board(chess.STARTING_FEN)
        self.engine = chess.engine.SimpleEngine.popen_uci(
            r"./engine/stockfish_14.1_linux_x64")

    def init_board(self):
        self.board: chess.Board = chess.Board(chess.STARTING_FEN)

    def get_engine_move(self):
        pvmove = None
        with self.engine.analysis(self.board, chess.engine.Limit(time=2)) as analysis:
            for info in analysis:
                if info.get("pv") is not None:
                    pvmove = info.get('pv')[0]

        pvmove = analysis.info.get('pv')[0]
        return pvmove

    def play_move(self, uci: str):
        move = chess.Move.from_uci(uci)
        self.board.push(move)

    def play_bot_move(self) -> [tuple[int, int], tuple[int, int]]:
        pvmove = self.get_engine_move()
        self.board.push_uci(str(pvmove))
        pos1, pos2 = uci_to_numpy(str(pvmove))
        return pos1, pos2


MyChessEngine = ChessEngine()
