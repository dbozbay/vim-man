from vim_man.vector import Vector2D


class TestVector2D:
    def test_addition(self) -> None:
        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)
        result = v1 + v2
        assert result.x == 4
        assert result.y == 6

    def test_subtraction(self) -> None:
        v1 = Vector2D(10, 12)
        v2 = Vector2D(15, 4)
        result = v1 - v2
        assert result.x == -5
        assert result.y == 8

    def test_negation(self) -> None:
        v = Vector2D(-5, 2)
        result = -v
        assert result.x == 5
        assert result.y == -2

    def test_scalar_muliplication(self) -> None:
        v = Vector2D(3, 4)
        result = v * 3
        assert result.x == 9
        assert result.y == 12

    def test_division_by_nonzero(self) -> None:
        v = Vector2D(18, 6)
        result = v / 6
        assert result is not None
        assert result.x == 3
        assert result.y == 1

    def test_division_by_zero(self) -> None:
        v = Vector2D(5, 5)
        result = v / 0
        assert result is None

    def test_equality(self) -> None:
        v1 = Vector2D(10, 5)
        v2 = Vector2D(10, 5)
        assert v1 == v2

    def test_equality_within_thresh(self) -> None:
        v1 = Vector2D(1, 2)
        v2 = Vector2D(1.0000001, 2.0000001)
        assert v1 == v2

    def test_inequality(self) -> None:
        v1 = Vector2D(2, 3)
        v2 = Vector2D(4, 5)
        assert not v1 == v2

    def test_magnitude_sq(self) -> None:
        v = Vector2D(10, 5)
        assert v.magnitude_sq() == 125

    def test_magnitude(self) -> None:
        v = Vector2D(3, 4)
        assert v.magnitude() == 5

    def test_copy(self) -> None:
        v1 = Vector2D(3, 5)
        v2 = v1.copy()
        assert v1 == v2
        assert v1 is not v2

    def test_as_tuple(self) -> None:
        v = Vector2D(4.2, 2.1)
        assert v.as_tuple() == (4.2, 2.1)

    def test_as_int(self) -> None:
        v = Vector2D(5.8, 8.2)
        assert v.as_int() == (5, 8)

    def test_str(self) -> None:
        v = Vector2D(3, 4)
        assert str(v) == "<3,4>"
