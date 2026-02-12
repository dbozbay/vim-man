import pygame

from vim_man.constants import (
    DOWN,
    LEFT,
    PACMAN,
    PORTAL,
    RIGHT,
    STOP,
    UP,
    YELLOW,
)
from vim_man.entity import Entity
from vim_man.nodes import Node
from vim_man.pellets import Pellet


class Pacman(Entity):
    """Pacman controls the player character's movement and interaction with the maze graph."""

    def __init__(self, node: Node) -> None:
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW

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

    def collide_ghost(self, ghost: Entity) -> bool:
        return self.collide_check(ghost)

    def collide_check(self, other: Entity | Pellet) -> bool:
        d = self.position - other.position
        d_squared = d.magnitude_squared()
        r_squared = (self.collide_radius + other.collide_radius) ** 2
        return d_squared <= r_squared

    def eat_pellets(self, pellet_list: list[Pellet]) -> Pellet | None:
        """Return the first pellet colliding with Pacman, or `None` if no collision occurs."""
        for pellet in pellet_list:
            if self.collide_check(pellet):
                return pellet
        return None
