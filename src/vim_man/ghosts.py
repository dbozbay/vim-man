from vim_man.constants import ORANGE
from vim_man.constants import NROWS
from vim_man.constants import RED
import pygame
from vim_man.constants import NCOLS
from vim_man.constants import TILEWIDTH, TILEHEIGHT
from vim_man.constants import PINK
from vim_man.constants import TEAL
from vim_man.constants import EntityID, GhostMode
from vim_man.entity import Entity
from vim_man.modes import ModeController
from vim_man.nodes import Node
from vim_man.vector import Vector2D
from vim_man.pacman import Pacman


class Ghost(Entity):
    """Ghost entity that moves like an Entity but chooses directions based on a goal position."""

    # TODO: Write docstrings for class methods
    def __init__(self, node: Node, pacman: Pacman | None = None) -> None:
        """Initialize a ghost at the given starting node with scoring and goal-tracking behavior."""
        super().__init__(node)
        self.name = EntityID.GHOST
        self.points = 200
        self.goal = Vector2D()
        self.pacman = pacman
        # self.direction_method = self.goal_direction
        self.mode = ModeController(self)

    def update(self, dt: float) -> None:
        self.mode.update(dt)
        if self.mode.current is GhostMode.SCATTER:
            self.scatter()
        elif self.mode.current is GhostMode.CHASE:
            self.chase()
        super().update(dt)

    def scatter(self) -> None:
        self.goal = Vector2D()

    def chase(self) -> None:
        if self.pacman is not None:
            self.goal = self.pacman.position

    def start_freight(self) -> None:
        self.mode.set_freight_mode()
        if self.mode.current == GhostMode.FREIGHT:
            self.set_speed(50)
            self.direction_method = self.random_direction

    def normal_mode(self) -> None:
        self.set_speed(100)
        self.direction_method = self.goal_direction

    def spawn(self) -> None:
        self.goal = self.spawn_node.position

    def set_spawn_node(self, node: Node) -> None:
        print(node.position)
        self.spawn_node = node

    def start_spawn(self) -> None:
        self.mode.set_spawn_mode()
        if self.mode.current == GhostMode.SPAWN:
            self.set_speed(150)
            self.direction_method = self.goal_direction
            self.spawn()


class Blinky(Ghost):
    def __init__(self, node: Node, pacman: Pacman | None = None) -> None:
        super().__init__(node, pacman)
        self.name = EntityID.BLINKY
        self.color = RED


class Pinky(Ghost):
    def __init__(self, node: Node, pacman: Pacman | None = None) -> None:
        super().__init__(node, pacman)
        self.name = EntityID.PINKY
        self.color = PINK

    def scatter(self) -> None:
        """Scatter to the upper right corner."""
        self.goal = Vector2D(TILEWIDTH * NCOLS, 0)

    def chase(self) -> None:
        """Find out where Pacman is and target 4 tiles ahead of him."""
        if self.pacman is not None:
            self.goal = (
                self.pacman.position
                + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
            )


class Inky(Ghost):
    def __init__(self, node: Node, pacman: Pacman | None = None) -> None:
        super().__init__(node, pacman)
        self.name = EntityID.INKY
        self.color = TEAL

    def scatter(self) -> None:
        """Scatter to the bottom left corner."""
        self.goal = Vector2D(0, TILEHEIGHT * NROWS)


class Clyde(Ghost):
    def __init__(self, node: Node, pacman: Pacman | None = None) -> None:
        super().__init__(node, pacman)
        self.name = EntityID.CLYDE
        self.color = ORANGE

    def scatter(self) -> None:
        """Scatter to the bottom left corner."""
        self.goal = Vector2D(TILEWIDTH * NCOLS, TILEHEIGHT * NROWS)


class GhostGroup:
    def __init__(self, node: Node, pacman: Pacman | None = None) -> None:
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):  # TODO: return type?
        return iter(self.ghosts)

    def update(self, dt: float) -> None:
        for ghost in self:
            ghost.update(dt)

    def start_freight(self) -> None:
        for ghost in self:
            ghost.start_freight()
        self.reset_points()

    def set_spawn_node(self, node: Node) -> None:
        for ghost in self:
            ghost.set_spawn_node(node)

    def update_points(self) -> None:
        for ghost in self:
            ghost.points *= 2

    def reset_points(self) -> None:
        for ghost in self:
            ghost.points = 200

    # def reset(self) -> None:
    #     for ghost in self:
    #         ghost.reset()

    def hide(self) -> None:
        for ghost in self:
            ghost.visible = False

    def show(self) -> None:
        for ghost in self:
            ghost.visible = True

    def render(self, screen: pygame.Surface) -> None:
        for ghost in self:
            ghost.render(screen)
