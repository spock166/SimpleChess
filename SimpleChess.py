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
    Reads a given string FEN_string that contains FEN notation for SimpleChess.
    """

    # Parse FEN_string.  Assumes a properly formatted string.
    # TODO: Validate the string
    positions, current_player, halfturns, fullturns = starting_fen.split(" ")

    rows = positions.split("/")

    new_board = [[], [], [], [], [], []]

    # Populate the new board
    for r in range(len(rows)):
        r_prime = len(rows) - 1 - r
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

    # Set current player
    if current_player == 'w':
        player = Color.WHITE
    elif current_player == 'b':
        player = Color.BLACK
    else:
        player = Color.NONE

    # Return relevant game information
    return new_board, player, int(halfturns), int(fullturns)


def DisplayBoard(current_board):
    print("  ======")
    for r in range(len(current_board) - 1, -1, -1):
        row = str(r + 1) + "|"
        for c in current_board[r]:
            row += str(c)
        print(row)
    print("  ======")
    print("  abcdef")


def isValidPawnMove(rp,cp,rd,cd,b):
    selected_piece = b[rp][cp]
    piece_color = selected_piece.piece_color

    # Unlike in normal chess pawns always move one square at a time.
    # Double moving the first move doesn't work as well on a 6x6 board.
    # A double move variant could be fun to try in the future.

    if piece_color == Color.WHITE:
        forward = 1
    elif piece_color == Color.BLACK:
        forward = -1

    if cp == cd and rp + forward == rd and b[rd][cd].piece_color == Color.NONE:
        return True
    elif abs(cp - cd) == 1 and rp + forward == rd:
        if piece_color == Color.WHITE and b[rd][cd].piece_color == Color.BLACK:
            return True
        elif piece_color == Color.BLACK and b[rd][cd].piece_color == Color.WHITE:
            return True
        return False

    return False


def isValidBishopMove(rp,cp,rd,cd,b):
    selected_piece = b[rp][cp]
    piece_color = selected_piece.piece_color

    # First check if move is diagonal.
    if abs(cp - cd) != abs(rp - rd) or (cp == cd and rp == rd):
        print(cp - cd, rp - rd)
        return False

    # Move right?
    if 0 < cd - cp:
        col_adj = 1
    else:
        col_adj = -1

    # Move up?
    if 0 < rd - rp:
        row_adj = 1
    else:
        row_adj = -1

    # Check to see if there's a piece blocking the path.
    for i in range(1, abs(cp - cd) + 1):
        # We don't mind if the final square contains an enemy.
        if i == abs(cp - cd):
            if b[rp + (i * row_adj)][cp + (i * col_adj)].piece_color == piece_color:
                return False
        else:
            if b[rp + (i * row_adj)][cp + (i * col_adj)].piece_color != Color.NONE:
                # We've run into a piece along our path.  This is a problem.
                return False
    return True


def isValidRookMove(rp, cp, rd, cd, b):
    selected_piece = b[rp][cp]
    piece_color = selected_piece.piece_color

    # Which direction are we moving?
    if cp - cd == 0 and rp - rd == 0:
        # We need to move to a new square
        return False
    elif cp - cd == 0:
        # We're moving along a file
        if 0 < rd - rp:
            row_adj = 1
        else:
            row_adj = -1

        for i in range(1, abs(rp - rd) + 1):
            if i == abs(rp - rd):
                if b[rp + (i * row_adj)][cp].piece_color == piece_color:
                    return False
            else:
                if b[rp + (i * row_adj)][cp].piece_color != Color.NONE:
                    return False
        return True
    elif rp - rd == 0:
        # We're moving along a rank.
        if 0 < cd - cp:
            col_adj = 1
        else:
            col_adj = -1

        for i in range(1, abs(cp - cd) + 1):
            if i == abs(cp - cd):
                if b[rp][cp + (i * col_adj)].piece_color == piece_color:
                    return False
            else:
                if b[rp][cp + (i * col_adj)].piece_color != Color.NONE:
                    return False
        return True
    else:
        # What the fuck are we doing not going along a rank or file?
        return False


def isValidKingMove(rp, cp, rd, cd, b):
    # Moving left/right or up/down
    if (rp == rd and abs(cp-cd) == 1) or (cp == cd and abs(rp-rd) == 1):
        return isValidRookMove(rp, cp, rd, cd, b)
    elif abs(cp-cd) == 1 and abs(rp-rd) == 1:
        return isValidBishopMove(rp, cp, rd, cd, b)
    else:
        return False


def isValidMove(rp, cp, rd, cd, b):
    """
    Checks if it is possible for the piece at rp,cp to move to rd,cd.
    :param rp:
    :param cp:
    :param rd:
    :param cd:
    :param b:
    :return: Returns True if move is valid, False otherwise.
    """

    if cp < 0 or cp > 5 or rd < 0 or rd > 5 or rp < 0 or rp > 5 or cd < 0 or cd > 5:
        return False

    selected_piece = b[rp][cp]

    if selected_piece.piece_name == Names.PAWN:
        return isValidPawnMove(rp, cp, rd, cd, b)

    if selected_piece.piece_name == Names.BISHOP:
        return isValidBishopMove(rp, cp, rd, cd, b)

    if selected_piece.piece_name == Names.ROOK:
        return isValidRookMove(rp, cp, rd, cd, b)

    if selected_piece.piece_name == Names.QUEEN:
        return isValidBishopMove(rp, cp, rd, cd, b) or isValidRookMove(rp, cp, rd, cd, b)

    if selected_piece.piece_name == Names.KING:
        return isValidKingMove(rp, cp, rd, cd, b)

    return False


def Move(rp, cp, rd, cd, b):
    """
    Moves piece located at rp,cp to rd,cd.  Use isValidMove to ensure move is legal
    :param rp:
    :param cp:
    :param rd:
    :param cd:
    :param b:
    :return: Returns True if there was a pawn move or a capture.
    """

    pawn_or_capture = False
    game_over = False

    selected_piece = b[rp][cp]
    target_piece = b[rd][cd]

    if target_piece.piece_name == Names.KING:
        return True, True

    # Check if a pawn move or capture has been done.  Necessary for 50 move rule.
    if selected_piece.piece_name == Names.PAWN or (
            selected_piece.piece_color == Color.BLACK and target_piece.piece_color == Color.WHITE) or (
            selected_piece.piece_color == Color.WHITE and target_piece.piece_color == Color.BLACK):
        pawn_or_capture = True

    # Update board
    b[rd][cd] = selected_piece
    b[rp][cp] = EmptySquare

    if selected_piece.piece_name == Names.PAWN:
        if selected_piece.piece_color == Color.WHITE and rd == 5:
            b[rd][cd] = WhiteQueen
        elif selected_piece.piece_color == Color.BLACK and rd == 0:
            b[rd][cd] = BlackQueen

    return pawn_or_capture, game_over


def make_move(current_board, player):
    game_over = False
    # Loop until player makes a valid move
    player_has_moved = False

    while not player_has_moved:
        # Select piece to move
        valid_selection = False
        while not valid_selection:
            square = input(f"Pick a square with a {player} piece on it (example a4):")
            try:
                r_piece = int(square[1]) - 1
                col = square[0]
                if col == 'a':
                    c_piece = 0
                elif col == 'b':
                    c_piece = 1
                elif col == 'c':
                    c_piece = 2
                elif col == 'd':
                    c_piece = 3
                elif col == 'e':
                    c_piece = 4
                elif col == 'f':
                    c_piece = 5
                else:
                    c_piece = -1

                if current_board[r_piece][c_piece].piece_color != player:
                    pass
                else:
                    valid_selection = True
            except IndexError:
                pass

        # Select where to move the selected piece
        valid_selection = False
        while not valid_selection:
            square = input(
                f"Pick a square to move the {board[r_piece][c_piece]} (enter 'skip' if wrong piece was selected):")

            # If player makes a mistake they can restart the selection process
            if square.lower() == 'skip':
                valid_selection = True
                break

            try:
                r_dest = int(square[1]) - 1

                col = square[0]
                if col == 'a':
                    c_dest = 0
                elif col == 'b':
                    c_dest = 1
                elif col == 'c':
                    c_dest = 2
                elif col == 'd':
                    c_dest = 3
                elif col == 'e':
                    c_dest = 4
                elif col == 'f':
                    c_dest = 5
                else:
                    c_dest = -1

                # If move is valid, then make the move
                if isValidMove(r_piece, c_piece, r_dest, c_dest, current_board):
                    pawn_or_capture, game_over = Move(r_piece, c_piece, r_dest, c_dest, current_board)
                    valid_selection = True
                    player_has_moved = True

            except IndexError:
                pass

    return pawn_or_capture, game_over


if __name__ == "__main__":
    board, current_player, halfturns, fullturns = ReadFEN(starting_fen)

    while True:
        # 50 move rule implemented from chess.
        if halfturns >= 50:
            print(f"Game is a draw by 50 move rule.")
            break

        DisplayBoard(board)

        print(f"It is move {fullturns} with {current_player} to play.")

        # Update half move counter
        pawn_move, end_game = make_move(board, current_player)

        if end_game:
            print("Game Over!")
            break

        if pawn_move:
            halfturns = 0
        else:
            halfturns += 1

        # Update whose turn it is
        if current_player == Color.BLACK:
            current_player = Color.WHITE
            fullturns += 1
        else:
            current_player = Color.BLACK
