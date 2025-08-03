"""Base player class for the battleship game.

This module defines the abstract Player class that serves as the base
for both human and AI players in the battleship game.
"""

from src.utils import Attack
from src.grid import Grid
from src.utils import Attack


class Player():
    """Abstract base class for players in the battleship game.
    
    This class defines the interface that all player types (human, AI)
    must implement to participate in the game.
    
    Attributes:
        grid (Grid): The player's attack grid showing hits and misses.
    """
    
    def __init__(self, grid: Grid):
        """Initialize a player with an attack grid.
        
        Args:
            grid (Grid): The grid for tracking attacks made by this player.
        """
        self.grid = grid

    def reset(self):
        """Reset the player to initial state.
        
        This method should be overridden by subclasses to provide
        player-specific reset behavior.
        """
        pass

    def get_attack_pos(self) -> int:
        """Get the position for the next attack.
        
        This method must be implemented by subclasses to define how
        the player selects attack positions.
        
        Returns:
            int: The grid position to attack.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError

    def handle_attack_result(self, pos: int, result: Attack):
        """Handle the result of an attack.
        
        This method must be implemented by subclasses to define how
        the player processes attack results.
        
        Args:
            pos (int): The position that was attacked.
            result (Attack): The result of the attack.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError
