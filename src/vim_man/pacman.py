import pygame

from vim_man.constants import (
    YELLOW,
    Direction,
    EntityID,
)
from vim_man.entity import Entity
from vim_man.nodes import Node
from vim_man.pellets import Pellet


class Pacman(Entity):
    """Player-controlled character that moves through the maze eating pellets while avoiding ghosts."""

    def __init__(self, node: Node) -> None:
        """Initialize Pacman at a starting node with its default color and direction."""
        super().__init__(node)
        self.name = EntityID.PACMAN
        self.color = YELLOW
        self.direction = Direction.LEFT
        self.set_between_nodes(Direction.LEFT)
        self.alive = True

    def reset(self) -> None:
        """Reset Pacman to the starting position with default direction and alive state."""
        super().reset()
        self.direction = Direction.LEFT
        self.set_between_nodes(Direction.LEFT)
        self.alive = True

    def die(self) -> None:
        """Mark Pacman as dead and stop its movement."""
        self.alive = False
        self.direction = Direction.STOP

    def update(self, dt: float) -> None:
        """Process player input and update Pacman's position and target node."""
        # Move Pacman in the current direction according to speed and elapsed time.
        self.position += self.directions[self.direction] * self.speed * dt
        # Read the latest player input and translate it to a desired direction.
        direction = self.get_valid_key()

        if self.overshot_target():
            # Snap Pacman to the center of the target node he just reached.
            self.node = self.target

            # Check if the node has a portal neighbor and move to it if it does.
            portal_node = self.node.neighbors[Direction.PORTAL]
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
                self.direction = Direction.STOP
            # Reset position exactly on the current node center to avoid drift.
            self.set_position()
        else:
            if self.opposite_direction(direction):
                # If the player requests the opposite direction mid-tile, flip direction.
                self.reverse_direction()

    def get_valid_key(self) -> Direction:
        """Read keyboard input and return the corresponding game movement direction."""
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_k]:
            return Direction.UP
        elif key_pressed[pygame.K_j]:
            return Direction.DOWN
        elif key_pressed[pygame.K_h]:
            return Direction.LEFT
        elif key_pressed[pygame.K_l]:
            return Direction.RIGHT
        else:
            return Direction.STOP

    def eat_pellets(self, pellet_list: list[Pellet]) -> Pellet | None:
        """Return the first pellet currently colliding with Pacman's position."""
        for pellet in pellet_list:
            if self.collide_check(pellet):
                return pellet
        return None
