#!/usr/bin/python3

from contextlib import redirect_stdout

with redirect_stdout(None):
    import pygame

from logic import Logic
from ui import UI

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()

    grid_size = (160, 90)
    window_size = (1920, 1080)

    logic = Logic(grid_size)
    ui = UI(logic, window_size)

    logic.running = True
    fps = 30
    ui.draw()
    clock.tick(fps)
    while logic.running:
        ui.handle_events()
        ui.draw()
        logic.progress()
        clock.tick(fps)
    pygame.quit()
