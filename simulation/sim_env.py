import os
from time import sleep

import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from simulation.linefollower_sim import SimLineFollower
from utils.enums import Actions, DirectionX, DirectionY

# ----- CONSTANTS -----
CURRENT_DIR = os.path.dirname(__file__)
FPS = 60


class SimEnv:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.init_track()
        self.display = pg.display.set_mode(self.track.get_size())
        self.robot = SimLineFollower((150, self.track.get_size()[1] - 70), 0.5)
        self.running = True

    def step(self, action):
        self.clock.tick(FPS)

        self.display.blit(self.track, (0, 0))
        self.robot.draw(self.display)

        pixel_array = pg.PixelArray(self.track)
        self.perform_action(action, pixel_array)
        del pixel_array

        pg.display.update()

    def perform_action(self, action, pixel_array):
        if action == Actions.MOVE_FORWARD:
            self.robot.move(DirectionY.FORWARD)

        elif action == Actions.MOVE_REVERSE:
            self.robot.move(DirectionY.REVERSE)

        elif action == Actions.TURN_LEFT:
            self.robot.turn(DirectionX.LEFT)

        elif action == Actions.TURN_RIGHT:
            self.robot.turn(DirectionX.RIGHT)

        elif action == Actions.SHARP_TURN_LEFT:
            self.robot.sharp_turn(DirectionX.LEFT)

        elif action == Actions.SHARP_TURN_RIGHT:
            self.robot.sharp_turn(DirectionX.RIGHT)
        elif action == Actions.GET_BACK_ON_TRACK:
            self.robot.get_back_on_track()

        self.robot.line_sensors.get_readings(pixel_array)

    def reset(self):
        self.robot = SimLineFollower((150, self.track.get_size()[1] - 70), 0.5)

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

                elif event.type == QUIT:
                    self.running = False

            self.display.blit(self.track, (0, 0))
            self.robot.draw(self.display)

            pixel_array = pg.PixelArray(self.track)
            self.robot.run(pixel_array)
            del pixel_array

            pg.display.update()

        pg.quit()

    def init_track(self):
        track = pg.image.load(os.path.join(CURRENT_DIR, "assets/track.png"))
        track_size = track.get_size()
        track = pg.transform.scale(
            track, (int(0.3 * track_size[0]), int(0.3 * track_size[1]))
        )
        self.track = pg.transform.flip(track, False, True)
