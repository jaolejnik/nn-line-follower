import pygame as pg
from pygame.math import Vector2


class SimLineSensors:
    def __init__(self, distance_form_center, robot_center, robot_angle):
        self.distance = distance_form_center
        self.set_positions(robot_center, robot_angle)
        self.state = (0, 1, 1, 0)
        self.finish = False

    def set_positions(self, robot_center, robot_angle):
        self.positions = []
        offset_angle = 25
        for i in range(4):
            distance = 0.95 * self.distance if i in [0, 3] else self.distance
            sensor = robot_center + Vector2(distance, 0).rotate(
                robot_angle - offset_angle
            )
            self.positions.append(tuple(map(int, sensor)))
            if i == 1:
                offset_angle -= 14
            else:
                offset_angle -= 20

    def draw(self, display):
        for sensor_pos in self.positions:
            pg.draw.circle(display, (0, 0, 0), sensor_pos, 1)

    def far_left(self):
        return self.state[0]

    def left(self):
        return self.state[1]

    def right(self):
        return self.state[2]

    def far_right(self):
        return self.state[3]

    def only_left_active(self):
        return (
            self.left()
            and not self.right()
            and not self.far_left()
            and not self.far_right()
        )

    def only_left_of_main_active(self):
        return self.left() and not self.right()

    def only_far_left_active(self):
        return (
            self.far_left()
            and not self.left()
            and not self.right()
            and not self.far_right()
        )

    def only_right_active(self):
        return (
            self.right()
            and not self.left()
            and not self.far_left()
            and not self.far_right()
        )

    def only_right_of_main_active(self):
        return self.right() and not self.left()

    def only_far_right_active(self):
        return (
            self.far_right()
            and not self.left()
            and not self.right()
            and not self.far_left()
        )

    def one_or_more_active(self):
        return self.far_left() or self.left() or self.right() or self.far_right()

    def one_of_main_active(self):
        return self.left() or self.right()

    def both_main_active(self):
        return self.left() and self.right()

    def is_finish(self, pixel_array):
        for i in range(4):
            if pixel_array[self.positions[i]] == 4278255360:
                self.finish = True

    def get_readings(self, pixel_array):
        try:
            self.state = tuple(
                [pixel_array[self.positions[i]] == 4278190080 for i in range(4)]
            )
            self.is_finish(pixel_array)
        except IndexError:
            self.finish = True
