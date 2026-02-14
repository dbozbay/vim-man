from vim_man.constants import EntityID, GhostMode
from vim_man.entity import Entity
from vim_man.modes import ModeController
from vim_man.nodes import Node
from vim_man.vector import Vector2D


class Ghost(Entity):
    """Ghost entity that moves like an Entity but chooses directions based on a goal position."""

    # TODO: Write docstrings for class methods
    def __init__(self, node: Node, pacman: Entity | None = None) -> None:
        """Initialize a ghost at the given starting node with scoring and goal-tracking behavior."""
        Entity.__init__(self, node)
        self.name = EntityID.GHOST
        self.points = 200
        self.goal = Vector2D(0, 0)
        # self.direction_method = self.goal_direction  # Override random directon
        self.pacman = pacman
        self.mode = ModeController(self)

    def update(self, dt: float) -> None:
        self.mode.update(dt)
        if self.mode.current is GhostMode.SCATTER:
            self.scatter()
        elif self.mode.current is GhostMode.CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self) -> None:
        self.goal = Vector2D(0, 0)

    def chase(self) -> None:
        if self.pacman is not None:
            self.goal = self.pacman.position

    def spawn(self) -> None:
        self.goal = self.spawn_node.position

    def set_spawn_node(self, node: Node) -> None:
        self.spawn_node = node

    def start_spawn(self) -> None:
        self.mode.set_spawn_mode()
        if self.mode.current == GhostMode.SPAWN:
            self.set_speed(150)
            self.direction_method = self.goal_direction
            self.spawn()

    def start_freight(self) -> None:
        self.mode.set_freight_mode()
        if self.mode.current == GhostMode.FREIGHT:
            self.set_speed(50)
            self.direction_method = self.random_direction

    def normal_mode(self) -> None:
        self.set_speed(100)
        self.direction_method = self.goal_direction
