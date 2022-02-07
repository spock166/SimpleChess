from Pieces import *

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
    positions, current_player, halfturns, fullturns = FEN_string.split(" ")

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


def DisplayBoard(board):
    print("  _____________")
    for r in range(len(board) - 1, -1, -1):
        row = str(r + 1) + " |"
        for c in board[r]:
            row += str(c) + "|"
        print(row)
    print("   a b c d e f")


def isValidPawnMove(piece_row, piece_col, dest_row, dest_col, board):
    selected_piece = board[piece_row][piece_col]
    piece_color = selected_piece.piece_color

    # Unlike in normal chess pawns always move one square at a time.
    # Double moving the first move doesn't work as well on a 6x6 board.
    # A double move variant could be fun to try in the future.

    if piece_color == Color.WHITE:
        forward = 1
    elif piece_color == Color.BLACK:
        forward = -1

    if piece_col == dest_col and piece_row + forward == dest_row and board[dest_row][dest_col].piece_color == Color.NONE:
        return True
    elif abs(piece_col - dest_col) == 1 and piece_row + forward == dest_row:
        if piece_color == Color.WHITE and board[dest_row][dest_col].piece_color == Color.BLACK:
            return True
        elif piece_color == Color.BLACK and board[dest_row][dest_col].piece_color == Color.WHITE:
            return True
        return False

    return False


def isValidBishopMove(piece_row, piece_col, dest_row, dest_col, board):
    selected_piece = board[piece_row][piece_col]
    piece_color = selected_piece.piece_color

    # First check if move is diagonal.
    if abs(piece_col - dest_col) != abs(piece_row - dest_row) or (piece_col == dest_col and piece_row == dest_row):
        return False

    # Move right?
    if 0 < dest_col - piece_col:
        col_adj = 1
    else:
        col_adj = -1

    # Move up?
    if 0 < dest_row - piece_row:
        row_adj = 1
    else:
        row_adj = -1

    # Check to see if there's a piece blocking the path.
    for i in range(1, abs(piece_col - dest_col) + 1):
        # We don't mind if the final square contains an enemy.
        if i == abs(piece_col - dest_col):
            if board[piece_row + (i * row_adj)][piece_col + (i * col_adj)].piece_color == piece_color:
                return False
        else:
            if board[piece_row + (i * row_adj)][piece_col + (i * col_adj)].piece_color != Color.NONE:
                # We've run into a piece along our path.  This is a problem.
                return False
    return True


def isValidRookMove(piece_row, piece_col, dest_row, dest_col, board):
    selected_piece = board[piece_row][piece_col]
    piece_color = selected_piece.piece_color

    # Which direction are we moving?
    if piece_col - dest_col == 0 and piece_row - dest_row == 0:
        # We need to move to a new square
        return False
    elif piece_col - dest_col == 0:
        # We're moving along a file
        if 0 < dest_row - piece_row:
            row_adj = 1
        else:
            row_adj = -1

        for i in range(1, abs(piece_row - dest_row) + 1):
            if i == abs(piece_row - dest_row):
                if board[piece_row + (i * row_adj)][piece_col].piece_color == piece_color:
                    return False
            else:
                if board[piece_row + (i * row_adj)][piece_col].piece_color != Color.NONE:
                    return False
        return True
    elif piece_row - dest_row == 0:
        # We're moving along a rank.
        if 0 < dest_col - piece_col:
            col_adj = 1
        else:
            col_adj = -1

        for i in range(1, abs(piece_col - dest_col) + 1):
            if i == abs(piece_col - dest_col):
                if board[piece_row][piece_col + (i * col_adj)].piece_color == piece_color:
                    return False
            else:
                if board[piece_row][piece_col + (i * col_adj)].piece_color != Color.NONE:
                    return False
        return True
    else:
        # What the fuck are we doing not going along a rank or file?
        return False


def isValidKingMove(piece_row, piece_col, dest_row, dest_col, board):
    # Moving left/right or up/down
    if (piece_row == dest_row and abs(piece_col - dest_col) == 1) or (piece_col == dest_col and abs(piece_row - dest_row) == 1):
        return isValidRookMove(piece_row, piece_col, dest_row, dest_col, board)
    elif abs(piece_col - dest_col) == 1 and abs(piece_row - dest_row) == 1:
        return isValidBishopMove(piece_row, piece_col, dest_row, dest_col, board)
    else:
        return False


def isValidMove(piece_row, piece_col, dest_row, dest_col, board):
    """
    Checks if it is possible for the piece at rp,cp to move to rd,cd.
    :param piece_row:
    :param piece_col:
    :param dest_row:
    :param dest_col:
    :param board:
    :return: Returns True if move is valid, False otherwise.
    """

    if piece_col < 0 or piece_col > 5 or dest_row < 0 or dest_row > 5 or piece_row < 0 or piece_row > 5 or dest_col < 0 or dest_col > 5:
        return False

    selected_piece = board[piece_row][piece_col]

    if selected_piece.piece_name == Names.PAWN:
        return isValidPawnMove(piece_row, piece_col, dest_row, dest_col, board)

    if selected_piece.piece_name == Names.BISHOP:
        return isValidBishopMove(piece_row, piece_col, dest_row, dest_col, board)

    if selected_piece.piece_name == Names.ROOK:
        return isValidRookMove(piece_row, piece_col, dest_row, dest_col, board)

    if selected_piece.piece_name == Names.QUEEN:
        return isValidBishopMove(piece_row, piece_col, dest_row, dest_col, board) or isValidRookMove(piece_row, piece_col, dest_row, dest_col, board)

    if selected_piece.piece_name == Names.KING:
        return isValidKingMove(piece_row, piece_col, dest_row, dest_col, board)

    return False

def validMoves(board, player_color):
    valid_moves = []
    for piece_row in range(len(board)):
        for piece_col in range(len(board[piece_row])):
            if board[piece_row][piece_col].piece_color == player_color:
                for dest_row in range(len(board)):
                    for dest_col in range(len(board[dest_row])):
                        if isValidMove(piece_row, piece_col, dest_row, dest_col, board):
                            valid_moves.append([piece_row,piece_col,dest_row,dest_col])

    return valid_moves

def Move(piece_row, piece_col, dest_row, dest_col, board):
    """
    Moves piece located at rp,cp to rd,cd.  Use isValidMove to ensure move is legal
    :param piece_row:
    :param piece_col:
    :param dest_row:
    :param dest_col:
    :param board:
    :return: Returns True if there was a pawn move or a capture.
    """

    pawn_or_capture = False
    game_over = False

    selected_piece = board[piece_row][piece_col]
    target_piece = board[dest_row][dest_col]

    if target_piece.piece_name == Names.KING:
        return True, True

    # Check if a pawn move or capture has been done.  Necessary for 50 move rule.
    if selected_piece.piece_name == Names.PAWN or (
            selected_piece.piece_color == Color.BLACK and target_piece.piece_color == Color.WHITE) or (
            selected_piece.piece_color == Color.WHITE and target_piece.piece_color == Color.BLACK):
        pawn_or_capture = True

    # Update board
    board[dest_row][dest_col] = selected_piece
    board[piece_row][piece_col] = EmptySquare

    if selected_piece.piece_name == Names.PAWN:
        if selected_piece.piece_color == Color.WHITE and dest_row == 5:
            board[dest_row][dest_col] = WhiteQueen
        elif selected_piece.piece_color == Color.BLACK and dest_row == 0:
            board[dest_row][dest_col] = BlackQueen

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
                f"Pick a square to move the {current_board[r_piece][c_piece]} (enter 'skip' if wrong piece was selected):")

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