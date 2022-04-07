import const


class Piece:

    def __init__(self, piece: int, coords: tuple[int, int]):
        self.piece_type: int = piece
        self.coords: tuple[int, int] = coords

    def is_white(self) -> bool:
        return str(self.piece_type)[0] == '1'

    def is_empty(self) -> bool:
        return self.piece_type == const.PIECE_NONE

    def is_rook(self) -> bool:
        return str(self.piece_type)[1] == '2'

    def is_queen(self) -> bool:
        return str(self.piece_type)[1] == '1'

    def is_king(self) -> bool:
        return str(self.piece_type)[1] == '0'

    def is_bishop(self) -> bool:
        return str(self.piece_type)[1] == '4'

    def is_knight(self) -> bool:
        return str(self.piece_type)[1] == '3'

    def is_pawn(self) -> bool:
        return str(self.piece_type)[1] == '5'