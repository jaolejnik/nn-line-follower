from enum import Enum
from time import sleep

from utils.timer import Timer

from .basic_movement import DirectionX, DirectionY, Movement
from .manager import MovementManager
from .sensors import CollisionSensors, LineSensors

FIND_TRACK_ACTIONS = [
    "Movement.move(DirectionY.FORWARD, self.base_speed, self.action_time*5)",
    "Movement.move(DirectionY.REVERSE, self.base_speed, self.action_time*5)",
    "Movement.rotate(DirectionX.RIGHT, self.base_speed, self.action_time*5)",
    # "sleep(self.action_time*5)",
]


class ActiveSensor(Enum):
    LEFT = (1, 0)
    RIGHT = (0, 1)
    BOTH = (1, 1)


class LineFollower:
    def __init__(self, base_speed, action_time):
        self.base_speed = base_speed
        self.action_time = action_time

        self.line_sensors = LineSensors
        self.collision_sensors = CollisionSensors
        self.last_active_line_sensor = ActiveSensor.BOTH
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

    def get_back_on_track(self):
        if self.last_active_line_sensor == ActiveSensor.RIGHT:
            while not self.line_sensors.one_or_more_active():
                self.rotate(DirectionX.RIGHT)

        if self.last_active_line_sensor == ActiveSensor.LEFT:
            while not self.line_sensors.one_or_more_active():
                self.rotate(DirectionX.LEFT)

        if self.last_active_line_sensor == ActiveSensor.BOTH:
            while not self.line_sensors.one_or_more_active():
                self.move(DirectionY.REVERSE)

    def find_track(self):
        for action in FIND_TRACK_ACTIONS:
            if not self.lost:
                break
            eval(action)
            self.lost = not self.line_sensors.one_or_more_active()

    def follow_line(self):
        if self.line_sensors.both_active():
            self.move(DirectionY.FORWARD)
            self.last_active_line_sensor = ActiveSensor.BOTH

        if self.line_sensors.only_right_active():
            self.turn(DirectionX.RIGHT)
            self.last_active_line_sensor = ActiveSensor.RIGHT

        if self.line_sensors.only_left_active():
            self.turn(DirectionX.LEFT)
            self.last_active_line_sensor = ActiveSensor.LEFT

    def run(self):
        while True:
            if not self.lost:
                self.follow_line()
                if not self.line_sensors.one_or_more_active():
                    self.get_back_on_track()
                    self.lost = self.timer.countdown_to(3)
            else:
                self.find_track()
