from enum import IntEnum

type Color = tuple[int, int, int]

TILEWIDTH: int = 16
TILEHEIGHT: int = 16
NROWS: int = 36
NCOLS: int = 28
SCREENWIDTH: int = NCOLS * TILEWIDTH
SCREENHEIGHT: int = NROWS * TILEHEIGHT
SCREENSIZE: tuple[int, int] = (SCREENWIDTH, SCREENHEIGHT)

BLACK: Color = (0, 0, 0)
YELLOW: Color = (255, 255, 0)
BLUE: Color = (0, 0, 255)
WHITE: Color = (255, 255, 255)
RED: Color = (255, 0, 0)
PINK: Color = (255, 100, 150)
TEAL: Color = (100, 255, 255)
ORANGE: Color = (230, 190, 40)


SCATTER_TIME: float = 7.0
CHASE_TIME: float = 20.0
FREIGHT_TIME: float = 7.0

MAZE: str = "maze1.txt"


class Direction(IntEnum):
    STOP = 0
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2
    PORTAL = 3

VERTICAL = (Direction.DOWN, Direction.UP)
HORIZONTAL = (Direction.LEFT, Direction.RIGHT)

class EntityID(IntEnum):
    PACMAN = 0
    PELLET = 1
    POWERPELLET = 2
    GHOST = 3
    BLINKY = 4
    PINKY = 5
    INKY = 6
    CLYDE = 7


class GhostMode(IntEnum):
    SCATTER = 0
    CHASE = 1
    FREIGHT = 2
    SPAWN = 3
