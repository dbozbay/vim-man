from __future__ import annotations

from typing import TYPE_CHECKING

from vim_man.constants import CHASE, FREIGHT, SCATTER, SPAWN

if TYPE_CHECKING:
    from vim_man.ghosts import Ghost


class MainMode(object):
    # TODO: Write docstrings
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
    def __init__(self, ghost: Ghost) -> None:
        self.timer = 0.0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.ghost = ghost

    def update(self, dt: float) -> None:
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            if self.time is not None:
                if self.timer >= self.time:
                    self.time = None
                    self.ghost.normal_mode()
                    self.current = self.mainmode.mode

        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            if self.ghost.node == self.ghost.spawn_node:
                self.ghost.normal_mode()
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
