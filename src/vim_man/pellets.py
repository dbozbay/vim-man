import pygame

from vim_man.constants import EntityID, TILEHEIGHT, TILEWIDTH, WHITE
from vim_man.level import Maze, MazeArray
from vim_man.vector import Vector2D


class Pellet:
    """Standard dot that Pacman can eat for small point values."""

    def __init__(self, row: int, column: int) -> None:
        """Initialize a standard pellet at specific maze coordinates with a fixed point value."""
        self.name = EntityID.PELLET
        self.position = Vector2D(column * TILEWIDTH, row * TILEHEIGHT)
        self.color = WHITE
        self.radius = int(4 * TILEWIDTH / 16)
        self.collide_radius = int(4 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, screen: pygame.Surface) -> None:
        """Draw the pellet as a colored circle on the screen if it is visible."""
        if self.visible:
            pos = self.position.as_int()
            pygame.draw.circle(screen, self.color, pos, self.radius)


class PowerPellet(Pellet):
    """Large, flashing pellet that grants higher points and triggers special ghost modes."""

    def __init__(self, row: int, column: int) -> None:
        """Initialize a power pellet with a larger radius and flashing behavioral state."""
        super().__init__(row, column)
        self.name = EntityID.POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flash_time = 0.2
        self.timer = 0.0

    def update(self, dt: float) -> None:
        """Toggle the visibility of the power pellet periodically to create a flashing effect."""
        self.timer += dt
        if self.timer >= self.flash_time:
            self.visible = not self.visible
            self.timer = 0


class PelletGroup(object):
    """Manages the creation and lifecycle of the pellets and power pellets."""

    def __init__(self, level: Maze) -> None:
        """Initialize the group by parsing the level's layout data and populating pellet lists."""
        self.level = level
        self.pellet_symbols = ["+", "."]
        self.powerpellet_symbols = ["P", "p"]
        self.pellet_list: list[Pellet] = []
        self.powerpellet_list: list[PowerPellet] = []
        self.create_pellet_list(self.level.data)
        self.num_eaten = 0

    def update(self, dt: float) -> None:
        """Advance the flashing logic for all power pellets in the group."""
        for powerpellet in self.powerpellet_list:
            powerpellet.update(dt)

    def create_pellet_list(self, data: MazeArray) -> None:
        """Parse the maze layout array to identify and instantiate pellet and power pellet locations."""
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in self.pellet_symbols:
                    self.pellet_list.append(Pellet(row, col))
                elif data[row][col] in self.powerpellet_symbols:
                    pp = PowerPellet(row, col)
                    self.pellet_list.append(pp)
                    self.powerpellet_list.append(pp)

    def is_empty(self) -> bool:
        """Return True if all pellets in the level have been eaten."""
        return len(self.pellet_list) == 0

    def render(self, screen: pygame.Surface) -> None:
        """Render every pellet in the group to the game screen."""
        for pellet in self.pellet_list:
            pellet.render(screen)
