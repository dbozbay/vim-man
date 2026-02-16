from vim_man.constants import GREEN
from vim_man.entity import Entity
from vim_man.nodes import Node
from vim_man.constants import EntityID
import pygame


class Fruit(Entity):
    def __init__(self, node: Node) -> None:
        super().__init__(node)
        self.name = EntityID.FRUIT
        self.color = GREEN
        self.points = 50  # TODO: Check this
        self.visible = False
        self.set_start_node(node)
        self.set_speed(0)

        self.num_apparences = 0
        self.time = 7
        self.timer = 0.0

    def update(self, dt: float) -> None:
        if self.num_apparences <= 2:
            self.timer += dt
            if self.timer >= self.time:
                self.visible = not self.visible
                self.timer = 0
                if self.visible:
                    self.num_apparences += 1
        else:
            self.visible = False

    def render(self, screen: pygame.Surface) -> None:
        """Draw the fruit to the screen if it is currently visible."""
        if self.visible:
            pos = self.position.as_int()
            pygame.draw.circle(screen, self.color, pos, self.radius)
