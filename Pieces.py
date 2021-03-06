from enum import Enum, auto


# Enum to keep track of piece colors
class Color(Enum):
    BLACK = auto()
    WHITE = auto()
    NONE = auto()


# Enum to keep track of piece names.
class Names(Enum):
    KING = auto()
    QUEEN = auto()
    BISHOP = auto()
    ROOK = auto()
    PAWN = auto()
    EMPTY = auto()


class Piece:
    def __init__(self, piece_name=Names.EMPTY, piece_color=Color.NONE, piece_value = 0):
        self.piece_name = piece_name
        self.piece_color = piece_color
        self.piece_value = piece_value

        if piece_name == Names.EMPTY:
            self.piece_char = '_'
        elif piece_name == Names.KING:
            self.piece_char = 'k'
        elif piece_name == Names.QUEEN:
            self.piece_char = 'q'
        elif piece_name == Names.BISHOP:
            self.piece_char = 'b'
        elif piece_name == Names.ROOK:
            self.piece_char = 'r'
        elif piece_name == Names.PAWN:
            self.piece_char = 'p'
        else:
            self.piece_char = '?'

    def __str__(self):
        if self.piece_color == Color.BLACK:
            return str.lower(self.piece_char)
        elif self.piece_color == Color.WHITE:
            return str.upper(self.piece_char)
        else:
            return self.piece_char
