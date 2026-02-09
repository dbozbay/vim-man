from __future__ import annotations
import math


class Vector2D(object):
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Vector2D:
        return Vector2D(-self.x, -self.y)

    def __mul__(self, scalar: float) -> Vector2D:
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Vector2D | None:
        return Vector2D(self.x / scalar, self.y / scalar) if scalar != 0 else None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return False
        return (
            abs(self.x - other.x) < self.thresh and abs(self.y - other.y) < self.thresh
        )

    def magnitude_squared(self) -> float:
        return self.x**2 + self.y**2

    def magnitude(self) -> float:
        return math.sqrt(self.magnitude_squared())

    def copy(self) -> Vector2D:
        return Vector2D(self.x, self.y)

    def as_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def as_int(self) -> tuple[int, int]:
        return int(self.x), int(self.y)

    def __str__(self) -> str:
        return f"<{str(self.x)},{str(self.y)}>"
