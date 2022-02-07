import random


from GameMechanics import *
from Bots import *

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


def humanVsHuman(game_board, cur_player, half, full):
    while True:
        # 50 move rule implemented from chess.
        if half >= 50:
            print(f"Game is a draw by 50 move rule.")
            break

        # Don't display the board if running a headless game.
        # Optimal if human has a physical board to reference.
        if selection != 3:
            DisplayBoard(game_board)

        print(f"It is move {full} with {cur_player} to play.")

        # Update half move counter
        pawn_move, end_game = make_move(game_board, cur_player)

        if end_game:
            print("Game Over!")
            break

        if pawn_move:
            half = 0
        else:
            half += 1

        # Update whose turn it is
        if cur_player == Color.BLACK:
            cur_player = Color.WHITE
            full += 1
        else:
            cur_player = Color.BLACK


def humanVsComputer(game_board, cur_player, half, full, human_color, disable_board):
    while True:
        # 50 move rule implemented from chess.
        if half >= 50:
            print(f"Game is a draw by 50 move rule.")
            break

        # Don't display the board if running a headless game.
        # Optimal if human has a physical board to reference.
        if not disable_board:
            DisplayBoard(game_board)

        print(f"It is move {full} with {cur_player} to play.")

        if cur_player == human_color:
            pawn_move, end_game = make_move(game_board, cur_player)
        else:
            pawn_move, end_game = randomMove(game_board, cur_player)

        if end_game:
            print("Game Over!")
            break

        # Update half move counter
        if pawn_move:
            half = 0
        else:
            half += 1

        # Update whose turn it is
        if cur_player == Color.BLACK:
            cur_player = Color.WHITE
            full += 1
        else:
            cur_player = Color.BLACK




if __name__ == "__main__":

    while True:
        print('|================================|')
        print('|Welcome to SimpleChess.         |')
        print('|1. Human vs. Human              |')
        print('|2. Human vs. Computer           |')
        print('|3. Human vs. Computer (headless)|')
        print('|4. Exit                         |')
        print('|================================|')

        selection = -1
        while selection not in range(1,5):
            selection = int(input('Please select an option (1-4): '))

        board, current_player, halfturns, fullturns = ReadFEN(starting_fen)

        if selection == 1:
            humanVsHuman(board, current_player, halfturns, fullturns)
        else:
            human_player = random.choice([Color.BLACK,Color.WHITE])
            headless = True if selection == 3 else False
            humanVsComputer(board, current_player, halfturns, fullturns, human_player, headless)




