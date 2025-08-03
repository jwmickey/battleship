"""Human player implementation for the battleship game.

This module implements the Human class, which represents a human player
that uses keyboard input to control their attacks in the battleship game.
"""

from src.grid import Grid
from src.player import Player
from src.utils import Attack, DPad, Direction, KeyPad


class Human(Player):
    """Human player that uses keyboard input for game control.
    
    The Human class extends Player to provide keyboard-based interaction,
    allowing a human player to move a cursor around the attack grid and
    select positions to attack.
    
    Attributes:
        grid (Grid): The player's attack grid showing hits and misses.
        get_input (callable): Function to get keyboard input.
        redraw (callable): Function to redraw the game display.
        pos (int): Current cursor position on the grid.
        covered_val (str): The value covered by the cursor.
    """
    
    def __init__(self, grid: Grid, get_input, redraw):
        """Initialize a human player.
        
        Args:
            grid (Grid): The grid for tracking attacks made by this player.
            get_input (callable): Function that returns keyboard input codes.
            redraw (callable): Function to refresh the game display.
        """
        super().__init__(grid)
        self.get_input = get_input
        self.redraw = redraw
        self.reset()

    def reset(self):
        """Reset the human player to initial state.
        
        Resets the grid, positions the cursor at the top-left corner,
        and refreshes the display.
        """
        self.grid.reset()
        self.pos = 0
        self.covered_val = self.grid.val(self.pos)
        self.grid.mark(self.pos, '+')
        self.redraw()

    def get_attack_pos(self) -> int:
        """Get the attack position from human keyboard input.
        
        Waits for keyboard input and handles cursor movement with arrow keys
        or attack selection with Enter or 'f'.
        
        Returns:
            int: The grid position to attack when Enter or 'f' is pressed.
        """
        while True:
            key = self.get_input()
            if key == KeyPad.ENTER.value or key == ord('f'):
                return self.pos
            elif key in DPad:
                self.move(DPad[key])

    def handle_attack_result(self, pos: int, result: Attack):
        """Handle the result of an attack by updating the grid display.
        
        Updates the grid with the attack result and refreshes the display.
        
        Args:
            pos (int): The position that was attacked.
            result (Attack): The result of the attack (hit or miss).
        """
        self.grid.mark(pos, Attack.MISS.value if result ==
                       Attack.MISS else Attack.HIT.value)
        self.covered_val = self.grid.val(pos)
        self.redraw()

    def move(self, dir: Direction):
        """Move the cursor in the specified direction.
        
        Finds the next valid position in the given direction and moves
        the cursor there, updating the display accordingly.
        
        Args:
            dir (Direction): The direction to move (UP, DOWN, LEFT, RIGHT).
        """
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
