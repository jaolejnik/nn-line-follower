from utils.enums import ActiveSensors, DirectionX, DirectionY

from .linefollower import BaseLineFollower

FIND_TRACK_ACTIONS = [
    "Movement.move(DirectionY.FORWARD, self.base_speed, self.action_time*5)",
    "Movement.move(DirectionY.REVERSE, self.base_speed, self.action_time*5)",
    "Movement.rotate(DirectionX.RIGHT, self.base_speed, self.action_time)",
]


class ProgrammedLineFollower(BaseLineFollower):
    def __init__(self, base_speed, action_time):
        super().__init__(base_speed, action_time)

    def sharp_turn(self, direction_x):
        while not self.line_sensors.one_of_main_active():
            self.rotate(direction_x)

    def get_back_on_track(self):
        print("Get back on track")
        if self.last_active_line_sensor == ActiveSensors.RIGHT:
            while not self.line_sensors.one_or_more_active():
                self.rotate(DirectionX.RIGHT)

        if self.last_active_line_sensor == ActiveSensors.LEFT:
            while not self.line_sensors.one_or_more_active():
                self.rotate(DirectionX.LEFT)

        if self.last_active_line_sensor == ActiveSensors.BOTH_MAIN:
            while not self.line_sensors.one_or_more_active():
                self.move(DirectionY.REVERSE)

    def find_track(self):
        print("Find track")
        for action in FIND_TRACK_ACTIONS:
            if not self.lost:
                break
            eval(action)
            self.lost = not self.line_sensors.one_or_more_active()

    def follow_line(self):
        print("Follow line")
        if self.line_sensors.both_main_active():
            self.move(DirectionY.FORWARD)
            self.last_active_line_sensor = ActiveSensors.BOTH_MAIN

        if self.line_sensors.only_right_of_main_active():
            self.turn(DirectionX.RIGHT)
            self.last_active_line_sensor = ActiveSensors.RIGHT

        if self.line_sensors.only_left_of_main_active():
            self.turn(DirectionX.LEFT)
            self.last_active_line_sensor = ActiveSensors.LEFT

        if self.line_sensors.only_far_left_active():
            self.sharp_turn(DirectionX.LEFT)
            self.last_active_line_sensor = ActiveSensors.FAR_LEFT

        if self.line_sensors.only_far_right_active():
            self.sharp_turn(DirectionX.RIGHT)
            self.last_active_line_sensor = ActiveSensors.FAR_RIGHT

    def run(self):
        while self.collision_sensors.front_distance() > 5.0:
            if not self.lost:
                self.follow_line()
                if not self.line_sensors.one_or_more_active():
                    self.get_back_on_track()
                    self.lost = self.timer.countdown_to(3)
            else:
                self.find_track()
