from src.grid import Grid
from src.player import Player
from src.utils import Attack, DPad, Direction, KeyPad


class Human(Player):
    def __init__(self, grid: Grid, get_input, redraw):
        super().__init__(grid)
        self.get_input = get_input
        self.redraw = redraw
        self.reset()

    def reset(self):
        self.grid.reset()
        self.pos = 0
        self.covered_val = self.grid.val(self.pos)
        self.grid.mark(self.pos, '+')
        self.redraw()

    def get_attack_pos(self) -> int:
        while True:
            key = self.get_input()
            if key == KeyPad.ENTER.value or key == ord('f'):
                return self.pos
            elif key in DPad:
                self.move(DPad[key])

    def handle_attack_result(self, pos: int, result: Attack):
        self.grid.mark(pos, Attack.MISS.value if result ==
                       Attack.MISS else Attack.HIT.value)
        self.covered_val = self.grid.val(pos)
        self.redraw()

    def move(self, dir: Direction):
        next = self.pos
        while True:
            neighbors = self.grid.neighbors(next)
            next = getattr(neighbors, dir.value)
            if next is None:
                return None
            if self.grid.val(next) == self.grid.initial_char:
                break

        if next != self.pos:
            next_covered = self.grid.val(next)
            self.grid.mark(next, '+')
            self.grid.mark(self.pos, self.covered_val)
            self.covered_val = next_covered
            self.pos = next
            self.redraw()
