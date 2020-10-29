import os

import numpy as np
import pygame as pg
from pygame.math import Vector2

CURRENT_DIR = os.path.dirname(__file__)


class SimLineSensors:
    def __init__(self, distance_form_center, robot_center, robot_angle):
        self.distance = distance_form_center
        self.set_positions(robot_center, robot_angle)

    def set_positions(self, robot_center, robot_angle):
        self.positions = []
        distance = self.distance
        offset_angle = 25
        for i in range(4):
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

    def far_left(self, pixel_array):
        return pixel_array[self.positions[0]] == 0

    def left(self, pixel_array):
        return pixel_array[self.positions[1]] == 0

    def right(self, pixel_array):
        return pixel_array[self.positions[2]] == 0

    def far_right(self, pixel_array):
        return pixel_array[self.positions[3]] == 0

    def get_readings(self, display):
        print(
            (
                self.far_left(display),
                self.left(display),
                self.right(display),
                self.far_right(display),
            )
        )
        return (
            self.far_left(display),
            self.left(display),
            self.right(display),
            self.far_right(display),
        )


class SimLineFollower:
    def __init__(self, position_tuple, scale):
        self.init_surface(scale)
        self.init_rect(position_tuple)
        self.angle = 0
        self.sensors = SimLineSensors(
            self.sensor_from_center_distance,
            self.rect.center,
            self.angle,
        )

    def draw(self, display):
        display.blit(self.surface_to_draw, self.rect)
        self.sensors.draw(display)

    def rotate(self):
        self.angle = (self.angle + 1) % 360
        self.surface_to_draw = pg.transform.rotozoom(self.surface, -self.angle, 1)
        self.rect = self.surface_to_draw.get_rect(center=self.rect.center)
        self.sensors.set_positions(self.rect.center, self.angle)

    def move(self):
        self.rect.center = Vector2(self.rect.center) + Vector2(5, 0).rotate(self.angle)
        self.sensors.set_positions(self.rect.center, self.angle)

    def turn(self):
        self.rotate()
        self.move()

    def init_surface(self, scale):
        print(os.path.join("assets", "robot.png"))
        surface = pg.image.load(os.path.join(CURRENT_DIR, "assets/robot.png"))
        size = surface.get_size()
        self.sensor_from_center_distance = size[0] / 4
        self.surface = pg.transform.scale(
            surface, (int(scale * size[0]), int(scale * size[1]))
        )
        self.surface_to_draw = self.surface

    def init_rect(self, position_tuple):
        self.rect = self.surface.get_rect()
        self.rect.center = position_tuple
