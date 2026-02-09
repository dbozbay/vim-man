import pygame
from vim_man.vector import Vector2D
from vim_man.constants import PACMAN, STOP, YELLOW, UP, DOWN, LEFT, RIGHT, TILEWIDTH


class Pacman(object):
    def __init__(self) -> None:
        self.name = PACMAN
        self.position = Vector2D(200, 400)
        self.directions = {
            STOP: Vector2D(),
            UP: Vector2D(0, -1),
            DOWN: Vector2D(0, 1),
            LEFT: Vector2D(-1, 0),
            RIGHT: Vector2D(1, 0),
        }
        self.direction = STOP
        self.speed = 100 * TILEWIDTH / 16
        self.radius = 10
        self.color = YELLOW

    def update(self, dt: float) -> None:
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.get_valid_key()
        self.direction = direction

    def get_valid_key(self) -> int:
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_k]:
            return UP
        if key_pressed[pygame.K_j]:
            return DOWN
        if key_pressed[pygame.K_h]:
            return LEFT
        if key_pressed[pygame.K_l]:
            return RIGHT
        return STOP

    def render(self, screen: pygame.SurfaceType) -> None:
        # Pygame does not like drawing circles with floats!
        pos = self.position.as_int()
        pygame.draw.circle(screen, self.color, pos, self.radius)
