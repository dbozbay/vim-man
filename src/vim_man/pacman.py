import pygame

from vim_man.constants import (
    DOWN,
    LEFT,
    PACMAN,
    PORTAL,
    RIGHT,
    STOP,
    TILEWIDTH,
    UP,
    YELLOW,
)
from vim_man.nodes import Node
from vim_man.vector import Vector2D


class Pacman(object):
    def __init__(self, node: Node) -> None:
        self.name = PACMAN
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
        self.target = node

    def set_position(self) -> None:
        """Align Pacman's position with the current node's position."""
        self.position = self.node.position.copy()

    def update(self, dt: float) -> None:
        """Update Pacman's movement, direction, and target node based on input and elapsed time."""
        # Move Pacman in the current direction according to speed and elapsed time.
        self.position += self.directions[self.direction] * self.speed * dt
        # Read the latest player input and translate it to a desired direction.
        direction = self.get_valid_key()

        if self.overshot_target():
            # Snap Pacman to the center of the target node he just reached.
            self.node = self.target

            # Check if the node has a portal neighbor and move to it if it does.
            portal_node = self.node.neighbors[PORTAL]
            if portal_node is not None:
                self.node = portal_node

            # Try to move toward the newly requested direction from this node.
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                # If that move is possible, commit to the new direction.
                self.direction = direction
            else:
                # Otherwise, keep moving in the current direction if possible.
                self.target = self.get_new_target(self.direction)

            if self.target is self.node:
                # If no movement is possible from this node, stop.
                self.direction = STOP
            # Reset position exactly on the current node center to avoid drift.
            self.set_position()
        else:
            if self.opposite_direction(direction):
                # If the player requests the opposite direction mid-tile, flip direction.
                self.reverse_direction()

    # TODO: Refactored this check away into `get_new_target`. Delete if no other callers needed
    # def valid_direction(self, direction: int) -> bool:
    #     """Return whether the given direction leads to a valid neighboring node."""
    #     if direction is not STOP:
    #         if self.node.neighbors[direction] is not None:
    #             return True
    #     return False

    def get_new_target(self, direction: int) -> Node:
        """Return the neighboring node for the given direction, or the current node if movement is not possible."""
        if direction is not STOP:
            neighbor = self.node.neighbors[direction]
            if neighbor is not None:
                return neighbor
        return self.node

    def get_valid_key(self) -> int:
        """Read the keyboard and return the corresponding movement direction constant."""
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_k]:
            return UP
        elif key_pressed[pygame.K_j]:
            return DOWN
        elif key_pressed[pygame.K_h]:
            return LEFT
        elif key_pressed[pygame.K_l]:
            return RIGHT
        else:
            return STOP

    def overshot_target(self) -> bool:
        """Return True if Pacman has moved past the center of the target node."""
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2target = vec1.magnitude_squared()
            node2self = vec2.magnitude_squared()
            return node2self >= node2target
        return False

    def reverse_direction(self) -> None:
        """Reverse Pacman's movement direction and swap the current node with the target node."""
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction: int) -> bool:
        """Return True if the given direction is opposite to Pacman's current direction."""
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def render(self, screen: pygame.SurfaceType) -> None:
        """Draw Pacman as a filled circle at his current position on the screen."""
        # Pygame does not like drawing circles with floats!
        pos = self.position.as_int()
        pygame.draw.circle(screen, self.color, pos, self.radius)
