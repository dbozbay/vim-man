from vim_man.constants import GHOST
from vim_man.entity import Entity
from vim_man.nodes import Node


class Ghost(Entity):
    def __init__(self, node: Node) -> None:
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
