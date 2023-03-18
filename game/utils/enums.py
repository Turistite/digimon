from enum import Enum


# NOTE: there could be other actions
class Action(Enum):
    NOTHING = 1
    PAYMENT = 2
    AUCTION = 3
    PRISON = 4
    CHANCE = 5
    PENDING = 6


class Status(Enum):
    FREE = 1
    BOUGHT = 2
    MORTGAGED = 3
    SPECIAL = 4


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    PURPLE = 5
    WHITE = 6


PLAYER_COLORS = [
    Color.RED,
    Color.GREEN,
    Color.BLUE,
    Color.YELLOW,
    Color.PURPLE,
    Color.WHITE
]
