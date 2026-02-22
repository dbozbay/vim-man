import pygame
from pygame import Surface

from vim_man.constants import BASETILEHEIGHT, BASETILEWIDTH, EntityID, SCREENHEIGHT, TILEHEIGHT, TILEWIDTH, SPRITEFILE
from vim_man.entity import Entity
from vim_man.level import MazeArray
from vim_man.utils import get_image_path


class Spritesheet:
    def __init__(self) -> None:
        self.sheet = pygame.image.load(get_image_path(SPRITEFILE)).convert()
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


class LifeSprites(Spritesheet):
    def __init__(self, num_lives: int) -> None:
        super().__init__()
        self.reset_lives(num_lives)

        self.images: list[Surface]

    def remove_image(self) -> None:
        if len(self.images) > 0:
            self.images.pop(0)

    def reset_lives(self, num_lives: int) -> None:
        self.images = []
        for i in range(num_lives):
            self.images.append(self.get_image(0, 0))

    def get_image(self, x: float, y: float, width: float = 2 * TILEWIDTH, height: float = 2 * TILEHEIGHT) -> Surface:
        return super().get_image(x, y, width, height)

    def render(self, screen: Surface) -> None:
        for i, image in enumerate(self.images):
            x = image.get_width() * i
            y = SCREENHEIGHT - image.get_height()
            screen.blit(image, (x, y))


class MazeSprites(Spritesheet):
    def __init__(self, data: MazeArray, rot_data: MazeArray | None = None) -> None:
        super().__init__()
        self.data = data
        self.rot_data = rot_data

    def get_image(self, x: float, y: float, width: float = TILEWIDTH, height: float = TILEHEIGHT) -> Surface:
        return super().get_image(x, y, width, height)

    def construct_background(self, backgroud: Surface, y: float) -> Surface:
        for row in range(self.data.shape[0]):
            for col in range(self.data.shape[1]):
                element = self.data[row][col]
                if element.isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.get_image(x, y)
                    if self.rot_data is not None:
                        rotation = self.rot_data[row][col]
                        if rotation.isdigit():
                            sprite = self.rotate(sprite, int(rotation))
                    backgroud.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))
                elif element == "=":
                    sprite = self.get_image(10, 8)
                    backgroud.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))
        return backgroud

    def rotate(self, sprite: Surface, value: int) -> Surface:
        return pygame.transform.rotate(sprite, value * 90)
