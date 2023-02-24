from contextlib import redirect_stdout

with redirect_stdout(None):
    import pygame

from logic import Logic


class UI:
    """graphical user interface for game of life"""

    def __init__(self, logic: Logic, window_size: tuple[int, int]) -> None:
        self.logic = logic

        self.scale_constants = {
            "window_size": window_size,
            "scaled_size": (0, 0),
            "inset_position": (0, 0),
        }

        self.screen = pygame.display.set_mode(
            self.scale_constants["window_size"], pygame.RESIZABLE
        )
        self.screen.fill((255, 127, 0))

        self.calculate_scaling()
        self.small_surface = pygame.Surface(self.logic.grid_size)
        self.pxgrid = pygame.PixelArray(self.small_surface)

        self.fullscreen = False

    def calculate_scaling(self) -> None:
        """
        calculate some constants for drawing the game
        at the right scale in the right position in the window
        """
        grid_size = self.logic.grid_size
        window_size = self.scale_constants["window_size"]
        if window_size[0] / grid_size[0] <= window_size[1] / grid_size[1]:
            self.scale_constants["scaled_size"] = (
                window_size[0],
                window_size[0] * grid_size[1] / grid_size[0],
            )
        else:
            self.scale_constants["scaled_size"] = (
                window_size[1] * grid_size[0] / grid_size[1],
                window_size[1],
            )

        self.scale_constants["inset_position"] = (
            window_size[0] / 2 - self.scale_constants["scaled_size"][0] / 2,
            window_size[1] / 2 - self.scale_constants["scaled_size"][1] / 2,
        )

    def toggle_fullscreen(self) -> None:
        """change between fullscreen and windowed display modes"""
        if self.fullscreen:
            self.screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
            self.fullscreen = False
        else:
            self.screen = pygame.display.set_mode(
                (0, 0), pygame.RESIZABLE | pygame.FULLSCREEN
            )
            self.fullscreen = True

        self.scale_constants["window_size"] = self.screen.get_size()
        self.calculate_scaling()

        self.screen.fill((255, 127, 0))
        pygame.display.update()

    def handle_events(self) -> None:
        """
        handle pygame events
        such as key presses, window resizing and clicks
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logic.stop()

            elif event.type == pygame.VIDEORESIZE:
                self.scale_constants["window_size"] = event.size
                self.calculate_scaling()

                if self.fullscreen:
                    self.screen = pygame.display.set_mode(
                        self.scale_constants["window_size"],
                        pygame.RESIZABLE | pygame.FULLSCREEN,
                    )
                else:
                    self.screen = pygame.display.set_mode(
                        self.scale_constants["window_size"], pygame.RESIZABLE
                    )
                self.screen.fill((255, 127, 0))
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # - check if click falls within game area
                inset_position = self.scale_constants["inset_position"]
                scaled_size = self.scale_constants["scaled_size"]
                grid_size = self.logic.grid_size
                if (
                    pos[0] >= inset_position[0]
                    and pos[0] < inset_position[0] + scaled_size[0]
                    and pos[1] >= inset_position[1]
                    and pos[1] < inset_position[1] + scaled_size[1]
                ):
                    self.logic.change(
                        int(
                            (pos[0] - inset_position[0])
                            / (scaled_size[0] / grid_size[0])
                        ),
                        int(
                            (pos[1] - inset_position[1])
                            / (scaled_size[1] / grid_size[1])
                        ),
                    )
                else:
                    self.logic.toggle_pause()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.logic.stop()

                elif event.key == pygame.K_SPACE:
                    self.logic.toggle_pause()

                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()

                elif event.key == pygame.K_BACKSPACE:
                    self.logic.generate_empty_grid()

                elif event.key == pygame.K_r:
                    self.logic.generate_random_grid()

                elif event.key == pygame.K_g:
                    self.logic.generate_glider_grid()

                elif event.key == pygame.K_f:
                    self.logic.generate_alternating_glider_grid()

                elif event.key == pygame.K_s:
                    self.logic.generate_spaceship_grid()

                elif event.key == pygame.K_a:
                    self.logic.generate_rectangle()

                if self.logic.paused:
                    if event.key == pygame.K_1:
                        self.logic.progress_steps += 1
                    elif event.key == pygame.K_2:
                        self.logic.progress_steps += 2
                    elif event.key == pygame.K_3:
                        self.logic.progress_steps += 3
                    elif event.key == pygame.K_4:
                        self.logic.progress_steps += 4
                    elif event.key == pygame.K_5:
                        self.logic.progress_steps += 5
                    elif event.key == pygame.K_6:
                        self.logic.progress_steps += 6
                    elif event.key == pygame.K_7:
                        self.logic.progress_steps += 7
                    elif event.key == pygame.K_8:
                        self.logic.progress_steps += 8
                    elif event.key == pygame.K_9:
                        self.logic.progress_steps += 9
                    elif event.key == pygame.K_0:
                        self.logic.progress_steps = 0

            if self.logic.paused and pygame.key.get_pressed()[pygame.K_p]:
                self.logic.progress_steps = 2

    def draw(self) -> None:
        """draw the game state to the window surface"""
        state = self.logic.get_state()
        self.small_surface.fill(0x000000)
        for x in range(self.logic.grid_size[0]):
            for y in range(self.logic.grid_size[1]):
                if state[x][y]:
                    self.pxgrid[x, y] = 0xFFFFFF  # type: ignore
        # - draw a scaled version of the one pixel per cell surface to the screen
        scaled_size = self.scale_constants["scaled_size"]
        inset_position = self.scale_constants["inset_position"]
        self.screen.blit(
            pygame.transform.scale(
                self.small_surface, (int(scaled_size[0]), int(scaled_size[1]))
            ),
            (int(inset_position[0]), int(inset_position[1])),
        )
        pygame.display.update()
