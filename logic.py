from random import randint


class Logic:
    """logic and data operations for game of life"""

    def __init__(self, grid_size: tuple[int, int]) -> None:
        self.grid_size = grid_size
        self.grid = []
        self.generate_random_grid()

        self.running = False
        self.paused = False
        self.progress_steps = 0

    def generate_random_grid(self) -> None:
        """generate random grid state"""
        self.grid = [
            [bool(randint(0, 1)) for y in range(self.grid_size[1])]
            for x in range(self.grid_size[0])
        ]

    def rule(self, x: int, y: int) -> bool:
        """apply the rules of the game of life to a single cell"""
        # - map the coordinates of the neighbouring cells, including edge wrapping
        if not (x < 1 or x > len(self.grid) - 2):
            x_neighbours = (x - 1, x, x + 1)
        else:
            if x < 1:
                x_neighbours = (-1, x, x + 1)
            else:
                x_neighbours = (x - 1, x, 0)
        if not (y < 1 or y > len(self.grid[0]) - 2):
            y_neighbours = (y - 1, y, y + 1)
        else:
            if y < 1:
                y_neighbours = (-1, y, y + 1)
            else:
                y_neighbours = (y - 1, y, 0)

        # - count number of alive cells in neighbouring cells
        alive = 0
        for i in x_neighbours:
            for j in y_neighbours:
                if (x, y) != (i, j) and self.grid[i][j]:
                    alive += 1

        # - condensed implementation of the classic rules
        return bool(alive == 3 or (self.grid[x][y] and alive == 2))

    def progress(self) -> None:
        """apply the game of life rule to every cell in the grid iteratively"""
        # - only run if the game isn't paused, or is set to progress a certain number of states
        if not self.paused or self.progress_steps:
            new_grid = [
                [self.rule(x, y) for y in range(self.grid_size[1])]
                for x in range(self.grid_size[0])
            ]
            self.grid = new_grid
            if self.progress_steps:
                self.progress_steps -= 1

    def get_state(self) -> list[list[bool]]:
        """get state of game"""
        return self.grid

    def stop(self) -> None:
        """stop game"""
        self.running = False

    def toggle_pause(self) -> None:
        """pause or resume the game"""
        self.paused = False if self.paused else True
        self.progress_steps = 0

    def change(self, x: int, y: int) -> None:
        """change the state of one cell"""
        self.grid[x][y] = False if self.grid[x][y] else True

    def generate_empty_grid(self) -> None:
        """generate a game state of only dead cells"""
        self.grid = [
            [False for y in range(self.grid_size[1])] for x in range(self.grid_size[0])
        ]

    def generate_glider_grid(self) -> None:
        """fill the grid with as many gliders as possible"""
        if not (self.grid_size[0] >= 5 and self.grid_size[1] >= 5):
            return
        self.generate_empty_grid()
        for x in range(0, len(self.grid), 5):
            for y in range(0, len(self.grid[0]), 5):
                if x < len(self.grid) - 4 and y < len(self.grid[0]) - 4:
                    self.grid[x + 2][y + 1] = True
                    self.grid[x + 3][y + 2] = True
                    self.grid[x + 1][y + 3] = True
                    self.grid[x + 2][y + 3] = True
                    self.grid[x + 3][y + 3] = True

    def generate_alternating_glider_grid(self) -> None:
        """
        fill the grid with as many gliders as possible.
        alternating rows of gliders move opposite directions
        """
        if not (self.grid_size[0] >= 5 and self.grid_size[1] >= 5):
            return
        self.generate_empty_grid()
        # - d: a flag to indicate direction. True is right, False is left
        direction = True
        for x in range(0, len(self.grid), 5):
            for y in range(0, len(self.grid[0]), 5):
                if x < len(self.grid) - 4 and y < len(self.grid[0]) - 4:
                    self.grid[x + 2][y + 1] = True
                    # - this if else handles the alternating directions of the rows of gliders
                    if direction:
                        self.grid[x + 3][y + 2] = True
                        direction = False
                    else:
                        self.grid[x + 1][y + 2] = True
                        direction = True
                    self.grid[x + 1][y + 3] = True
                    self.grid[x + 2][y + 3] = True
                    self.grid[x + 3][y + 3] = True
            direction = True

    def generate_spaceship_grid(self) -> None:
        """fill the grid with as many spaceships as possible"""
        if not (self.grid_size[0] >= 7 and self.grid_size[1] >= 6):
            return
        self.generate_empty_grid()
        for x in range(0, len(self.grid), 7):
            for y in range(0, len(self.grid[0]), 6):
                if x < len(self.grid) - 6 and y < len(self.grid[0]) - 5:
                    self.grid[x + 1][y + 1] = True
                    self.grid[x + 4][y + 1] = True
                    self.grid[x + 5][y + 2] = True
                    self.grid[x + 1][y + 3] = True
                    self.grid[x + 5][y + 3] = True
                    self.grid[x + 2][y + 4] = True
                    self.grid[x + 3][y + 4] = True
                    self.grid[x + 4][y + 4] = True
                    self.grid[x + 5][y + 4] = True

    def generate_rectangle(self) -> None:
        """create a rectangle of alive cells in the grid with a border of dead cells"""
        if not (self.grid_size[0] >= 3 and self.grid_size[1] >= 3):
            return
        self.generate_empty_grid()
        # - iterate through the entire grid except for the outer layer and set state to alive
        for x in range(1, len(self.grid) - 1):
            for y in range(1, len(self.grid[0]) - 1):
                self.grid[x][y] = True
