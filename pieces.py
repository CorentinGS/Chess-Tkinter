class Piece:

    def __init__(self, piece: int, coords: tuple[int, int]):
        self.piece_type: int = piece
        self.coords:  tuple[int, int] = coords
