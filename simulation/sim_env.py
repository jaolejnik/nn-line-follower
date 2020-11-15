import os
from time import sleep

import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from simulation.linefollower_sim import SimLineFollower
from utils.enums import Actions, ActiveSensors, DirectionX, DirectionY

# ----- CONSTANTS -----
CURRENT_DIR = os.path.dirname(__file__)
FPS = 60


class SimEnv:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.font = pg.font.SysFont("Arial", 30)
        self.clock = pg.time.Clock()
        self._init_track()
        self.display = pg.display.set_mode(self.track.get_size())
        self.robot = SimLineFollower((150, self.track.get_size()[1] - 70), 0.5)
        self.state_memory_size = 15
        self.last_n_states = []

    def _init_track(self):
        track = pg.image.load(os.path.join(CURRENT_DIR, "assets/track_finish.png"))
        track_size = track.get_size()
        track = pg.transform.scale(
            track, (int(0.3 * track_size[0]), int(0.3 * track_size[1]))
        )
        self.track = pg.transform.flip(track, False, True)

    def reset(self):
        self.robot = SimLineFollower((150, self.track.get_size()[1] - 70), 0.5)
        return self.robot.line_sensors.state

    def save_state(self, state):
        if len(self.last_n_states) == self.state_memory_size:
            self.last_n_states.pop(0)
        self.last_n_states.append(state)

    def all_saved_states_eq(self, state):
        count = 0
        for saved_state in self.last_n_states:
            if saved_state == state.value:
                count += 1
        return count == self.state_memory_size

    def perform_action(self, action, pixel_array):
        if action == Actions.MOVE_FORWARD:
            self.robot.move(DirectionY.FORWARD)

        # elif action == Actions.MOVE_REVERSE:
        #     self.robot.move(DirectionY.REVERSE)

        elif action == Actions.TURN_LEFT:
            self.robot.turn(DirectionX.LEFT)

        elif action == Actions.TURN_RIGHT:
            self.robot.turn(DirectionX.RIGHT)

        elif action == Actions.ROTATE_LEFT:
            self.robot.rotate(DirectionX.LEFT)

        elif action == Actions.ROTATE_RIGHT:
            self.robot.rotate(DirectionX.RIGHT)

        self.robot.line_sensors.get_readings(pixel_array)

    def evaluate_action(self, state, action, last_active_sensor):
        reward = -5

        if state == ActiveSensors.NONE.value:
            reward = 0

        elif state == ActiveSensors.BOTH_MAIN.value and action == Actions.MOVE_FORWARD:
            reward = 15

        elif state == ActiveSensors.LEFT.value and action == Actions.TURN_LEFT:
            reward = 10

        elif (
            state in [ActiveSensors.RIGHT.value, ActiveSensors.BOTH_RIGHT.value]
            and action == Actions.TURN_RIGHT
        ):
            reward = 10

        elif (
            state in [ActiveSensors.FAR_LEFT.value, ActiveSensors.BOTH_LEFT.value]
            or last_active_sensor == ActiveSensors.FAR_LEFT
        ) and action == Actions.ROTATE_LEFT:
            reward = 20

        elif (
            state in [ActiveSensors.FAR_RIGHT.value, ActiveSensors.BOTH_RIGHT.value]
            or last_active_sensor == ActiveSensors.FAR_RIGHT
        ) and action == Actions.ROTATE_RIGHT:
            reward = 20

        return reward

    def step(self, action, episode_info):
        self.clock.tick(FPS)

        pixel_array = pg.PixelArray(self.track)
        self.perform_action(action, pixel_array)
        del pixel_array

        text = self.font.render(
            f"Episode: {episode_info[0]}"
            + f"    Step: {episode_info[1]}"
            + f"    Current reward: {episode_info[2]}",
            True,
            (0, 0, 0),
        )

        self.display.blit(self.track, (0, 0))
        self.display.blit(text, (0, 0))
        self.robot.draw(self.display)

        pg.display.update()

        self.save_state(self.robot.line_sensors.state)

        reward = self.evaluate_action(
            self.robot.line_sensors.state,
            action,
            self.robot.last_active_line_sensor,
        )

        done = self.robot.line_sensors.finish or self.all_saved_states_eq(
            ActiveSensors.NONE
        )

        return self.robot.line_sensors.state, reward, done

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                elif event.type == QUIT:
                    running = False

            self.display.blit(self.track, (0, 0))
            self.robot.draw(self.display)

            running = not self.robot.line_sensors.finish

            pixel_array = pg.PixelArray(self.track)
            self.robot.run(pixel_array)
            del pixel_array

            pg.display.update()

        pg.quit()
