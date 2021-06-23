from random import choice
from src.grid import Grid
from src.utils import Attack, Fleet, Orientation, Ship, ShipPlacement


class Board:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.hits = []
        self.total_fleet_size = 0

    def reset(self):
        self.hits = []
        self.total_fleet_size = 0
        self.grid.reset()

    def receive_attack(self, pos: int) -> Attack:
        val = self.grid.val(pos)
        if val == self.grid.initial_char:
            return Attack.MISS
        else:
            self.hits.append(pos)
            if self.fleet_is_sunk():
                return Attack.WIN
            if self.ship_is_sunk(self.ship_at_pos(pos)):
                return Attack.SINK
            return Attack.HIT

    def ship_hits(self, ship: Ship) -> int:
        return len([x for x in self.hits if self.grid.val(x) == ship.id])

    def ship_at_pos(self, pos: int):
        val = self.grid.val(pos)
        return next(iter([member.value for member in Fleet.__members__.values() if member.value.id == val]), None)

    def ship_is_sunk(self, ship: Ship) -> bool:
        return self.ship_hits(ship) == ship.size

    def fleet_is_sunk(self) -> bool:
        return len(self.hits) == self.total_fleet_size

    def ship_placement(self, pos: int, ship: Ship, orientation: Orientation) -> ShipPlacement:
        empty_value = self.grid.get_initial_char()

        # get list of positions required for this ship and orientation
        positions = []
        curr = pos
        i = 0
        while i < ship.size and curr is not None:
            positions.append(curr)
            neighbors = self.grid.neighbors(curr)
            curr = neighbors.RIGHT if orientation == Orientation.HORIZONTAL else neighbors.DOWN
            i += 1

        if len(positions) != ship.size:
            return ShipPlacement(False, [])

        # make sure all values of positions are the empty value
        empty_slots = [x for x in positions if self.grid.val(x) == empty_value]
        valid_placement = len(empty_slots) == ship.size
        return ShipPlacement(valid_placement, positions)

    def place_ship(self, pos: int, ship: Ship, orientation: Orientation) -> bool:
        [valid, positions] = self.ship_placement(pos, ship, orientation)
        if not valid:
            return False
        for x in positions:
            self.grid.mark(x, ship.id)
        self.total_fleet_size += ship.size
        return True

    def place_fleet_randomly(self):
        ships = [f.value for f in list(Fleet)]
        attempts = 0
        for ship in ships:
            placed = False
            while not placed:
                attempts += 1
                pos = choice(self.grid.empty_positions())
                orientation = choice(list(Orientation))
                placed = self.place_ship(pos, ship, orientation)

    def render(self):
        """Renders the board with hits recognized

        Returns:
            A string representation of the grid in size x size
        """
        size = self.grid.get_size()
        s = ""
        for i in range(size):
            offset = i * size
            chars = self.grid.grid[offset:offset + size]
            for j in range(size):
                if self.grid.pos(j, i) in self.hits:
                    chars[j] = Attack.HIT.value

            s += "\n" + "".join(["{} ".format(c) for c in chars])[:-1]
        return s[1:]
