from typing import Callable


class Pause:
    def __init__(self, paused: bool = False) -> None:
        self.paused = paused
        self.timer = 0.0
        self.pause_time: float | None = None
        self.func: Callable | None = None

    def update(self, dt: float) -> Callable | None:
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
        self.timer = 0
        self.func = func
        self.pause_time = pause_time
        self.flip()

    def flip(self) -> None:
        self.paused = not self.paused
