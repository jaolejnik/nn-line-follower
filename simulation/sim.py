from time import sleep

import pygame
from linefollower_sim import SimLineFollower
from pygame.locals import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN, QUIT

pygame.init()
clock = pygame.time.Clock()

# ----- CONSTANTS -----
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 1000
FPS = 30


running = True
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
robot = SimLineFollower((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2), 0.5)
display_surface = pygame.display.get_surface()


while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    display.fill((0, 0, 0))
    pixel_array = pygame.PixelArray(display_surface)
    robot.sensors.get_readings(pixel_array)
    del pixel_array
    robot.draw(display)
    robot.rotate()

    pygame.display.update()

pygame.quit()
