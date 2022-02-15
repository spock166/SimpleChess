import sys, time
from Bots import *
import pygame, pygame_gui

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
WIDTH = 1024
HEIGHT = 768


def humanVsHuman(game_board, cur_player, half, full):
    while True:
        # 50 move rule implemented from chess.
        if half >= 50:
            print(f"Game is a draw by 50 move rule.")
            break

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
    white_depth = random.randint(1, 8)
    black_depth = random.randint(1, 8)

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
        move_times.append(end_time - start_time)
        print("Level %d KurisuBot evaluated its move in %.2f seconds" % (depth, move_times[-1]))
        print("Current evaluation average for this level is %.2f seconds" % (sum(move_times) / len(move_times)))
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


class SimpleChessGUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SimpleChess")
        resolution = (WIDTH, HEIGHT)
        self.window_surface = pygame.display.set_mode(resolution)
        self.bg_img = pygame.image.load('images/menuBackground.jpg')
        self.manager = pygame_gui.UIManager(resolution, 'theme.json')
        self.button_width = 256
        self.depth = 3
        self.board, self.current_player, self.halfturns, self.fullturns = ReadFEN(starting_fen)
        self.selecting_target = False
        self.game_over = False
        self.human_color = random.choice([Color.BLACK, Color.WHITE])
        self.waiting_for_bot = False

    def showBoardGUI(self,surface, game_board):
        for r in range(len(game_board)):
            r_prime = len(game_board) - 1 - r
            for c in range(len(game_board[r])):
                square_color = '#000000' if (r + c) % 2 else '#ffffff'
                pygame.draw.rect(surface, square_color, (128 * c, 128 * r_prime, 128, 128))
                if game_board[r][c].piece_name != Names.EMPTY:
                    prefix = 'black' if game_board[r][c].piece_color == Color.BLACK else 'white'
                    suffix = game_board[r][c].piece_char
                    img_name =prefix+'-'+suffix+'.png'
                    piece_image = pygame.image.load('images/'+img_name)
                    surface.blit(piece_image,(128*c,128*r_prime))

    def showMainMenu(self):
        self.manager.clear_and_reset()
        self.window_surface.blit(self.bg_img, (0, 0))
        self.menu_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH - 500) / 2, 50), (500, 50)),
                                                      text="Welcome to SimpleChess", manager=self.manager,
                                                      object_id='@page_labels')
        self.pvp_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - self.button_width) / 2, 200), (self.button_width, 50)),
            text="Human vs. Human",
            manager=self.manager)
        self.pvb_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - self.button_width) / 2, 300), (self.button_width, 50)),
            text="Human vs. Bot",
            manager=self.manager)
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - self.button_width) / 2, 400), (self.button_width, 50)), text="Exit",
            manager=self.manager)

    def showPvP(self):
        self.manager.clear_and_reset()
        self.window_surface.fill('#B1B1B1')
        color = 'black' if self.current_player == Color.BLACK else 'white'
        self.turn_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((WIDTH - 256, 50), (256, 50)),
                                                      text=f"Currently {color} turn {self.fullturns}", manager=self.manager,
                                                      object_id='@page_labels')
        self.current_state = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((WIDTH - 256, 100), (256, 50)),
                                                      text="Please select a piece to move.", manager=self.manager,
                                                      object_id='@page_labels')
        self.showBoardGUI(self.window_surface, self.board)
        self.back_to_main_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH - self.button_width, 650), (self.button_width, 50)), text="Back",
            manager=self.manager)
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH - self.button_width, 700), (self.button_width, 50)), text="Exit",
            manager=self.manager)

    def showPvBSettings(self):
        self.manager.clear_and_reset()
        self.window_surface.blit(self.bg_img, (0, 0))
        self.menu_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH - 500) / 2, 50), (500, 50)),
                                                      text="Game Settings", manager=self.manager,
                                                      object_id='@page_labels')
        self.depth_selector = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(((WIDTH - 500) / 2, 150), (500, 50)),
            manager=self.manager, start_value=self.depth, value_range=(1, 5), click_increment=1)

        self.depth_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH - 500) / 2, 250), (500, 50)),
                                                      text=str(self.depth_selector.get_current_value()),
                                                      manager=self.manager, object_id='@page_labels')

        self.back_to_main_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((WIDTH - 2 * self.button_width) / 2, 600), (self.button_width, 50)), text="Back",
            manager=self.manager)

        self.start_pvb_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH / 2, 600), (self.button_width, 50)), text="Start Game",
            manager=self.manager)

    def showPvB(self):
        # TODO:Select image based on depth
        self.manager.clear_and_reset()

        color = 'black' if self.current_player == Color.BLACK else 'white'

        self.window_surface.fill('#B1B1B1')
        self.bot_img = pygame.image.load('images/PawnPortrait.png')
        self.window_surface.blit(self.bot_img, (WIDTH - 256, 0))
        self.bot_text = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((WIDTH - 256, HEIGHT-296), (256, 96)),
                                                      manager=self.manager,
                                                      html_text=f"Will you play with me senpai?")
        self.turn_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((WIDTH - 256, HEIGHT-200), (256, 50)),
                                                      text=f"Currently {color} turn {self.fullturns}",
                                                      manager=self.manager,
                                                      object_id='@page_labels')
        if self.current_player == self.human_color:
            self.current_state = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((WIDTH - 256, HEIGHT-150), (256, 50)),
                                                         text="Please select a piece to move.", manager=self.manager,
                                                         object_id='@page_labels')
        else:
            self.current_state = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((WIDTH - 256, HEIGHT - 150), (256, 50)),
                text="Please wait for bot.", manager=self.manager,
                object_id='@page_labels')
        self.showBoardGUI(self.window_surface,self.board)
        self.back_to_main_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH-self.button_width,HEIGHT-100), (self.button_width, 50)), text="Back",
            manager=self.manager)
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH-self.button_width,HEIGHT-50), (self.button_width, 50)), text="Exit",
            manager=self.manager)

    def runApp(self):
        clock = pygame.time.Clock()
        is_running = True
        current_screen = 'mainmenu'

        self.showMainMenu()
        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.pvp_button:
                        current_screen = 'PVP'
                        self.board, self.current_player, self.halfturns, self.fullturns = ReadFEN(starting_fen)
                        self.game_over = False
                        self.showPvP()

                    elif event.ui_element == self.pvb_button:
                        current_screen = 'PVBSettings'
                        self.showPvBSettings()
                    elif event.ui_element == self.back_to_main_button:
                        current_screen = 'mainmenu'
                        self.showMainMenu()
                    elif event.ui_element == self.start_pvb_game:
                        current_screen = 'PVB'
                        self.board, self.current_player, self.halfturns, self.fullturns = ReadFEN(starting_fen)
                        self.human_color = random.choice([Color.BLACK, Color.WHITE])
                        self.game_over = False
                        self.showPvB()
                    elif event.ui_element == self.exit_button:
                        exit()

                if event.type == pygame.MOUSEBUTTONDOWN and (current_screen == 'PVP' or current_screen == 'PVB') and not self.game_over:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    if pos_x > 768 or pos_x < 0 or pos_y > 768 or pos_y < 0:
                        break

                    c = pos_x // 128
                    r = 5 - pos_y //128

                    #Handle PvP first
                    if current_screen == 'PVP':
                        if self.board[r][c].piece_color == self.current_player:
                            self.selecting_target = True
                            piece_row = r
                            piece_col = c
                            self.current_state.set_text('Select a target square')

                        if self.board[r][c].piece_color != self.current_player and self.selecting_target:
                            dest_row = r
                            dest_col = c
                            if isValidMove(piece_row, piece_col, dest_row, dest_col, self.board):
                                pawn_or_capture, self.game_over = Move(piece_row, piece_col, dest_row, dest_col, self.board)
                                self.showBoardGUI(self.window_surface, self.board)
                                if self.game_over:
                                    color = 'black' if self.current_player == Color.BLACK else 'white'
                                    self.current_state.set_text(f"{color} wins")
                                    break
                                elif self.halfturns >= 50:
                                    self.current_state.set_text("Game is a Draw")
                                    self.game_over = True
                                    break
                                else:
                                    if pawn_or_capture:
                                        self.halfturns = 0
                                    else:
                                        self.halfturns += 1

                                    if self.current_player == Color.BLACK:
                                        self.current_player = Color.WHITE
                                        self.fullturns += 1
                                    else:
                                        self.current_player = Color.BLACK
                                    color = 'black' if self.current_player == Color.BLACK else 'white'
                                    self.turn_label.set_text(f"Currently {color} turn {self.fullturns}")
                                    self.current_state.set_text("Please select a piece to move.")

                    #Next handle PvB next
                    if current_screen == 'PVB':
                        if self.board[r][c].piece_color == self.current_player and self.current_player == self.human_color:
                            self.selecting_target = True
                            piece_row = r
                            piece_col = c
                            self.current_state.set_text('Select a target square')

                        if self.board[r][c].piece_color != self.current_player and self.selecting_target and self.current_player == self.human_color:
                            dest_row = r
                            dest_col = c
                            if isValidMove(piece_row, piece_col, dest_row, dest_col, self.board):
                                pawn_or_capture, self.game_over = Move(piece_row, piece_col, dest_row, dest_col, self.board)
                                self.showBoardGUI(self.window_surface, self.board)
                                if self.game_over:
                                    color = 'black' if self.current_player == Color.BLACK else 'white'
                                    self.current_state.set_text(f"{color} wins")
                                    break
                                elif self.halfturns >= 50:
                                    self.current_state.set_text("Game is a Draw")
                                    self.game_over = True
                                    break
                                else:
                                    if pawn_or_capture:
                                        self.halfturns = 0
                                    else:
                                        self.halfturns += 1

                                    if self.current_player == Color.BLACK:
                                        self.current_player = Color.WHITE
                                        self.fullturns += 1
                                    else:
                                        self.current_player = Color.BLACK
                                    color = 'black' if self.current_player == Color.BLACK else 'white'
                                    self.turn_label.set_text(f"Currently {color} turn {self.fullturns}")
                                    self.current_state.set_text("Please wait for bot to move.")

                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.depth_selector:
                        self.depth = int(self.depth_selector.get_current_value())
                        self.depth_text.set_text(f"Current difficulty: {self.depth}")
                        #self.manager.clear_and_reset()
                        #self.showPvBSettings()

            if current_screen == 'PVB' and self.current_player != self.human_color:
                pawn_or_capture, self.game_over = alphaMove(self.board, self.current_player, self.depth, True)
                self.showBoardGUI(self.window_surface, self.board)
                if self.game_over:
                    color = 'black' if self.current_player == Color.BLACK else 'white'
                    self.current_state.set_text(f"{color} wins")
                    break
                elif self.halfturns >= 50:
                    self.current_state.set_text("Game is a Draw")
                    self.game_over = True
                    break
                else:
                    if pawn_or_capture:
                        self.halfturns = 0
                    else:
                        self.halfturns += 1

                    if self.current_player == Color.BLACK:
                        self.current_player = Color.WHITE
                        self.fullturns += 1
                    else:
                        self.current_player = Color.BLACK
                    color = 'black' if self.current_player == Color.BLACK else 'white'
                    self.turn_label.set_text(f"Currently {color} turn {self.fullturns}")
                    self.current_state.set_text("Please select a piece.")

            self.manager.process_events(event)

            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()

def consoleChess():
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

            for i in range(1, num_levels + 1):
                board, current_player, halfturns, fullturns = ReadFEN(starting_fen)
                benchmark(board, current_player, halfturns, fullturns, i)

if __name__ == "__main__":
    # Uncomment for GUI
    display = SimpleChessGUI();
    display.runApp()

    # Uncomment for terminal
    # consoleChess()


