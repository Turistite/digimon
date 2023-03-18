from enum import Enum


class Action(Enum):
    NOTHING = 1
    PAYMENT = 2
    AUCTION = 3
    PRISON = 4
    CHANCHE = 5
    OTHER = 6 # todo add real ones
    PENDING = 7
