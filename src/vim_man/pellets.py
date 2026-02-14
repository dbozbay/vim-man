import pygame

from vim_man.constants import BLUE, TILEHEIGHT, TILEWIDTH, EntityID
from vim_man.level import MazeArray, MazeLevel
from vim_man.vector import Vector2D


class Pellet(object):
    """Pellet represents a standard dot that Pacman can eat for points."""

    def __init__(self, row: int, column: int) -> None:
        """Create a standard pellet at the given maze row and column."""
        self.name = EntityID.PELLET
        self.position = Vector2D(column * TILEWIDTH, row * TILEHEIGHT)
        self.color = BLUE
        self.radius = int(4 * TILEWIDTH / 16)
        self.collide_radius = int(4 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, screen: pygame.Surface) -> None:
        """Draw the pellet to the screen if it is currently visible."""
        if self.visible:
            pos = self.position.as_int()
            pygame.draw.circle(screen, self.color, pos, self.radius)


class PowerPellet(Pellet):
    """PowerPellet is a larger, flashing pellet that grants bonus points and power effects."""

    def __init__(self, row: int, column: int) -> None:
        """Create a power pellet at the given maze row and column."""
        Pellet.__init__(self, row, column)
        self.name = EntityID.POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flash_time = 0.2
        self.timer = 0.0

    def update(self, dt: float) -> None:
        """Toggle power pellet visibility over time to create a flashing effect."""
        self.timer += dt
        if self.timer >= self.flash_time:
            self.visible = not self.visible
            self.timer = 0


class PelletGroup(object):
    """PelletGroup manages all pellets and power pellets for a level."""

    def __init__(self, level: MazeLevel) -> None:
        """Load all pellets and power pellets for the level from the given layout file."""
        self.level = level
        self.pellet_symbols = ["+", "."]
        self.powerpellet_symbols = ["P", "p"]
        self.pellet_list: list[Pellet] = []
        self.powerpellet_list: list[PowerPellet] = []
        self.create_pellet_list(self.level.data)
        self.num_eaten = 0

    def update(self, dt: float) -> None:
        """Update all power pellets in the group."""
        for powerpellet in self.powerpellet_list:
            powerpellet.update(dt)

    def create_pellet_list(self, data: MazeArray) -> None:
        """Parse the pellet layout file and populate the pellet and power pellet lists."""
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.pellet_symbols:
                    self.pellet_list.append(Pellet(row, col))
                elif data[row][col] in self.powerpellet_symbols:
                    pp = PowerPellet(row, col)
                    self.pellet_list.append(pp)
                    self.powerpellet_list.append(pp)

    def is_empty(self) -> bool:
        """Return True if there are no pellets left in the level."""
        return len(self.pellet_list) == 0

    def render(self, screen: pygame.Surface) -> None:
        """Render all pellets in the group to the screen."""
        for pellet in self.pellet_list:
            pellet.render(screen)
