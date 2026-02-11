from random import randint

import pygame

from vim_man.constants import (
    DOWN,
    LEFT,
    PORTAL,
    RIGHT,
    STOP,
    TILEWIDTH,
    UP,
    WHITE,
)
from vim_man.nodes import Node
from vim_man.vector import Vector2D


class Entity(object):
    """Base moving game entity that travels between nodes on the maze and renders as a circle."""

    def __init__(self, node: Node) -> None:
        """Initialize an entity at the given node with default movement, appearance, and targeting state."""
        self.name: int | None = None
        self.directions = {
            STOP: Vector2D(),
            UP: Vector2D(0, -1),
            DOWN: Vector2D(0, 1),
            LEFT: Vector2D(-1, 0),
            RIGHT: Vector2D(1, 0),
        }

        self.direction = STOP
        self.set_speed(100)
        self.radius = 10
        self.collide_radius = 5
        self.color = WHITE
        self.node = node
        self.set_position()
        self.target = node
        self.visible = True
        self.disable_portal = False
        self.goal: Vector2D | None = None
        self.direction_method = self.random_direction

    def set_position(self) -> None:
        """Align entity's position with the current node's position."""
        self.position = self.node.position.copy()

    def valid_direction(self, direction: int) -> bool:
        """Return True if entity has a neighboring node in the given direction."""
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def valid_directions(self) -> list[int]:
        """Return a list of valid directions for the entity to move in."""
        # We only only want to move in the opposite direction if there are no other valid directions.
        directions = []
        for d in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(d):
                if d != self.direction * -1:
                    directions.append(d)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def random_direction(self, directions: list[int]) -> int:
        """Return a random direction from the given list of valid directions."""
        return directions[randint(0, len(directions) - 1)]

    # TODO: we are checking is None twice
    def get_new_target(self, direction: int) -> Node:
        """Return the neighboring node for the given direction, or the current node if movement is not possible."""
        if self.valid_direction(direction):
            neighbor = self.node.neighbors[direction]
            assert neighbor is not None
            return neighbor
        return self.node

    def overshot_target(self) -> bool:
        """Return True if entity has moved past the center of the target node."""
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2target = vec1.magnitude_squared()
            node2self = vec2.magnitude_squared()
            return node2self >= node2target
        return False

    def reverse_direction(self) -> None:
        """Reverse entity's movement direction and swap the current node with the target node."""
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction: int) -> bool:
        """Return True if the given direction is opposite to entity's current direction."""
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def set_speed(self, speed: int) -> None:
        """Set the entity's movement speed in pixels per second based on a tile-relative value."""
        self.speed = speed * TILEWIDTH / 16

    def update(self, dt: float) -> None:
        """Advance the entity in its current direction by its speed*dt and handle node transitions (direction changes, portals)."""
        self.position += self.directions[self.direction] * self.speed * dt

        # Once we have reached or passed the center of the target node....
        if self.overshot_target():
            # Update the current node to the target we’ve just reached.
            self.node = self.target

            # Choose a direction from the available valid directions based on the entity's direction method.
            directions = self.valid_directions()
            direction = self.direction_method(directions)

            # If portals are enabled and this node has a portal neighbor, teleport to that portal node.
            if not self.disable_portal:
                portal_node = self.node.neighbors[PORTAL]
                if portal_node is not None:
                    self.node = portal_node

            # First, try moving in the newly chosen random direction from this node.
            # If that direction is valid, update the movement direction and target that neighbor.
            # Otherwise, fall back to continuing in the current direction if that is still valid.
            # If neither is valid, remain on this node (no target neighbor).
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            # After choosing a new target (and handling portals), snap position to the new node’s center.
            self.set_position()

    def render(self, screen: pygame.SurfaceType) -> None:
        """Draw entity as a filled circle at his current position on the screen."""
        # Pygame does not like drawing circles with floats!
        pos = self.position.as_int()
        pygame.draw.circle(screen, self.color, pos, self.radius)
