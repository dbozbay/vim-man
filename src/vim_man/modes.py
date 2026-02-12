from vim_man.constants import SCATTER, CHASE
from vim_man.entity import Entity


class MainMode(object):
    def __init__(self) -> None:
        self.timer = 0.0
        self.scatter()

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self) -> None:
        self.mode = SCATTER
        self.time = 7.0
        self.timer = 0.0

    def chase(self) -> None:
        self.mode = CHASE
        self.time = 20.0
        self.timer = 0.0


class ModeController(object):
    def __init__(self, entity: Entity) -> None:
        self.timer = 0.0
        self.time: float | None = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity

    def update(self, dt: float) -> None:
        self.mainmode.update(dt)
        self.current = self.mainmode.mode
