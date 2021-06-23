from collections import namedtuple
from enum import Enum


Ship = namedtuple('Ship', ['size', 'id'])
ShipPlacement = namedtuple('ShipPlacement', ['valid', 'positions'])
Neighbors = namedtuple('Neighbors', ['UP', 'DOWN', 'LEFT', 'RIGHT'])


class GameMode(Enum):
    SP = 'Single Player'
    CPU = 'CPU vs CPU'


class Direction(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class Orientation(Enum):
    VERTICAL = 'V'
    HORIZONTAL = 'H'


class Fleet(Enum):
    CARRIER = Ship(5, 'A')
    BATTLESHIP = Ship(4, 'B')
    CRUISER = Ship(3, 'C')
    SUBMARINE = Ship(3, 'S')
    DESTROYER = Ship(2, 'D')


class Player(Enum):
    ONE = 1
    TWO = 2


class Attack(Enum):
    MISS = '_'
    HIT = 'X'
    SINK = 'S'
    WIN = 'W'


class KeyPad(Enum):
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
