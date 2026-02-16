from __future__ import annotations

import pygame

from vim_man.constants import (
    NCOLS,
    NROWS,
    ORANGE,
    PINK,
    RED,
    TEAL,
    TILEHEIGHT,
    TILEWIDTH,
    EntityID,
    GhostMode,
)
from vim_man.entity import Entity
from vim_man.modes import ModeController
from vim_man.nodes import Node
from vim_man.pacman import Pacman
from vim_man.vector import Vector2D


class Ghost(Entity):
    """Ghost entity that moves like an Entity but chooses directions based on a goal position."""

    def __init__(
        self, node: Node, pacman: Pacman | None = None, blinky: Blinky | None = None
    ) -> None:
        """Initialize a ghost with its starting node, target, and behavior modes."""
        super().__init__(node)
        self.name = EntityID.GHOST
        self.points = 200
        self.goal = Vector2D()
        self.direction_method = self.goal_direction
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homenode = node
        self.spawn_node: Node

    def update(self, dt: float) -> None:
        """Update the ghost's behavior mode and position based on elapsed time."""
        self.mode.update(dt)
        if self.mode.current is GhostMode.SCATTER:
            self.scatter()
        elif self.mode.current is GhostMode.CHASE:
            self.chase()
        super().update(dt)

    def scatter(self) -> None:
        """Set the ghost's target goal to its default scatter position."""
        self.goal = Vector2D()

    def chase(self) -> None:
        """Set the ghost's target goal based on Pacman's current position."""
        if self.pacman is not None:
            self.goal = self.pacman.position

    def start_freight(self) -> None:
        """Switch the ghost to freight mode, reducing its speed and making it move randomly."""
        self.mode.set_freight_mode()
        if self.mode.current == GhostMode.FREIGHT:
            self.set_speed(50)
            self.direction_method = self.random_direction

    def normal_mode(self) -> None:
        """Reset the ghost to its standard speed and goal-seeking behavior."""
        self.set_speed(100)
        self.direction_method = self.goal_direction

    def spawn(self) -> None:
        """Set the ghost's goal to its spawn node position."""
        self.goal = self.spawn_node.position

    def set_spawn_node(self, node: Node) -> None:
        """Assign the designated spawn node for the ghost."""
        self.spawn_node = node

    def start_spawn(self) -> None:
        """Switch the ghost to spawn mode, increasing speed as it returns to the ghost house."""
        self.mode.set_spawn_mode()
        if self.mode.current == GhostMode.SPAWN:
            self.set_speed(150)
            self.direction_method = self.goal_direction
            self.spawn()


class Blinky(Ghost):
    """Red ghost that aggressively chases Pacman directly."""

    def __init__(
        self, node: Node, pacman: Pacman | None = None, blinky: Blinky | None = None
    ) -> None:
        """Initialize Blinky with its specific identity and color."""
        super().__init__(node, pacman, blinky)
        self.name = EntityID.BLINKY
        self.color = RED


class Pinky(Ghost):
    """Pink ghost that attempts to ambush Pacman by targeting ahead of him."""

    def __init__(
        self, node: Node, pacman: Pacman | None = None, blinky: Blinky | None = None
    ) -> None:
        """Initialize Pinky with its specific identity and color."""
        super().__init__(node, pacman, blinky)
        self.name = EntityID.PINKY
        self.color = PINK

    def scatter(self) -> None:
        """Set Pinky's goal to the upper right corner of the maze."""
        self.goal = Vector2D(TILEWIDTH * NCOLS, 0)

    def chase(self) -> None:
        """Target a position four tiles ahead of Pacman's current direction."""
        if self.pacman is not None:
            self.goal = (
                self.pacman.position
                + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
            )


class Inky(Ghost):
    """Teal ghost that uses both Pacman's and Blinky's positions for its targeting logic."""

    def __init__(
        self, node: Node, pacman: Pacman | None = None, blinky: Blinky | None = None
    ) -> None:
        """Initialize Inky with its specific identity and color."""
        super().__init__(node, pacman, blinky)
        self.name = EntityID.INKY
        self.color = TEAL

    def scatter(self) -> None:
        """Set Inky's goal to the bottom right corner of the maze."""
        self.goal = Vector2D(TILEWIDTH * NCOLS, TILEHEIGHT * NROWS)

    def chase(self) -> None:
        """Target a position determined by a vector from Blinky through a point ahead of Pacman."""
        if self.pacman is not None and self.blinky is not None:
            vec1 = (
                self.pacman.position
                + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
            )
            vec2 = (vec1 - self.blinky.position) * 2
            self.goal = self.blinky.position + vec2


class Clyde(Ghost):
    """Orange ghost that chases Pacman when distant but retreats when close."""

    def __init__(self, node: Node, pacman: Pacman | None = None) -> None:
        """Initialize Clyde with its specific identity and color."""
        super().__init__(node, pacman)
        self.name = EntityID.CLYDE
        self.color = ORANGE

    def scatter(self) -> None:
        """Set Clyde's goal to the bottom left corner of the maze."""
        self.goal = Vector2D(0, TILEHEIGHT * NROWS)

    def chase(self) -> None:
        """Chase Pacman if distant, otherwise retreat to its scatter goal."""
        if self.pacman is not None:
            d = self.pacman.position
            d_squared = d.magnitude_squared()
            if d_squared <= (TILEWIDTH * 8) ** 2:
                self.scatter()
            else:
                self.goal = (
                    self.pacman.position
                    + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
                )


class GhostGroup:
    """Manages the lifecycle and collective behaviors of the ghost entities."""

    def __init__(self, node: Node, pacman: Pacman | None = None) -> None:
        """Initialize the group by creating all four ghost instances."""
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        """Return an iterator over the individual ghosts in the group."""
        return iter(self.ghosts)

    def update(self, dt: float) -> None:
        """Update the logic and position of all ghosts in the group."""
        for ghost in self:
            ghost.update(dt)

    def start_freight(self) -> None:
        """Set all ghosts in the group to freight mode and reset their point values."""
        for ghost in self:
            ghost.start_freight()
        self.reset_points()

    def set_spawn_node(self, node: Node) -> None:
        """Set the common spawn node for all ghosts in the group."""
        for ghost in self:
            ghost.set_spawn_node(node)

    def update_points(self) -> None:
        """Double the point value awarded for eating ghosts during the current freight period."""
        for ghost in self:
            ghost.points *= 2

    def reset_points(self) -> None:
        """Reset the point value for all ghosts to the base starting value."""
        for ghost in self:
            ghost.points = 200

    def hide(self) -> None:
        """Make all ghosts in the group invisible on the screen."""
        for ghost in self:
            ghost.visible = False

    def show(self) -> None:
        """Make all ghosts in the group visible on the screen."""
        for ghost in self:
            ghost.visible = True

    def render(self, screen: pygame.Surface) -> None:
        """Draw all ghosts in the group to the screen."""
        for ghost in self:
            ghost.render(screen)
