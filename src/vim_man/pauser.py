from typing import Callable


class Pause:
    """Pause manages the temporary suspension of game logic and timers."""

    def __init__(self, paused: bool = False) -> None:
        """Initialize the pause state with an optional initial paused flag and timer."""
        self.paused = paused
        self.timer = 0.0
        self.pause_time: float | None = None
        self.func: Callable | None = None

    def update(self, dt: float) -> Callable | None:
        """Advance the pause timer and return the callback function when the duration expires."""
        if self.pause_time is not None:
            self.timer += dt
            if self.timer >= self.pause_time:
                self.timer = 0.0
                self.paused = False
                self.pause_time = None
                return self.func
        return None

    def set_pause(
        self,
        player_paused: bool = False,
        pause_time: float | None = None,
        func: Callable | None = None,
    ) -> None:
        """Explicitly set a timed pause with an optional callback function to execute afterwards."""
        self.timer = 0
        self.func = func
        self.pause_time = pause_time
        self.flip()

    def flip(self) -> None:
        """Toggle the current paused state between True and False."""
        self.paused = not self.paused
