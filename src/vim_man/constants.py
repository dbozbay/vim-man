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


class Direction(IntEnum):
    STOP = 0
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2
    PORTAL = 3


class EntityID(IntEnum):
    PACMAN = 0
    PELLET = 1
    POWERPELLET = 2
    GHOST = 3


class GhostMode(IntEnum):
    SCATTER = 0
    CHASE = 1
    FREIGHT = 2
    SPAWN = 3


MAZE: str = "maze1.txt"
