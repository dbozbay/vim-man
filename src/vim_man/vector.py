from __future__ import annotations

import math


class Vector2D(object):
    """Vector2D represents a 2D vector with basic arithmetic and utility operations."""

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __add__(self, other: Vector2D) -> Vector2D:
        """Return the vector sum of this vector and another."""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        """Return the vector difference between this vector and another."""
        return Vector2D(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Vector2D:
        """Return a vector with both components negated."""
        return Vector2D(-self.x, -self.y)

    def __mul__(self, scalar: float) -> Vector2D:
        """Return a new vector scaled by the given scalar."""
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Vector2D:
        """Return a new vector divided by the given scalar."""
        return Vector2D(self.x / scalar, self.y / scalar)

    def __eq__(self, other: object) -> bool:
        """Return True if the other vector is approximately equal within the configured threshold."""
        if not isinstance(other, Vector2D):
            return False
        return (
            abs(self.x - other.x) < self.thresh and abs(self.y - other.y) < self.thresh
        )

    def magnitude_squared(self) -> float:
        """Return the squared length of the vector (avoiding a square root)."""
        return self.x**2 + self.y**2

    def magnitude(self) -> float:
        """Return the Euclidean length of the vector."""
        return math.sqrt(self.magnitude_squared())

    def copy(self) -> Vector2D:
        """Return a copy of this vector."""
        return Vector2D(self.x, self.y)

    def as_tuple(self) -> tuple[float, float]:
        """Return the vector components as an (x, y) tuple of floats."""
        return self.x, self.y

    def as_int(self) -> tuple[int, int]:
        """Return the vector components as an (x, y) tuple of ints."""
        return int(self.x), int(self.y)

    def __str__(self) -> str:
        """Return a string representation of the vector in angle-bracket form."""
        return f"<{str(self.x)},{str(self.y)}>"
