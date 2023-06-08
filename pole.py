import random

from CONST import *


class Pole:
    def __init__(self, pos):
        self.val = random.randint(POLES_VALUE_RANGE.x, POLES_VALUE_RANGE.y)
        self.pos = pos
        self.state = 0