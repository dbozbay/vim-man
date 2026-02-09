import pygame
from vim_man.vector import Vector2D
from vim_man.constants import PACMAN, STOP, YELLOW, UP, DOWN, LEFT, RIGHT, TILEWIDTH
from vim_man.nodes import Node


class Pacman(object):
    def __init__(self, node: Node) -> None:
        self.name = PACMAN
        # self.position = Vector2D(200, 400)
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
        self.node = node
        self.set_position()

    def set_position(self) -> None:
        self.position = self.node.position.copy()

    def update(self, dt: float) -> None:
        # self.position += self.directions[self.direction] * self.speed * dt
        direction = self.get_valid_key()
        self.direction = direction
        self.node = self.get_new_target(direction)
        self.set_position()

    # TODO: Maybe put this logic inside `get_new_target` to make type checker happy
    def valid_direction(self, direction: int) -> bool:
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    # TODO: Currently duplicating the is None check twice. Fix this later
    def get_new_target(self, direction: int) -> Node:
        if self.valid_direction(direction):
            neighbor = self.node.neighbors[direction]
            if neighbor is not None:
                return neighbor
        return self.node

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
