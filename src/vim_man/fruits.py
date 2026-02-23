from vim_man.constants import GREEN, Direction, EntityID
from vim_man.entity import Entity
from vim_man.nodes import Node
from vim_man.sprites import FruitSprites


class Fruit(Entity):
    """Bonus fruit entity that appears temporarily and can be eaten for points."""

    def __init__(self, node: Node) -> None:
        """Initialize the fruit at a specific node with a limited lifespan."""
        super().__init__(node)
        self.name = EntityID.FRUIT
        self.color = GREEN
        self.lifespan = 5.0
        self.timer = 0.0
        self.destroy = False
        self.points = 100
        self.set_between_nodes(Direction.RIGHT)
        self.sprites = FruitSprites(self)

    def update(self, dt: float) -> None:
        """Update the fruit's timer and mark it for destruction when its lifespan expires."""
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
