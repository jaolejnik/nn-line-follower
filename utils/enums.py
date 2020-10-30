from enum import Enum, IntEnum


class DirectionX(IntEnum):
    LEFT = 0
    RIGHT = 1


class DirectionY(IntEnum):
    REVERSE = 0
    FORWARD = 1


class ActiveSensor(Enum):
    NONE = (0, 0, 0, 0)
    FAR_LEFT = (1, 0, 0, 0)
    LEFT = (0, 1, 0, 0)
    RIGHT = (0, 0, 1, 0)
    FAR_RIGHT = (0, 0, 0, 1)
    BOTH_MAIN = (0, 1, 1, 0)
