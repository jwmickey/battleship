"""Game board implementation for the battleship game.

This module implements the Board class, which manages ship placement,
attack handling, and game state tracking for a player's board in battleship.
"""

from random import choice
from src.grid import Grid
from src.utils import Attack, Fleet, Orientation, Ship, ShipPlacement


class Board:
    """Game board that manages ships and handles attacks.
    
    The Board class represents a player's game board containing their fleet
    of ships. It handles ship placement, attack processing, and tracks hits
    to determine when ships are sunk or the game is won.
    
    Attributes:
        grid (Grid): The underlying grid containing ship positions.
        hits (list): List of positions that have been successfully hit.
        total_fleet_size (int): Total number of grid cells occupied by ships.
    """
    
    def __init__(self, grid: Grid):
        """Initialize a board with the given grid.
        
        Args:
            grid (Grid): The grid to use for ship placement and tracking.
        """
        self.grid = grid
        self.hits = []
        self.total_fleet_size = 0

    def reset(self):
        """Reset the board to empty state.
        
        Clears all hits, resets fleet size, and resets the underlying grid.
        """
        self.hits = []
        self.total_fleet_size = 0
        self.grid.reset()

    def receive_attack(self, pos: int) -> Attack:
        """Process an incoming attack at the specified position.
        
        Determines the result of an attack and updates the board state
        accordingly. Tracks hits and checks for sunk ships or game end.
        
        Args:
            pos (int): The grid position being attacked.
            
        Returns:
            Attack: The result of the attack (MISS, HIT, SINK, or WIN).
        """
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
        """Count the number of hits on a specific ship.
        
        Args:
            ship (Ship): The ship to count hits for.
            
        Returns:
            int: The number of times this ship has been hit.
        """
        return len([x for x in self.hits if self.grid.val(x) == ship.id])

    def ship_at_pos(self, pos: int):
        """Get the ship located at the specified position.
        
        Args:
            pos (int): The grid position to check.
            
        Returns:
            Ship or None: The ship at that position, or None if no ship.
        """
        val = self.grid.val(pos)
        return next(iter([member.value for member in Fleet.__members__.values() if member.value.id == val]), None)

    def ship_is_sunk(self, ship: Ship) -> bool:
        """Check if the specified ship has been completely sunk.
        
        Args:
            ship (Ship): The ship to check.
            
        Returns:
            bool: True if the ship is completely sunk, False otherwise.
        """
        return self.ship_hits(ship) == ship.size

    def fleet_is_sunk(self) -> bool:
        """Check if the entire fleet has been sunk.
        
        Returns:
            bool: True if all ships in the fleet are sunk, False otherwise.
        """
        return len(self.hits) == self.total_fleet_size

    def ship_placement(self, pos: int, ship: Ship, orientation: Orientation) -> ShipPlacement:
        """Check if a ship can be placed at the given position and orientation.
        
        Validates that all positions required for the ship are empty and
        within the grid boundaries.
        
        Args:
            pos (int): The starting position for ship placement.
            ship (Ship): The ship to be placed.
            orientation (Orientation): The orientation for placement.
            
        Returns:
            ShipPlacement: A named tuple indicating if placement is valid
                          and listing the positions that would be occupied.
        """
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
        """Place a ship on the board at the specified position and orientation.
        
        Args:
            pos (int): The starting position for ship placement.
            ship (Ship): The ship to place.
            orientation (Orientation): The orientation for placement.
            
        Returns:
            bool: True if the ship was successfully placed, False otherwise.
        """
        [valid, positions] = self.ship_placement(pos, ship, orientation)
        if not valid:
            return False
        for x in positions:
            self.grid.mark(x, ship.id)
        self.total_fleet_size += ship.size
        return True

    def place_fleet_randomly(self):
        """Randomly place all ships in the fleet on the board.
        
        Attempts to place each ship from the Fleet enum at random positions
        and orientations until all ships are successfully placed.
        """
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
        """Render the board with hits recognized.

        Displays the board state with ships shown and hits marked with
        the appropriate attack symbols.

        Returns:
            str: A string representation of the board showing ships and hits.
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
