import os

import pygame as pg
from pygame.math import Vector2

from utils.enums import ActiveSensors, DirectionX, DirectionY
from utils.timer import Timer

from .sensors_sim import SimLineSensors

CURRENT_DIR = os.path.dirname(__file__)


class SimLineFollower:
    def __init__(self, position_tuple, scale):
        self._init_surface(scale)
        self._init_rect(position_tuple)
        self.angle = 0
        self.line_sensors = SimLineSensors(
            self.sensor_from_center_distance,
            self.rect.center,
            self.angle,
        )
        self.last_active_line_sensor = ActiveSensors.BOTH_MAIN.value

    def _init_surface(self, scale):
        surface = pg.image.load(os.path.join(CURRENT_DIR, "assets/robot.png"))
        size = surface.get_size()
        self.sensor_from_center_distance = size[0] / 4
        self.surface = pg.transform.scale(
            surface, (int(scale * size[0]), int(scale * size[1]))
        )
        self.surface_to_draw = self.surface

    def _init_rect(self, position_tuple):
        self.rect = self.surface.get_rect()
        self.rect.center = position_tuple

    def move(self, direction_y):
        if direction_y == DirectionY.FORWARD:
            distance = 5
        else:
            distance = -5
        self.rect.center = Vector2(self.rect.center) + Vector2(distance, 0).rotate(
            self.angle
        )
        self.line_sensors.set_positions(self.rect.center, self.angle)

    def rotate(self, direction_x):
        if direction_x == DirectionX.RIGHT:
            angle_change = 1
        else:
            angle_change = -1
        self.angle = (self.angle + angle_change) % 360
        self.surface_to_draw = pg.transform.rotozoom(self.surface, -self.angle, 1)
        self.rect = self.surface_to_draw.get_rect(center=self.rect.center)
        self.line_sensors.set_positions(self.rect.center, self.angle)

    def turn(self, direction_x):
        self.rotate(direction_x)
        self.move(DirectionY.FORWARD)

    def sharp_turn(self, direction_x, pixel_array):
        while not self.line_sensors.one_of_main_active():
            self.line_sensors.get_readings(pixel_array)
            self.rotate(direction_x)

    def get_back_on_track(self):
        if self.last_active_line_sensor == ActiveSensors.RIGHT:
            if not self.line_sensors.one_or_more_active():
                self.rotate(DirectionX.RIGHT)

        if self.last_active_line_sensor == ActiveSensors.LEFT:
            if not self.line_sensors.one_or_more_active():
                self.rotate(DirectionX.LEFT)

        if self.last_active_line_sensor == ActiveSensors.BOTH_MAIN:
            if not self.line_sensors.one_or_more_active():
                self.move(DirectionY.REVERSE)

    def follow_line(self, pixel_array):
        if self.line_sensors.both_main_active():
            self.move(DirectionY.FORWARD)
            self.last_active_line_sensor = ActiveSensors.BOTH_MAIN

        elif self.line_sensors.only_right_of_main_active():
            self.turn(DirectionX.RIGHT)
            self.last_active_line_sensor = ActiveSensors.RIGHT

        elif self.line_sensors.only_left_of_main_active():
            self.turn(DirectionX.LEFT)
            self.last_active_line_sensor = ActiveSensors.LEFT

        elif self.line_sensors.only_far_left_active():
            self.sharp_turn(DirectionX.LEFT, pixel_array)
            self.last_active_line_sensor = ActiveSensors.FAR_LEFT

        elif self.line_sensors.only_far_right_active():
            self.sharp_turn(DirectionX.RIGHT, pixel_array)
            self.last_active_line_sensor = ActiveSensors.FAR_RIGHT

        self.line_sensors.get_readings(pixel_array)

    def draw(self, display):
        display.blit(self.surface_to_draw, self.rect)
        self.line_sensors.draw(display)

    def run(self, pixel_array):
        self.follow_line(pixel_array)
        if not self.line_sensors.one_or_more_active():
            self.get_back_on_track()
