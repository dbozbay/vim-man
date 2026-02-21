from __future__ import annotations

from typing import TYPE_CHECKING

from vim_man.constants import CHASE_TIME, FREIGHT_TIME, SCATTER_TIME, GhostMode

if TYPE_CHECKING:
    from vim_man.ghosts import Ghost


class MainMode(object):
    """Controller for the global ghost behaviors of scattering and chasing."""

    def __init__(self) -> None:
        """Initialize the main mode state with scatter as the default behavioral mode."""
        self.timer: float = 0.0

        self.mode: GhostMode | None = None
        self.time: float = 0.0

        self.scatter()

        assert self.mode is not None

    def update(self, dt: float) -> None:
        """Advance the behavioral timer and toggle between scatter and chase modes."""
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is GhostMode.SCATTER:
                self.chase()
            elif self.mode is GhostMode.CHASE:
                self.scatter()

    def scatter(self) -> None:
        """Set the current mode to scatter and reset the behavioral timer."""
        self.mode = GhostMode.SCATTER
        self.time = SCATTER_TIME
        self.timer = 0.0

    def chase(self) -> None:
        """Set the current mode to chase and reset the behavioral timer."""
        self.mode = GhostMode.CHASE
        self.time = CHASE_TIME
        self.timer = 0.0


class ModeController(object):
    """Manages the behavior state transitions for an individual ghost entity."""

    def __init__(self, ghost: Ghost) -> None:
        """Initialize the controller with a reference to its ghost and the global main mode."""
        self.timer = 0.0
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.ghost = ghost
        self.time: float | None = None

    def update(self, dt: float) -> None:
        """Update the ghost's behavioral state based on global mode and freight timers."""
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
        """Transition the ghost to spawn mode if it is currently in freight mode."""
        if self.current is GhostMode.FREIGHT:
            self.current = GhostMode.SPAWN

    def set_freight_mode(self) -> None:
        """Transition the ghost to freight mode for a set duration."""
        if self.current in [GhostMode.SCATTER, GhostMode.CHASE]:
            self.timer = 0
            self.time = FREIGHT_TIME
            self.current = GhostMode.FREIGHT
        elif self.current is GhostMode.FREIGHT:
            self.timer = 0
