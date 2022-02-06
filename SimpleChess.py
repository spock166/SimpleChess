import Pieces
from Pieces import *

# Default Starting FEN
# Adapted from standard chess FEN
# Gives board setup from rank 6 to rank 1
# Lower case letters are black pieces
# Upper case letters are white pieces
# Don't need to record en passant or castling since we're making SimpleChess
# w indicates white to move, b indicates black to move
# Halfmove clock: Number of halfmoves since last capture or pawn advance, used for fifty-move rule
# Fullmove clock: Updates after black moves.

starting_fen = 'rbqkbr/pppppp/6/6/PPPPPP/RBQKBR w 0 1'

# Define Piece Prototypes
EmptySquare = Piece()
BlackPawn = Piece(piece_name=Names.PAWN, piece_color=Color.BLACK)
WhitePawn = Piece(piece_name=Names.PAWN, piece_color=Color.WHITE)

BlackBishop = Piece(piece_name=Names.BISHOP, piece_color=Color.BLACK)
WhiteBishop = Piece(piece_name=Names.BISHOP, piece_color=Color.WHITE)

BlackRook = Piece(piece_name=Names.ROOK, piece_color=Color.BLACK)
WhiteRook = Piece(piece_name=Names.ROOK, piece_color=Color.WHITE)

BlackKing = Piece(piece_name=Names.KING, piece_color=Color.BLACK)
WhiteKing = Piece(piece_name=Names.KING, piece_color=Color.WHITE)

BlackQueen = Piece(piece_name=Names.QUEEN, piece_color=Color.BLACK)
WhiteQueen = Piece(piece_name=Names.QUEEN, piece_color=Color.WHITE)


def ReadFEN(FEN_string: str):
    """
    Reads a given string FEN_string that contains FEN notation for SimpleChess
    """

    positions, current_player, halfturns, fullturns = starting_fen.split(" ")

    rows = positions.split("/")

    new_board = [[],[],[],[],[],[]]

    for r in range(len(rows)):
        r_prime = len(rows)-1-r
        for c in rows[r]:
            if c.isnumeric():
                for i in range(int(c)):
                    new_board[r_prime].append(EmptySquare)
            elif c == 'p':
                new_board[r_prime].append(BlackPawn)
            elif c == 'b':
                new_board[r_prime].append(BlackBishop)
            elif c == 'r':
                new_board[r_prime].append(BlackRook)
            elif c == 'k':
                new_board[r_prime].append(BlackKing)
            elif c == 'q':
                new_board[r_prime].append(BlackQueen)
            elif c == 'P':
                new_board[r_prime].append(WhitePawn)
            elif c == 'B':
                new_board[r_prime].append(WhiteBishop)
            elif c == 'R':
                new_board[r_prime].append(WhiteRook)
            elif c == 'K':
                new_board[r_prime].append(WhiteKing)
            elif c == 'Q':
                new_board[r_prime].append(WhiteQueen)


    if current_player == 'w':
        player = Color.WHITE
    elif current_player == 'b':
        player = Color.BLACK
    else:
        player = Color.NONE

    return new_board, player, int(halfturns), int(fullturns)

def DisplayBoard(board):
    print("  123456")
    print("  ======")
    for r in range(len(board)-1,-1,-1):
        row = str(r+1) + "|"
        for c in board[r]:
            row += str(c)
        print(row)

def isValidMove(rp,cp,rd,cd,b):
    selected_piece = b[rp][cp]

    return True

def Move(rp,cp,rd,cd,b):
    selected_piece = b[rp][cp]
    pass

if __name__ == "__main__":
    board, current_player, halfturns, fullturns = ReadFEN(starting_fen)


    DisplayBoard(board)

    while(True):
        if(halfturns >= 50):
            print(f"Game is a draw by 50 move rule.")
            break


        print(f"It is move {fullturns} with {current_player} to play.")

        valid_selection = False
        while(not valid_selection):
            square = input(f"Pick a square with a {current_player} piece on it (input as two digits rc):")
            r_piece, c_piece = int(square[0])-1, int(square[1])-1

            if board[r_piece][c_piece].piece_color != current_player:
                pass
            else:
                valid_selection = True

        valid_selection = False
        while(not valid_selection):
            square = input(f"Pick a square to move the {board[r_piece][c_piece]} (input as two digits rc):")
            r_dest, c_dest = int(square[0]) - 1, int(square[1]) - 1
            if isValidMove(r_piece,c_piece,r_dest,c_dest,board):
                valid_selection = True

        Move(r_piece,c_piece,r_dest,c_dest,board)

        if current_player == Color.BLACK:
            current_player = Color.WHITE
            fullturns += 1
        else:
            current_player = Color.BLACK
