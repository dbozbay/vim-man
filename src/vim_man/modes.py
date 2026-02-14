from __future__ import annotations

from typing import TYPE_CHECKING

from vim_man.constants import CHASE_TIME, FREIGHT_TIME, SCATTER_TIME, GhostMode

if TYPE_CHECKING:
    from vim_man.ghosts import Ghost


class MainMode(object):
    # TODO: Write docstrings
    def __init__(self) -> None:
        self.timer: float = 0.0
        self.time: float | None = None
        self.mode: GhostMode | None = None
        self.scatter()

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.time is not None:
            if self.timer >= self.time:
                if self.mode is GhostMode.SCATTER:
                    self.chase()
                elif self.mode is GhostMode.CHASE:
                    self.scatter()

    def scatter(self) -> None:
        self.mode = GhostMode.SCATTER
        self.time = SCATTER_TIME
        self.timer = 0.0

    def chase(self) -> None:
        self.mode = GhostMode.CHASE
        self.time = CHASE_TIME
        self.timer = 0.0


class ModeController(object):
    def __init__(self, ghost: Ghost) -> None:
        self.timer: float = 0.0
        self.time: float | None = None
        self.mainmode: MainMode = MainMode()
        self.current: GhostMode | None = self.mainmode.mode
        self.ghost: Ghost = ghost

    def update(self, dt: float) -> None:
        self.mainmode.update(dt)
        if self.current is GhostMode.FREIGHT:
            self.timer += dt
            if self.time is not None:
                if self.timer >= self.time:
                    self.time = None
                    self.ghost.normal_mode()
                    self.current = self.mainmode.mode

        elif self.current in [GhostMode.SCATTER, GhostMode.CHASE]:
            self.current = self.mainmode.mode

        if self.current is GhostMode.SPAWN:
            if self.ghost.node == self.ghost.spawn_node:
                self.ghost.normal_mode()
                self.current = self.mainmode.mode

    def set_spawn_mode(self) -> None:
        if self.current is GhostMode.FREIGHT:
            self.current = GhostMode.SPAWN

    def set_freight_mode(self) -> None:
        # If ghost is in either SCATTER or CHASE mode, set to FREIGHT mode for 7 seconds.
        # If ghost is already in FREIGHT mode, reset the timer to 0.
        if self.current in [GhostMode.SCATTER, GhostMode.CHASE]:
            self.timer = 0
            self.time = FREIGHT_TIME
            self.current = GhostMode.FREIGHT
        elif self.current is GhostMode.FREIGHT:
            self.timer = 0
