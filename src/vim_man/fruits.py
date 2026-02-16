from vim_man.constants import GREEN
from vim_man.entity import Entity
from vim_man.nodes import Node
from vim_man.constants import EntityID, Direction


class Fruit(Entity):
    def __init__(self, node: Node) -> None:
        super().__init__(node)
        self.name = EntityID.FRUIT
        self.color = GREEN
        self.lifespan = 5.0
        self.timer = 0.0
        self.destroy = False
        self.points = 100
        self.set_between_nodes(Direction.RIGHT)

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
