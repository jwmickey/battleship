import random
from src.grid import Grid
from src.player import Player
from src.utils import Attack, Direction, Orientation


class Ai(Player):
    def __init__(self, grid: Grid):
        super().__init__(grid)
        self.reset()

    def get_attack_pos(self) -> int:
        pos = None

        if self.last_hit is not None:
            pos = self.next_target()

        if not pos:
            self.last_hit = None
            choices = self.grid.empty_positions()
            if len(choices):
                pos = random.choice(choices)
                if not self.has_open_neighbors(pos):
                    self.grid.mark(pos, Attack.INVALID.value)
                    return self.get_attack_pos()

        return pos

    def handle_attack_result(self, pos: int, result: Attack):
        self.grid.mark(pos, Attack.MISS.value if result ==
                       Attack.MISS else Attack.HIT.value)

        if result == Attack.HIT:
            self.last_hit = pos
            if self.last_hit_origin is None:
                self.last_hit_origin = pos
            if self.ship_orientation is None:
                self.set_ship_orientation()
        elif result == Attack.SINK:
            self.reset_ship_tracking()
        elif result == Attack.WIN:
            self.finished = True
        elif result == Attack.MISS:
            self.last_hit = self.last_hit_origin
            if self.ship_orientation is None:
                self.direction = None

    def reset(self):
        self.grid.reset()
        self.reset_ship_tracking()

    def reset_ship_tracking(self):
        self.last_hit = None
        self.last_hit_origin = None
        self.direction = None
        self.ship_orientation = None
        self.has_reversed = False

    def valid_moves_from(self, pos):
        grid = self.grid
        neighbors = grid.neighbors(pos)
        moves = []
        for dir in neighbors._fields:
            pos = getattr(neighbors, dir)
            if pos is not None and grid.val(pos) == grid.initial_char:
                moves.append((Direction[dir], pos))
        return moves

    def set_ship_orientation(self):
        if self.direction == Direction.UP or self.direction == Direction.DOWN:
            self.ship_orientation = Orientation.VERTICAL
        elif self.direction == Direction.LEFT or self.direction == Direction.RIGHT:
            self.ship_orientation = Orientation.HORIZONTAL
        else:
            self.ship_orientation = None

    def reverse_direction(self):
        self.has_reversed = True
        if self.ship_orientation == Orientation.VERTICAL:
            if self.direction == Direction.UP:
                self.direction = Direction.DOWN
            elif self.direction == Direction.DOWN:
                self.direction = Direction.UP
        elif self.ship_orientation == Orientation.HORIZONTAL:
            if self.direction == Direction.LEFT:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.LEFT

    # TODO: this needs improvement
    def next_best_direction(self, pos):
        [x, y] = self.grid.coords(pos)
        if y < 2 or y > 7:
            return Direction.LEFT if x >= 5 else Direction.RIGHT
        if x < 2 or x > 7:
            return Direction.UP if y >= 5 else Direction.DOWN
        return None

    def next_in_direction(self):
        if not self.last_hit or not self.direction:
            return None

        neighbors = self.grid.neighbors(self.last_hit)
        pos = getattr(neighbors, self.direction.value)

        if pos is not None and self.grid.val(pos) == self.grid.initial_char:
            return pos
        elif self.ship_orientation and not self.has_reversed:
            self.reverse_direction()
            self.last_hit = self.last_hit_origin
            return self.next_in_direction()
        elif self.has_reversed:
            self.reset_ship_tracking()

        return None

    def next_target(self):
        # next_target only works when we have a previous hit
        if not self.last_hit:
            self.last_hit_origin = None
            return None

        # keep chasing in the same direction, if the next position is valid
        if self.direction:
            return self.next_in_direction()

        # is there a best direction?
        preferred = self.next_best_direction(self.last_hit)

        # find valid moves
        targets = self.valid_moves_from(self.last_hit)

        if len(targets):
            if preferred and preferred in [t[0] for t in targets]:
                [dir, pos] = [t for t in targets if t[0] == preferred][0]
            else:
                [dir, pos] = random.choice(targets)

            self.direction = dir
            return pos
        else:
            return None

    def has_open_neighbors(self, pos):
      neighbors = self.grid.neighbors(pos)
      return len([x for x in neighbors if x is not None and self.grid.val(x) == self.grid.initial_char]) > 0
