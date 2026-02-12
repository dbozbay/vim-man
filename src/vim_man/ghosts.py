from vim_man.constants import FREIGHT
from vim_man.constants import SCATTER, CHASE
from vim_man.constants import GHOST, TILEWIDTH
from vim_man.entity import Entity
from vim_man.nodes import Node
from vim_man.vector import Vector2D
from vim_man.pacman import Pacman
from vim_man.modes import ModeController


class Ghost(Entity):
    """Ghost entity that moves like an Entity but chooses directions based on a goal position."""

    def __init__(self, node: Node, pacman: Pacman) -> None:
        """Initialize a ghost at the given starting node with scoring and goal-tracking behavior."""
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2D(0, 0)
        self.direction_method = self.goal_direction  # Override random directon
        self.pacman = pacman
        self.mode = ModeController(self)

    def update(self, dt: float) -> None:
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self) -> None:
        self.goal = Vector2D(0, 0)

    def chase(self) -> None:
        self.goal = self.pacman.position

    def start_freight(self) -> None:
        self.mode.set_freight_mode()
        if self.mode.current == FREIGHT:
            self.set_speed(50)
            self.direction_method = self.random_direction

    def normal_mode(self) -> None:
        self.set_speed(100)
        self.direction_method = self.goal_direction

    def goal_direction(self, directions: list[int]) -> int:
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
