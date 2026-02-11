from vim_man.constants import GHOST
from vim_man.entity import Entity
from vim_man.nodes import Node
from vim_man.vector import Vector2D


class Ghost(Entity):
    def __init__(self, node: Node) -> None:
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2D(0, 0)
        self.direction_method = self.goal_direction

    def goal_direction(self, directions: list[int]) -> int:
        # If no goal has been set, fall back to Entity's random direction logic.
        if self.goal is None:
            return self.random_direction(directions)

        # Otherwise, we want this ghost to move in the direction that gets its
        # *next node* (the neighboring junction in that direction) as close as
        # possible to the goal.
        # For each possible direction, we:
        #   1. Find the neighboring node we would move to in that direction.
        #   2. Build a vector from that neighbor node's position to the goal.
        #   3. Compute the squared magnitude of that vector as a distance metric.
        distances = []
        for direction in directions:
            neighbor = self.get_new_target(direction)
            vec = neighbor.position - self.goal
            distances.append(vec.magnitude_squared())
        index = distances.index(min(distances))
        return directions[index]
