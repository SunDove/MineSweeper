from enum import Enum


MAX_BOMB_RATIO = 0.5
MIN_WIDTH = 10
MAX_WIDTH = 100
MIN_HEIGHT = 10
MAX_HEIGHT = 100

class Spaces(Enum):
    BOMB = -1
    UNKNOWN = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7,
    FLAG = 8
