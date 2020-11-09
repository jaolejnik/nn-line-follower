from enum import Enum, IntEnum


class DirectionX(IntEnum):
    LEFT = 0
    RIGHT = 1


class DirectionY(IntEnum):
    REVERSE = 0
    FORWARD = 1


class ActiveSensors(Enum):
    ALL = (1, 1, 1, 1)
    NONE = (0, 0, 0, 0)
    FAR_LEFT = (1, 0, 0, 0)
    LEFT = (0, 1, 0, 0)
    RIGHT = (0, 0, 1, 0)
    FAR_RIGHT = (0, 0, 0, 1)
    BOTH_MAIN = (0, 1, 1, 0)
    BOTH_LEFT = (1, 1, 0, 0)
    BOTH_RIGHT = (0, 0, 1, 1)
    BOTH_FAR = (1, 0, 0, 1)
    FAR_LEFT_RIGHT = (1, 0, 1, 0)
    FAR_RIGHT_LEFT = (0, 1, 0, 1)
    LEFT_INACTIVE = (1, 0, 1, 1)
    RIGHT_INACTIVE = (1, 1, 0, 1)
    FAR_RIGHT_INACTIVE = (1, 1, 1, 0)
    FAR_LEFT_INACTIVE = (0, 1, 1, 1)


class Actions(Enum):
    MOVE_FORWARD = "move forward"
    # MOVE_REVERSE = "move reverse"
    TURN_LEFT = "turn left"
    TURN_RIGHT = "turn right"
    ROTATE_LEFT = "rotate left"
    ROTATE_RIGHT = "rotate right"
    # SHARP_TURN_LEFT = "sharp turn left"
    # SHARP_TURN_RIGHT = "sharp turn right"
    # GET_BACK_ON_TRACK = "get back on track"
