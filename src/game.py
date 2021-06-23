import curses
from time import sleep
from src.board import Board
from src.grid import Grid
from src.ai import Ai
from src.human import Human
from src.utils import Attack, GameMode, Player


class Game:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.mode = GameMode.SP
        self.turn = Player.ONE
        self.winner: Player = None
        self.w1 = curses.newwin(12, 24, 2, 2)
        self.w2 = curses.newwin(12, 24, 2, 36)
        self.w3 = curses.newwin(12, 24, 15, 2)
        self.w4 = curses.newwin(12, 24, 15, 36)

    def reset(self):
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
        self.stdscr.addstr(0, 7, 'Player 1')
        self.stdscr.addstr(0, 41, 'Player 2')

    def render_grid(self, win: curses.window, grid: Grid or Board):
        color_map = {
            'X': curses.color_pair(1),
            '_': curses.color_pair(2),
            '.': curses.color_pair(3),
            '+': curses.color_pair(4)
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

    def render_fire(self, player: Grid, pos):
        [a, b] = player.grid.coords(pos)
        if self.stdscr:
            y = 13
            x = 6 if self.turn == Player.ONE else 40
            eraseX = 6 if self.turn == Player.TWO else 40
            self.stdscr.addstr(y, x, 'FIRE! ({}, {})'.format(a, b))
            self.stdscr.addstr(y, eraseX, ' '*12)
            self.stdscr.refresh()
        else:
            print('FIRE: ', a, b)

    def render_winner(self):
        msg = 'Player {} Wins!'.format(self.winner.value)
        if self.stdscr:
            self.stdscr.addstr(13, 0, msg.center(56, ' '), curses.A_BOLD)
        else:
            print(msg)

    def log(self, msg: str):
        self.stdscr.addstr(26, 0, msg.ljust(80, ' '), curses.A_DIM)

    def take_turn(self):
        if self.turn == Player.ONE:
            player = self.p1
            board = self.b2
        else:
            player = self.p2
            board = self.b1

        pos = player.get_attack_pos()
        if pos is not None:
            self.render_fire(player, pos)
            result = board.receive_attack(pos)
            player.handle_attack_result(pos, result)
            if result == Attack.WIN:
                self.winner = self.turn

        self.turn = Player.ONE if self.turn == Player.TWO else Player.TWO

    def menu(self):
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
        self.reset()
        auto = False

        self.render_title()
        self.stdscr.refresh()

        while True:
            key = None
            self.render_grid(self.w1, self.b1)
            self.render_grid(self.w2, self.b2)
            self.render_grid(self.w3, self.p1.grid)
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
