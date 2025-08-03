"""Main game controller for the battleship game.

This module implements the Game class, which serves as the main controller
for the battleship game. It manages the game loop, user interface, player
interactions, and game state transitions.
"""

import curses
from time import sleep
from src.board import Board
from src.grid import Grid
from src.ai import Ai
from src.human import Human
from src.utils import Attack, GameMode, Player


class Game:
    """Main game controller that manages the battleship game.
    
    The Game class handles the complete game flow including menu navigation,
    game setup, turn management, user interface rendering, and game state
    tracking. It supports both single-player (human vs AI) and CPU vs CPU modes.
    
    Attributes:
        stdscr: The curses standard screen object for terminal interface.
        mode (GameMode): Current game mode (single player or CPU vs CPU).
        turn (Player): Which player's turn it currently is.
        winner (Player or None): The winning player, if game is complete.
        w1, w2, w3, w4: Curses window objects for displaying game grids.
        p1, p2: Player instances for player one and two.
        b1, b2: Board instances for player one and two.
    """
    
    def __init__(self, stdscr: curses.window):
        """Initialize the game with the curses screen.
        
        Args:
            stdscr: The curses standard screen object for terminal display.
        """
        self.stdscr = stdscr
        self.mode = GameMode.SP
        self.turn = Player.ONE
        self.winner: Player = None
        self.w1 = curses.newwin(12, 24, 2, 2)
        self.w2 = curses.newwin(12, 24, 2, 36)
        self.w3 = curses.newwin(12, 24, 15, 2)
        self.w4 = curses.newwin(12, 24, 15, 36)

    def reset(self):
        """Reset the game to initial state for a new game.
        
        Initializes players based on current game mode, creates new boards
        and grids, and places ships randomly on both boards.
        """
        self.turn = Player.ONE
        self.winner = None
        if self.mode == GameMode.SP:
            get_input = self.stdscr.getch
            p1_grid = Grid(inital_char=".")
            def redraw(): return self.render_grid(self.w3, p1_grid)
            self.p1 = Human(grid=p1_grid, get_input=get_input, redraw=redraw)
        else:
            self.p1 = Ai(grid=Grid(inital_char="."))
        self.p2 = Ai(grid=Grid(inital_char="."))
        self.b1 = Board(grid=Grid())
        self.b2 = Board(grid=Grid())
        self.b1.place_fleet_randomly()
        self.b2.place_fleet_randomly()

    def render_title(self):
        """Render the player titles at the top of the screen."""
        self.stdscr.addstr(0, 7, 'Player 1')
        self.stdscr.addstr(0, 41, 'Player 2')

    def render_grid(self, win: curses.window, grid: Grid or Board):
        """Render a grid or board in the specified window.
        
        Displays the grid with appropriate colors for different cell types.
        
        Args:
            win: The curses window to render into.
            grid: The Grid or Board object to render.
        """
        color_map = {
            'X': curses.color_pair(1),
            '_': curses.color_pair(2),
            '.': curses.color_pair(3),
            '+': curses.color_pair(4),
            'i': curses.color_pair(5),
        }
        y = 0
        x = 0
        for c in grid.render():
            if c == "\n":
                y += 1
                x = 0
            else:
                color = color_map[c] if c in color_map.keys() else 0
                win.addstr(y, x, c, color)
                x += 1
        win.refresh()

    def render_fire(self, player: Grid, pos, result: Attack):
        """Render the result of a firing action.
        
        Displays the attack result and coordinates on the screen.
        
        Args:
            player: The player's grid (for coordinate calculation).
            pos: The position that was attacked.
            result: The result of the attack.
        """
        [a, b] = player.grid.coords(pos)
        if self.stdscr:
            y = 13
            x = 6 if self.turn == Player.ONE else 40
            eraseX = 6 if self.turn == Player.TWO else 40
            self.stdscr.addstr(y, x, '{}! ({}, {})'.format(result.name, a, b))
            self.stdscr.addstr(y, eraseX, ' '*12)
            self.stdscr.refresh()
        else:
            print(result.value, a, b)

    def render_instructions(self):
        """Render game instructions based on current game mode.
        
        Displays different instructions for single-player vs CPU modes.
        """
        y = 27
        x = 1
        if self.mode == GameMode.CPU:
            self.stdscr.addstr(y, x, 'Press (f) to fire')
            self.stdscr.addstr(y + 1, x, 'Press (a) to auto- play')
            self.stdscr.addstr(y + 2, x, 'Press (r) to reset the board')
            self.stdscr.addstr(y + 3, x, 'Press (q) to quit the game')
        elif self.mode == GameMode.SP:
            self.stdscr.addstr(y, x, 'Use arrow keys to move')
            self.stdscr.addstr(y + 1, x, 'Press (f) or (enter) to fire')
            self.stdscr.addstr(y + 2, x, 'Press (q) to quit the game')
        self.stdscr.refresh()

    def render_winner(self):
        """Render the winner announcement.
        
        Displays which player won the game in bold text.
        """
        msg = 'Player {} Wins!'.format(self.winner.value)
        if self.stdscr:
            self.stdscr.addstr(13, 0, msg.center(56, ' '), curses.A_BOLD)
        else:
            print(msg)

    def log(self, msg: str):
        """Log a message to the screen.
        
        Args:
            msg: The message to display.
        """
        self.stdscr.addstr(26, 0, msg.ljust(80, ' '), curses.A_DIM)

    def take_turn(self):
        """Execute one turn of the game.
        
        Gets the current player's attack position, processes the attack
        on the opponent's board, handles the result, and switches turns.
        """
        if self.turn == Player.ONE:
            player = self.p1
            board = self.b2
        else:
            player = self.p2
            board = self.b1

        pos = player.get_attack_pos()
        if pos is not None:
            result = board.receive_attack(pos)
            self.render_fire(player, pos, result)
            player.handle_attack_result(pos, result)
            if result == Attack.WIN:
                self.winner = self.turn

        self.turn = Player.ONE if self.turn == Player.TWO else Player.TWO

    def menu(self):
        """Display and handle the main game menu.
        
        Shows game mode selection and handles navigation between modes.
        Allows starting a new game or quitting.
        """
        self.stdscr.clear()
        win = curses.newwin(60, 80, 0, 0)
        win.addstr(2, 0, "BATTLESHIP!".center(80, ' '), curses.A_BOLD)

        cpuModeLabel = GameMode.CPU.value
        spModeLabel = GameMode.SP.value
        if self.mode == GameMode.CPU:
            cpuModeLabel = "> " + cpuModeLabel
            spModeLabel = "  " + spModeLabel
        if self.mode == GameMode.SP:
            spModeLabel = "> " + spModeLabel
            cpuModeLabel = "  " + cpuModeLabel

        win.addstr(5, 2, spModeLabel)
        win.addstr(7, 2, cpuModeLabel)
        win.refresh()

        key = win.getch()
        if key == 65 and self.mode == GameMode.CPU:
            self.mode = GameMode.SP
        elif key == 66 and self.mode == GameMode.SP:
            self.mode = GameMode.CPU
        elif key == ord('q'):
            return  # quits game
        elif key == 10:
            win.clear()
            return self.run()

        self.menu()

    def run(self):
        """Run the main game loop.
        
        Initializes the game, handles the main game loop including
        rendering, input processing, and game state management.
        Supports both manual and automatic play modes.
        """
        self.reset()
        auto = False

        self.render_title()
        self.render_instructions()
        self.stdscr.refresh()


        while True:
            key = None
            self.render_grid(self.w1, self.b1)
            self.render_grid(self.w3, self.p1.grid)

            if self.mode == GameMode.CPU or self.winner is not None:
                self.render_grid(self.w2, self.b2)
                self.render_grid(self.w4, self.p2.grid)

            if self.mode == GameMode.SP and not self.winner:
                if self.turn == Player.TWO:
                    sleep(1)
                self.take_turn()
            else:
                if not auto:
                    key = self.stdscr.getch()
                if key == ord('q'):
                    break
                elif key == ord('a'):
                    auto = True
                elif not self.winner and (auto or key == ord('f')):
                    if auto:
                        sleep(0.05)
                    self.take_turn()
                elif key == ord('r'):
                    self.stdscr.addstr(13, 0, ' '*60)
                    auto = False
                    self.reset()
                elif key == ord('m'):
                    self.reset()
                    return self.menu()

            if self.winner is not None:
                auto = False
                self.render_winner()

            self.stdscr.refresh()
