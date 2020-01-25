from enum import Enum
from collections import defaultdict

MAX_BOMB_RATIO = 0.5
MIN_WIDTH = 10
MAX_WIDTH = 100
MIN_HEIGHT = 10
MAX_HEIGHT = 100

class Spaces(Enum):
    UNKNOWN = -2
    BOMB = -1
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    FLAG = 9

    def __str__(self):
        if self.value == self.BOMB.value:
            return '*'
        if self.value == self.FLAG.value:
            return '?'
        if self.value == self.UNKNOWN.value or self.value == self.ZERO.value:
            return ''
        return str(self.value)