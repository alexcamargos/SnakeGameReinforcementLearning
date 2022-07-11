from collections import namedtuple
from enum import Enum


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

Point = namedtuple('Point', 'x, y')

# RGB Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE1 = (0, 0, 128)
BLUE2 = (0, 0, 255)

BLOCK_SIZE = 20
SPEED_FOR_HUMAN = 20
SPEED_FOR_AI = SPEED_FOR_HUMAN * 4
