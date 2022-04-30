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

    # value += 0.1 * (len(validMoves(board, player_color)) - len(validMoves(board, opponent_color)))

    return value


def boardValue(board, player_color):
    default_square_values = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                             [0.25, 0.40, 0.40, 0.40, 0.40, 0.25],
                             [0.25, 0.40, 1.00, 1.00, 0.40, 0.25],
                             [0.25, 0.40, 1.00, 1.00, 0.40, 0.25],
                             [0.25, 0.40, 1.40, 0.40, 0.40, 0.25],
                             [0.25, 0.25, 0.25, 0.25, 0.25, 0.25]]

    bishop_square_values =  [[1.00, 0.25, 0.25, 0.25, 0.25, 1.00],
                             [0.25, 1.00, 0.40, 0.40, 1.00, 0.25],
                             [0.25, 0.40, 1.00, 1.00, 0.40, 0.25],
                             [0.25, 0.40, 1.00, 1.00, 0.40, 0.25],
                             [0.25, 1.00, 1.40, 0.40, 1.00, 0.25],
                             [1.00, 0.25, 0.25, 0.25, 0.25, 1.00]]

    opponent_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE
    my_king = False
    opp_king = False
    value = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == EmptySquare:
                pass

            sqr_values = default_square_values

            if board[r][c].piece_name == Names.BISHOP:
                sqr_values = bishop_square_values

            multiplier = 0
            if board[r][c].piece_color == player_color:
                multiplier = 1
            elif board[r][c].piece_color == opponent_color:
                multiplier = -1
            value += multiplier * board[r][c].piece_value * sqr_values[r][c]

            if board[r][c].piece_color == player_color and board[r][c].piece_name == Names.KING:
                my_king = True
            elif board[r][c].piece_color == opponent_color and board[r][c].piece_name == Names.KING:
                opp_king = True
    if not my_king:
        return -5000

    if not opp_king:
        return 5000


    for move in validMoves(board, player_color):
        if board[move[2]][move[3]].piece_color == opponent_color:
            value -= 0.2 * (board[move[0]][move[1]].piece_value - board[move[2]][move[3]].piece_value)

    for move in validMoves(board, opponent_color):
        if board[move[2]][move[3]].piece_color == player_color:
            value += 0.2 * (board[move[0]][move[1]].piece_value - board[move[2]][move[3]].piece_value)

    value += 0.1 * (len(validMoves(board, player_color)) - len(validMoves(board, opponent_color)))

    return value


def minMax(board, depth, maximizing_player, player_color, bot_color, game_over):
    if depth == 0 or game_over:
        return simpleBoardValue(board, bot_color)

    opponent_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE

    if maximizing_player:
        best_eval = float("-inf")
        for move in validMoves(board,player_color):
            board_copy, game_over = HypotheticalMove(*move, board)
            result = minMax(board,depth-1, False,opponent_color,bot_color,game_over)
            best_eval = max(result,best_eval)
        return best_eval
    else:
        worst_eval = float("inf")
        for move in validMoves(board, player_color):
            board_copy, game_over = HypotheticalMove(*move, board)
            result = minMax(board, depth - 1, True, opponent_color, bot_color, game_over)
            worst_eval = min(result, worst_eval)
        return worst_eval


def find_best_min_max_move(board, max_depth, bot_color):
    best_eval = float("-inf")
    possible_moves = validMoves(board, bot_color)
    best_move = possible_moves[0]
    opponent_color = Color.BLACK if bot_color == Color.WHITE else Color.WHITE

    for move in possible_moves:
        #Assume we move
        board_copy, game_over = HypotheticalMove(*move, board)
        result = minMax(board_copy,max_depth,False, opponent_color, bot_color, game_over)
        if result > best_eval:
            best_eval = result
            best_move = move

    return best_move, best_eval


def minMaxMove(board, bot_color, depth, suppress_messages = False):
    selected_move, value = find_best_min_max_move(board, depth, bot_color)

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

    if not suppress_messages:
        print(f"{bot_color} moves {board[piece_row][piece_col].piece_name} from {piece_col_convert}{piece_row_convert} to {dest_col_convert}{dest_row_convert}.")
        print(f"{bot_color} evaluated this move to have value {value}.")

    if isValidMove(*selected_move, board):
        return Move(*selected_move, board)
    else:
        raise Exception('Invalid move selected', bot_color, selected_move)


def alphaBeta(board, depth, maximizing_player, player_color, bot_color, game_over, alpha=float("-inf"), beta=float("inf")):
    if depth == 0 or game_over:
        return simpleBoardValue(board, bot_color)
        #return boardValue(board,bot_color)

    opponent_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE
    possible_moves = validMoves(board, player_color)
    random.shuffle(possible_moves)

    if maximizing_player:
        for move in possible_moves:
            board_copy, game_over = HypotheticalMove(*move, board)
            result = alphaBeta(board,depth-1, False,opponent_color,bot_color,game_over,alpha,beta)
            alpha = max(result,alpha)
            if beta <= alpha:
                break
        return alpha
    else:
        for move in possible_moves:
            board_copy, game_over = HypotheticalMove(*move, board)
            result = alphaBeta(board, depth - 1, True, opponent_color, bot_color, game_over,alpha,beta)
            beta = min(result,beta)
            if beta <= alpha:
                break
        return beta

def find_best_alpha_beta_move(board, max_depth, bot_color):
    best_eval = float("-inf")
    possible_moves = validMoves(board, bot_color)
    random.shuffle(possible_moves)
    best_move = possible_moves[0]
    opponent_color = Color.BLACK if bot_color == Color.WHITE else Color.WHITE

    for move in possible_moves:
        #Assume we move
        board_copy, game_over = HypotheticalMove(*move, board)
        result = alphaBeta(board_copy,max_depth,False, opponent_color, bot_color, game_over)
        if result > best_eval:
            best_eval = result
            best_move = move

    return best_move, best_eval


def alphaBetaMove(board, bot_color, depth, suppress_messages = False):
    selected_move, value = find_best_alpha_beta_move(board, depth, bot_color)

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

    if not suppress_messages:
        print(f"{bot_color} moves {board[piece_row][piece_col].piece_name} from {piece_col_convert}{piece_row_convert} to {dest_col_convert}{dest_row_convert}.")
        print(f"{bot_color} evaluated this move to have value {value}.")

    if isValidMove(*selected_move, board):
        return Move(*selected_move, board)
    else:
        raise Exception('Invalid move selected', bot_color, selected_move)




