import random
import copy
import math

from GameMechanics import *


def randomMove(board, bot_color):
    selected_move = random.choice(validMoves(board, bot_color))
    piece_row, piece_col, dest_row, dest_col = selected_move
    piece_row_convert = piece_row + 1
    dest_row_convert = dest_row + 1

    if piece_col == 0:
        piece_col_convert = 'a'
    elif piece_col == 1:
        piece_col_convert = 'b'
    elif piece_col == 2:
        piece_col_convert = 'c'
    elif piece_col == 3:
        piece_col_convert = 'd'
    elif piece_col == 4:
        piece_col_convert = 'e'
    elif piece_col == 5:
        piece_col_convert = 'f'
    else:
        piece_row_convert = '?'

    if dest_col == 0:
        dest_col_convert = 'a'
    elif dest_col == 1:
        dest_col_convert = 'b'
    elif dest_col == 2:
        dest_col_convert = 'c'
    elif dest_col == 3:
        dest_col_convert = 'd'
    elif dest_col == 4:
        dest_col_convert = 'e'
    elif dest_col == 5:
        dest_col_convert = 'f'
    else:
        dest_col_convert = '?'

    print(
        f"{bot_color} moves {board[piece_row][piece_col].piece_name} from {piece_col_convert}{piece_row_convert} to {dest_col_convert}{dest_row_convert}.")
    if isValidMove(*selected_move, board):
        return Move(*selected_move, board)


def simpleBoardValue(board, player_color):
    opponent_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE
    value = 0
    my_king = False
    opp_king = False
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == EmptySquare:
                pass
            multiplier = 0
            if board[r][c].piece_color == player_color:
                multiplier = 1
            elif board[r][c].piece_color == opponent_color:
                multiplier = -1
            value += multiplier * board[r][c].piece_value

            if board[r][c].piece_color == player_color and board[r][c].piece_name == Names.KING:
                my_king = True
            elif board[r][c].piece_color == opponent_color and board[r][c].piece_name == Names.KING:
                opp_king = True

    if not my_king:
        return -5000

    if not opp_king:
        return 5000

    #value += 0.1 * (len(validMoves(board, player_color)) - len(validMoves(board, opponent_color)))

    return value

def boardValue(board, player_color):
    default_square_values = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                             [0.25, 0.40, 0.40, 0.40, 0.40, 0.25],
                             [0.25, 0.40, 1.00, 1.00, 0.40, 0.25],
                             [0.25, 0.40, 1.00, 1.00, 0.40, 0.25],
                             [0.25, 0.40, 1.40, 0.40, 0.40, 0.25],
                             [0.25, 0.25, 0.25, 0.25, 0.25, 0.25]]

    opponent_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE
    value = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == EmptySquare:
                pass
            multiplier = 0
            if board[r][c].piece_color == player_color:
                multiplier = 1
            elif board[r][c].piece_color == opponent_color:
                multiplier = -1
            value += multiplier * board[r][c].piece_value

    for move in validMoves(board, player_color):
        if board[move[2]][move[3]].piece_color == opponent_color:
            value -= 0.2 * (board[move[0]][move[1]].piece_value - board[move[2]][move[3]].piece_value)

    for move in validMoves(board, opponent_color):
        if board[move[2]][move[3]].piece_color == player_color:
            value += 0.2 * (board[move[0]][move[1]].piece_value - board[move[2]][move[3]].piece_value)

    value += 0.1 * (len(validMoves(board, player_color)) - len(validMoves(board, opponent_color)))

    return value

def canIHazEnemyKing(board, player_color):
    opponent_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE
    for x in validMoves(board, player_color):
        if board[x[2]][x[3]].piece_name == Names.KING and board[x[2]][x[3]].piece_color == opponent_color:
            return x


def alphaBeta(board, depth, current_depth, alpha, beta, maximizing_player, player_color, bot_color, game_over):
    if depth == 0 or game_over:
        return boardValue(board, bot_color), [0, 0, 0, 0]


    opponent_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE
    best_move = validMoves(board, player_color)[0]

    if maximizing_player:
        value = -math.inf
        for x in validMoves(board, player_color):
            board_copy, game_over = HypotheticalMove(*x, board)
            value = max(value,
                        alphaBeta(board_copy, depth - 1, current_depth+1,alpha, beta, False, opponent_color, bot_color, game_over)[0])
            if value >= beta:
                break
            alpha = max(alpha, value)
            best_move = x
        return value, best_move
    else:
        value = math.inf
        for x in validMoves(board, player_color):
            board_copy, game_over = HypotheticalMove(*x, board)
            value = min(value,
                        alphaBeta(board_copy, depth - 1, current_depth+1, alpha, beta, True, opponent_color, bot_color, game_over)[0])
            if value <= alpha:
                break
            beta = min(beta, value)
            best_move = x
        return value, best_move


def alphaMove(board, bot_color, depth):
    kingCapture = canIHazEnemyKing(board, bot_color)

    if kingCapture in validMoves(board, bot_color):
        value = 5000
        selected_move = kingCapture
    else:
        value, selected_move = alphaBeta(board, depth, 1, -math.inf, math.inf, True, bot_color, bot_color, False)

    piece_row, piece_col, dest_row, dest_col = selected_move
    piece_row_convert = piece_row + 1
    dest_row_convert = dest_row + 1

    if piece_col == 0:
        piece_col_convert = 'a'
    elif piece_col == 1:
        piece_col_convert = 'b'
    elif piece_col == 2:
        piece_col_convert = 'c'
    elif piece_col == 3:
        piece_col_convert = 'd'
    elif piece_col == 4:
        piece_col_convert = 'e'
    elif piece_col == 5:
        piece_col_convert = 'f'
    else:
        piece_row_convert = '?'

    if dest_col == 0:
        dest_col_convert = 'a'
    elif dest_col == 1:
        dest_col_convert = 'b'
    elif dest_col == 2:
        dest_col_convert = 'c'
    elif dest_col == 3:
        dest_col_convert = 'd'
    elif dest_col == 4:
        dest_col_convert = 'e'
    elif dest_col == 5:
        dest_col_convert = 'f'
    else:
        dest_col_convert = '?'

    print(
        f"{bot_color} moves {board[piece_row][piece_col].piece_name} from {piece_col_convert}{piece_row_convert} to {dest_col_convert}{dest_row_convert}.")
    print(f"{bot_color} evaluated this move to have value {value}.")

    if isValidMove(*selected_move, board):
        return Move(*selected_move, board)
    else:
        raise Exception('Invalid move selected', bot_color, selected_move)
