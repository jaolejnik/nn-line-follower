from utils.enums import ActiveSensors, DirectionX, DirectionY
from utils.timer import Timer

from .basic_movement import Movement
from .manager import MovementManager
from .sensors import CollisionSensors, LineSensors


class BaseLineFollower:
    def __init__(self, base_speed, action_time):
        self.base_speed = base_speed
        self.action_time = action_time

        self.line_sensors = LineSensors
        self.collision_sensors = CollisionSensors
        self.last_active_line_sensor = ActiveSensors.BOTH_MAIN
        self.lost = False
        self.action_manager = MovementManager()
        self.timer = Timer()
        self.time_since_lost_line = 0

    def move(self, direction_y):
        self.action_manager.add_and_save_action(
            Movement.move,
            direction_y=direction_y,
            speed=self.base_speed,
            time=self.action_time,
        )

    def turn(self, direction_x):
        self.action_manager.add_and_save_action(
            Movement.turn,
            direction_x=direction_x,
            direction_y=DirectionY.FORWARD,
            speed=self.base_speed,
            sharpness=0.5,
            time=self.action_time,
        )

    def rotate(self, direction_x):
        self.action_manager.add_and_save_action(
            Movement.rotate,
            direction_x=direction_x,
            speed=self.base_speed,
            time=self.action_time,
        )
