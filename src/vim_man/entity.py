from __future__ import annotations

from random import choice

import pygame

from vim_man.constants import (
    TILEWIDTH,
    WHITE,
    Direction,
)
from vim_man.nodes import Node
from vim_man.pellets import Pellet
from vim_man.vector import Vector2D


class Entity(object):
    """Base moving game entity that travels between nodes on the maze and renders as a circle."""

    def __init__(self, node: Node) -> None:
        """Initialize an entity at the given node with default movement, appearance, and targeting state."""
        self.name = None
        self.directions = {
            Direction.STOP: Vector2D(),
            Direction.UP: Vector2D(0, -1),
            Direction.DOWN: Vector2D(0, 1),
            Direction.LEFT: Vector2D(-1, 0),
            Direction.RIGHT: Vector2D(1, 0),
        }

        self.direction = Direction.STOP
        self.set_speed(100)
        self.radius = 10
        self.collide_radius = 5
        self.color = WHITE
        self.node = node
        self.set_position()
        self.target = node
        self.visible = True
        self.disable_portal = False
        self.goal = None
        self.direction_method = self.goal_direction

    def set_position(self) -> None:
        """Align entity's position with the current node's position."""
        self.position = self.node.position.copy()

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
                portal_node = self.node.neighbors[Direction.PORTAL]
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

    def valid_direction(self, direction: Direction) -> bool:
        """Return True if entity has a neighboring node in the given direction."""
        if direction is not Direction.STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def valid_directions(self) -> list[Direction]:
        """Return a list of valid directions for the entity to move in."""
        # We only only want to move in the opposite direction if there are no other valid directions.
        directions = []
        for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            if self.valid_direction(d):
                if d != Direction(self.direction * -1):
                    directions.append(d)
        if len(directions) == 0:
            directions.append(Direction(self.direction * -1))
        return directions

    def random_direction(self, directions: list[Direction]) -> Direction:
        """Return a random direction from the given list of valid directions."""
        return choice(directions)

    # TODO: we are checking is None twice
    def get_new_target(self, direction: Direction) -> Node:
        """Return the neighboring node for the given direction, or the current node if movement is not possible."""
        if self.valid_direction(direction):
            neighbor = self.node.neighbors[direction]
            if neighbor is not None:
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
        self.direction = Direction(self.direction * -1)
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction: Direction) -> bool:
        """Return True if the given direction is opposite to entity's current direction."""
        if direction is not Direction.STOP:
            if direction == Direction(self.direction * -1):
                return True
        return False

    def set_speed(self, speed: int) -> None:
        """Set the entity's movement speed in pixels per second based on a tile-relative value."""
        self.speed = speed * TILEWIDTH / 16

    def goal_direction(self, directions: list[Direction]) -> Direction:
        """Return the direction that makes a one-tile step from the current node land closest to the goal."""
        # If no goal has been set, fall back to Entity's random-direction logic.
        if self.goal is None:
            return self.random_direction(directions)

        # Otherwise, we want this ghost to move in the direction such that,
        # after taking ONE tile-sized step in that direction, it is as close
        # as possible to the goal.
        # For each possible direction, we:
        #   1. Take a hypothetical one-tile step from the current node's
        #      position in that direction.
        #   2. Build a vector from that stepped-to position to the goal.
        #   3. Compute the squared magnitude of that vector as a distance
        #      metric and choose the direction with the smallest value.

        # TODO: How things would change with “nearest node in every direction”?
        return min(
            directions,
            key=lambda direction: (
                self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            ).magnitude_squared(),
        )

    def render(self, screen: pygame.SurfaceType) -> None:
        """Draw entity as a filled circle at his current position on the screen."""
        if self.visible:
            pos = self.position.as_int()
            pygame.draw.circle(screen, self.color, pos, self.radius)

    def collide_check(self, other: Entity | Pellet) -> bool:
        """Return True if this entity collides with another entity."""
        d = self.position - other.position
        d_squared = d.magnitude_squared()
        r_squared = (self.collide_radius + other.collide_radius) ** 2
        return d_squared <= r_squared
