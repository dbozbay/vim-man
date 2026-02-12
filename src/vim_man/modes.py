from vim_man.constants import FREIGHT, SPAWN
from vim_man.constants import SCATTER, CHASE
from vim_man.entity import Entity


class MainMode(object):
    def __init__(self) -> None:
        self.timer = 0.0
        self.time = None
        self.mode = None
        self.scatter()

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.time is not None:
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
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity

    def update(self, dt: float) -> None:
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            if self.time is not None:
                if self.timer >= self.time:
                    self.time = None
                    self.entity.normal_mode()  # pyrefly: ignore
                    self.current = self.mainmode.mode

        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            if self.entity.node == self.entity.spawn_node:
                self.entity.normal_mode()
                self.current = self.mainmode.mode

    def set_spawn_mode(self) -> None:
        if self.current is FREIGHT:
            self.current = SPAWN

    def set_freight_mode(self) -> None:
        # If ghost is in either SCATTER or CHASE mode, set to FREIGHT mode for 7 seconds.
        # If ghost is already in FREIGHT mode, reset the timer to 0.
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7.0
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0
