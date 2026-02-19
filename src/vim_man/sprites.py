from vim_man.constants import EntityID
import pygame
from pygame import Surface
from vim_man.constants import BASETILEHEIGHT, BASETILEWIDTH, TILEHEIGHT, TILEWIDTH
from vim_man.entity import Entity
from vim_man.utils import get_image_path


class Spritesheet:
    def __init__(self) -> None:
        self.sheet = pygame.image.load(get_image_path("spritesheet.png")).convert()
        transparent_color = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transparent_color)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    def get_image(self, x: float, y: float, width: float, height: float) -> Surface:
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())


class PacmanSprites(Spritesheet):
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity
        self.entity.image = self.get_start_image()

    def get_start_image(self) -> Surface:
        return self.get_image(8, 0)

    def get_image(self, x: float, y: float, width: float = 2 * TILEWIDTH, height: float = 2 * TILEHEIGHT) -> Surface:
        return super().get_image(x, y, width, height)


class GhostSprites(Spritesheet):
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.x = {
            EntityID.BLINKY: 0,
            EntityID.PINKY: 2,
            EntityID.INKY: 4,
            EntityID.CLYDE: 6,
        }
        self.entity = entity
        self.entity.image = self.get_start_image()

    def get_start_image(self) -> Surface | None:
        name = self.entity.name
        if name is not None:
            return self.get_image(self.x[name], 4)

    def get_image(self, x: float, y: float, width: float = 2 * TILEWIDTH, height: float = 2 * TILEHEIGHT) -> Surface:
        return super().get_image(x, y, width, height)


class FruitSprites(Spritesheet):
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity
        self.entity.image = self.get_start_image()

    def get_start_image(self) -> Surface:
        return self.get_image(16, 8)

    def get_image(self, x: float, y: float, width: float = 2 * TILEWIDTH, height: float = 2 * TILEHEIGHT) -> Surface:
        return super().get_image(x, y, width, height)
