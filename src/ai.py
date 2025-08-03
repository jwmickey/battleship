"""AI player implementation for the battleship game.

This module implements the Ai class, which represents a computer player
that uses intelligent algorithms to play battleship, including ship tracking
and directional attacking strategies.
"""

import random
from src.grid import Grid
from src.player import Player
from src.utils import Attack, Direction, Orientation


class Ai(Player):
    """AI player that uses strategic algorithms for battleship gameplay.
    
    The AI implements smart targeting strategies including:
    - Random initial targeting with neighbor checking
    - Ship tracking after successful hits
    - Directional pursuit once ship orientation is determined
    - Direction reversal when reaching ship ends
    
    Attributes:
        grid (Grid): The AI's attack grid showing hits and misses.
        last_hit (int or None): Position of the most recent hit.
        last_hit_origin (int or None): Position of the first hit on current ship.
        direction (Direction or None): Current pursuit direction.
        ship_orientation (Orientation or None): Determined ship orientation.
        has_reversed (bool): Whether direction has been reversed for current ship.
        finished (bool): Whether the game is finished.
    """
    
    def __init__(self, grid: Grid):
        """Initialize an AI player.
        
        Args:
            grid (Grid): The grid for tracking attacks made by this player.
        """
        super().__init__(grid)
        self.reset()

    def get_attack_pos(self) -> int:
        """Get the next attack position using AI strategy.
        
        Uses intelligent targeting:
        1. If tracking a ship, continue in pursuit direction
        2. Otherwise, randomly select positions with open neighbors
        3. Mark invalid positions and retry if needed
        
        Returns:
            int: The grid position to attack, or None if no valid moves.
        """
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
        """Handle the result of an attack and update AI state.
        
        Updates the grid and AI tracking state based on attack results:
        - HIT: Begin or continue ship tracking
        - SINK: Reset ship tracking
        - MISS: Adjust strategy based on current state
        
        Args:
            pos (int): The position that was attacked.
            result (Attack): The result of the attack.
        """
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
        """Reset the AI player to initial state.
        
        Resets both the grid and all ship tracking variables.
        """
        self.grid.reset()
        self.reset_ship_tracking()

    def reset_ship_tracking(self):
        """Reset all ship tracking variables to None/default state.
        
        Called when a ship is sunk or when starting fresh.
        """
        self.last_hit = None
        self.last_hit_origin = None
        self.direction = None
        self.ship_orientation = None
        self.has_reversed = False

    def valid_moves_from(self, pos):
        """Get valid attack positions adjacent to the given position.
        
        Args:
            pos (int): The grid position to check neighbors of.
            
        Returns:
            list: List of tuples containing (Direction, position) for valid moves.
        """
        grid = self.grid
        neighbors = grid.neighbors(pos)
        moves = []
        for dir in neighbors._fields:
            pos = getattr(neighbors, dir)
            if pos is not None and grid.val(pos) == grid.initial_char:
                moves.append((Direction[dir], pos))
        return moves

    def set_ship_orientation(self):
        """Determine and set the ship orientation based on current direction.
        
        Sets the ship_orientation attribute based on the current direction
        of attack pursuit.
        """
        if self.direction == Direction.UP or self.direction == Direction.DOWN:
            self.ship_orientation = Orientation.VERTICAL
        elif self.direction == Direction.LEFT or self.direction == Direction.RIGHT:
            self.ship_orientation = Orientation.HORIZONTAL
        else:
            self.ship_orientation = None

    def reverse_direction(self):
        """Reverse the current pursuit direction.
        
        Used when reaching the end of a ship to attack from the other direction.
        Sets has_reversed flag to prevent infinite reversal.
        """
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

    def next_best_direction(self, pos):
        """Determine the best initial direction for attacking from a position.
        
        Uses simple heuristics based on position to avoid edge cases.
        
        Args:
            pos (int): The grid position to analyze.
            
        Returns:
            Direction or None: The recommended direction, or None if no preference.
        """
        [x, y] = self.grid.coords(pos)
        if y < 2 or y > 7:
            return Direction.LEFT if x >= 5 else Direction.RIGHT
        if x < 2 or x > 7:
            return Direction.UP if y >= 5 else Direction.DOWN
        return None

    def next_in_direction(self):
        """Get the next position to attack in the current direction.
        
        Returns:
            int or None: The next position to attack, or None if no valid position.
        """
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
        """Determine the next target position using ship tracking logic.
        
        Returns:
            int or None: The next position to attack, or None if no valid target.
        """
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
        """Check if a position has any empty neighboring cells.
        
        Args:
            pos (int): The grid position to check.
            
        Returns:
            bool: True if the position has at least one empty neighbor.
        """
        neighbors = self.grid.neighbors(pos)
        return len([x for x in neighbors if x is not None and self.grid.val(x) == self.grid.initial_char]) > 0
