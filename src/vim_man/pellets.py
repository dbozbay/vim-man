import numpy as np
import pygame

from vim_man.constants import BLUE, PELLET, POWERPELLET, TILEHEIGHT, TILEWIDTH
from vim_man.types import MazeArray
from vim_man.vector import Vector2D


class Pellet(object):
    def __init__(self, row: int, column: int) -> None:
        self.name = PELLET
        self.position = Vector2D(column * TILEWIDTH, row * TILEHEIGHT)
        self.color = BLUE
        self.radius = int(4 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, screen: pygame.Surface) -> None:
        if self.visible:
            pos = self.position.as_int()
            pygame.draw.circle(screen, self.color, pos, self.radius)


class PowerPellet(Pellet):
    def __init__(self, row: int, column: int) -> None:
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flash_time = 0.2
        self.timer = 0.0

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.timer >= self.flash_time:
            self.visible = not self.visible
            self.timer = 0


class PelletGroup(object):
    def __init__(self, pelletfile: str) -> None:
        self.pellet_symbols = ["+", "."]
        self.powerpellet_symbols = ["P", "p"]
        self.pellet_list: list[Pellet] = []
        self.powerpellet_list: list[PowerPellet] = []
        self.create_pellet_list(pelletfile)
        self.num_eaten = 0

    def update(self, dt: float) -> None:
        for powerpellet in self.powerpellet_list:
            powerpellet.update(dt)

    def create_pellet_list(self, pelletfile: str) -> None:
        data = self.read_pellet_file(pelletfile)
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.pellet_symbols:
                    self.pellet_list.append(Pellet(row, col))
                elif data[row][col] in self.powerpellet_symbols:
                    pp = PowerPellet(row, col)
                    self.pellet_list.append(pp)
                    self.powerpellet_list.append(pp)

    def read_pellet_file(self, textfile: str) -> MazeArray:
        return np.loadtxt(textfile, dtype="<U1")

    def is_empty(self) -> bool:
        return len(self.pellet_list) == 0

    def render(self, screen: pygame.Surface) -> None:
        for pellet in self.pellet_list:
            pellet.render(screen)


if __name__ == "__main__":
    pellets = PelletGroup("maze1.txt").pellet_list
    for p in pellets:
        print(p.position)
