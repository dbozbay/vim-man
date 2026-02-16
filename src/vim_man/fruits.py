from vim_man.constants import GREEN
from vim_man.entity import Entity
from vim_man.nodes import Node
from vim_man.constants import EntityID


class Fruit(Entity):
    def __init__(self, node: Node) -> None:
        super().__init__(node)
        self.name = EntityID.FRUIT
        self.set_speed(0)
        self.color = GREEN
        self.set_start_node(node)

    

