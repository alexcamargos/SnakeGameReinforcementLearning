from enum import Enum
from collections import namedtuple


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


Point = namedtuple('Point', 'x, y')

# RGB Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE1 = (0, 0, 128)
BLUE2 = (0, 0, 255)

BLOCK_SIZE = 20
SPEED = 20
