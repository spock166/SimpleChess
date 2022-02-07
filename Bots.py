import random

from GameMechanics import *


def randomMove(board, bot_color):
    selected_move = random.choice(validMoves(board,bot_color))
    piece_row, piece_col, dest_row, dest_col = selected_move
    piece_row_convert = piece_row+1
    dest_row_convert = dest_row+1

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


    print(f"{bot_color} moves {board[piece_row][piece_col].piece_name} from {piece_col_convert}{piece_row_convert} to {dest_col_convert}{dest_row_convert}.")
    if isValidMove(*selected_move, board):
        return Move(*selected_move, board)