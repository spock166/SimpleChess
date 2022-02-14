import random
import tkinter as tk
import sys, time
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


def humanVsComputer(game_board, cur_player, half, full, human_color, disable_board, depth):
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
        print(f"Board Valuation from {cur_player}'s perspective: {boardValue(game_board, cur_player)}")
        if cur_player == human_color:
            pawn_move, end_game = make_move(game_board, cur_player)
        else:
            pawn_move, end_game = alphaMove(game_board, cur_player, depth)

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


def computerVsComputer(game_board, cur_player, half, full):
    white_depth = random.randint(1,8)
    black_depth = random.randint(1,8)

    print(f"White will be playing alpha-beta moves to a depth of {white_depth}.")
    print(f"Black will be playing alpha-beta moves to a depth of {black_depth}.")

    while True:
        # 50 move rule implemented from chess.
        if half >= 50:
            print(f"Game is a draw by 50 move rule.")
            break

        DisplayBoard(game_board)

        print(f"It is move {full} with {cur_player} to play.")

        if cur_player == Color.WHITE:
            pawn_move, end_game = alphaMove(game_board, cur_player, white_depth)
        else:
            pawn_move, end_game = alphaMove(game_board, cur_player, black_depth)

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


def benchmark(game_board, cur_player, half, full, depth):
    move_times = []
    while True:
        # 50 move rule implemented from chess.
        if half >= 50:
            break

        start_time = time.time()
        pawn_move, end_game = alphaMove(game_board, cur_player, depth, suppress_messages=True)
        end_time = time.time()
        move_times.append(end_time-start_time)
        print("Level %d KurisuBot evaluated its move in %.2f seconds" % (depth, move_times[-1]))
        print("Current evaluation average for this level is %.2f seconds" % (sum(move_times)/len(move_times)))
        if end_game:
            print(full)
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
    # TODO: Implement GUI with tkinter
    # window = tk.Tk()
    # main_menu = tk.Label(text = "Main Menu")
    # main_menu.pack()

    while True:
        print('|==================================|')
        print('|Welcome to SimpleChess (name TBA).|')
        print('|1. Human vs. Human                |')
        print('|2. Human vs. Computer             |')
        print('|3. Human vs. Computer (headless)  |')
        print('|4. Bot Battle                     |')
        print('|5. Benchmark KurisuBot            |')
        print('|6. Exit                           |')
        print('|==================================|')

        selection = -1
        while selection not in range(1, 7):
            selection = int(input('Please select an option (1-6): '))

        if selection == 6:
            sys.exit()

        board, current_player, halfturns, fullturns = ReadFEN(starting_fen)

        if selection == 1:
            humanVsHuman(board, current_player, halfturns, fullturns)
        elif selection == 2 or selection == 3:
            human_player = random.choice([Color.BLACK, Color.WHITE])
            headless = True if selection == 3 else False
            opponent_depth = -1

            while opponent_depth not in range(1, 7):
                opponent_depth = int(input('Please enter a max depth for KurisuBot to play at (1-6): '))
            humanVsComputer(board, current_player, halfturns, fullturns, human_player, headless, opponent_depth)
        elif selection == 4:
            computerVsComputer(board, current_player, halfturns, fullturns)
        elif selection == 5:
            num_levels = 0
            while num_levels <= 0:
                num_levels = int(input('Select maximum depth you would like to test: '))

            for i in range(1,num_levels+1):
                board, current_player, halfturns, fullturns = ReadFEN(starting_fen)
                benchmark(board, current_player, halfturns, fullturns, i)