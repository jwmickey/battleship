"""Utility classes and constants for the battleship game.

This module contains enumerations, named tuples, and constants used throughout
the battleship game including ship definitions, game modes, directions, and
attack result types.
"""

from collections import namedtuple
from enum import Enum


Ship = namedtuple('Ship', ['size', 'id'])
"""A named tuple representing a battleship.

Attributes:
    size (int): The length of the ship in grid cells.
    id (str): A single character identifier for the ship.
"""

ShipPlacement = namedtuple('ShipPlacement', ['valid', 'positions'])
"""A named tuple representing the result of attempting to place a ship.

Attributes:
    valid (bool): Whether the ship placement is valid.
    positions (list): List of grid positions the ship would occupy.
"""

Neighbors = namedtuple('Neighbors', ['UP', 'DOWN', 'LEFT', 'RIGHT'])
"""A named tuple representing the neighboring positions of a grid cell.

Attributes:
    UP (int or None): Position above, None if at top edge.
    DOWN (int or None): Position below, None if at bottom edge.
    LEFT (int or None): Position to the left, None if at left edge.
    RIGHT (int or None): Position to the right, None if at right edge.
"""


class GameMode(Enum):
    """Enumeration of available game modes.
    
    Attributes:
        SP: Single player mode (human vs AI).
        CPU: CPU vs CPU mode (AI vs AI).
    """
    SP = 'Single Player'
    CPU = 'CPU vs CPU'


class Direction(Enum):
    """Enumeration of cardinal directions for grid navigation.
    
    Attributes:
        UP: Move up on the grid.
        DOWN: Move down on the grid.
        LEFT: Move left on the grid.
        RIGHT: Move right on the grid.
    """
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class Orientation(Enum):
    """Enumeration of ship orientations for placement.
    
    Attributes:
        VERTICAL: Ship placed vertically (up-down).
        HORIZONTAL: Ship placed horizontally (left-right).
    """
    VERTICAL = 'V'
    HORIZONTAL = 'H'


class Fleet(Enum):
    """Enumeration of ships in a battleship fleet.
    
    Each ship has a specific size and single-character identifier.
    
    Attributes:
        CARRIER: Aircraft carrier (5 cells, ID: 'A').
        BATTLESHIP: Battleship (4 cells, ID: 'B').
        CRUISER: Cruiser (3 cells, ID: 'C').
        SUBMARINE: Submarine (3 cells, ID: 'S').
        DESTROYER: Destroyer (2 cells, ID: 'D').
    """
    CARRIER = Ship(5, 'A')
    BATTLESHIP = Ship(4, 'B')
    CRUISER = Ship(3, 'C')
    SUBMARINE = Ship(3, 'S')
    DESTROYER = Ship(2, 'D')


class Player(Enum):
    """Enumeration of players in the game.
    
    Attributes:
        ONE: Player one (human or first AI).
        TWO: Player two (AI or second AI).
    """
    ONE = 1
    TWO = 2


class Attack(Enum):
    """Enumeration of attack result types.
    
    Attributes:
        MISS: Attack missed (hit water).
        HIT: Attack hit a ship.
        SINK: Attack sunk a ship.
        WIN: Attack resulted in winning the game.
        INVALID: Invalid attack position.
    """
    MISS = '_'
    HIT = 'X'
    SINK = 'S'
    WIN = 'W'
    INVALID = 'i'


class KeyPad(Enum):
    """Enumeration of keyboard input codes for game controls.
    
    Maps keyboard input to numeric codes for game interaction.
    
    Attributes:
        ENTER: Enter key code.
        DOWN: Down arrow key code.
        UP: Up arrow key code.
        LEFT: Left arrow key code.
        RIGHT: Right arrow key code.
    """
    ENTER = 10
    DOWN = 258
    UP = 259
    LEFT = 260
    RIGHT = 261


DPad = {
    KeyPad.UP.value: Direction.UP,
    KeyPad.DOWN.value: Direction.DOWN,
    KeyPad.LEFT.value: Direction.LEFT,
    KeyPad.RIGHT.value: Direction.RIGHT
}
"""Dictionary mapping keyboard input codes to movement directions.

Maps KeyPad enum values to Direction enum values for directional movement
in the game interface.
"""
