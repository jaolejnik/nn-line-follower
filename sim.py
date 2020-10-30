import os
from time import sleep

import pygame as pg
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from simulation.linefollower_sim import SimLineFollower

# ----- CONSTANTS -----
CURRENT_DIR = os.path.dirname(__file__)
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 1000
FPS = 60

pg.init()
clock = pg.time.Clock()


track = pg.image.load(os.path.join(CURRENT_DIR, "simulation/assets/track.png"))
track_size = track.get_size()
track = pg.transform.scale(track, (int(0.3 * track_size[0]), int(0.3 * track_size[1])))
track = pg.transform.flip(track, False, True)
display = pg.display.set_mode(track.get_size())
robot = SimLineFollower((150, track.get_size()[1] - 70), 0.5)

running = True


while running:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    display.blit(track, (0, 0))
    robot.draw(display)

    pixel_array = pg.PixelArray(track)
    robot.run(pixel_array)
    del pixel_array

    pg.display.update()

pg.quit()
