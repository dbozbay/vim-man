from enum import IntEnum

type Color = tuple[int, int, int]

TILEWIDTH: int = 16
TILEHEIGHT: int = 16
NROWS: int = 36
NCOLS: int = 28
SCREENWIDTH: int = NCOLS * TILEWIDTH
SCREENHEIGHT: int = NROWS * TILEHEIGHT
SCREENSIZE: tuple[int, int] = (SCREENWIDTH, SCREENHEIGHT)


BASETILEWIDTH: int = 16
BASETILEHEIGHT: int = 16

GHOST_HOUSE_X_OFFSET: float = 11.5
GHOST_HOUSE_Y_OFFSET: float = 14


class Direction(IntEnum):
    """Enumeration of possible movement directions including portal transitions."""

    STOP = 0
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2
    PORTAL = 3


PORTAL_LEFT: tuple[int, int] = (0, 17)
PORTAL_RIGHT: tuple[int, int] = (27, 17)

GHOST_DOOR_LEFT: tuple[int, int] = (12, 14)
GHOST_DOOR_RIGHT: tuple[int, int] = (15, 14)

PACMAN_START: tuple[int, int] = (15, 26)

BLINKY_START: tuple[float, float] = (2 + GHOST_HOUSE_X_OFFSET, 0 + GHOST_HOUSE_Y_OFFSET)
PINKY_START: tuple[float, float] = (2 + GHOST_HOUSE_X_OFFSET, 3 + GHOST_HOUSE_Y_OFFSET)
INKY_START: tuple[float, float] = (0 + GHOST_HOUSE_X_OFFSET, 3 + GHOST_HOUSE_Y_OFFSET)
CLYDE_START: tuple[float, float] = (4 + GHOST_HOUSE_X_OFFSET, 3 + GHOST_HOUSE_Y_OFFSET)
GHOST_SPAWN: tuple[float, float] = (2 + GHOST_HOUSE_X_OFFSET, 3 + GHOST_HOUSE_Y_OFFSET)

GHOST_HOUSE_DOOR_UP_POSITIONS: list[tuple[int, int]] = [
    (12, 14),
    (15, 14),
    (12, 26),
    (15, 26),
]

GHOST_ACCESS_POSITIONS: list[tuple[float, float, Direction]] = [
    (2 + GHOST_HOUSE_X_OFFSET, 3 + GHOST_HOUSE_Y_OFFSET, Direction.LEFT),
    (2 + GHOST_HOUSE_X_OFFSET, 3 + GHOST_HOUSE_Y_OFFSET, Direction.RIGHT),
]

PELLET_UNLOCK_INKY: int = 30
PELLET_UNLOCK_CLYDE: int = 70

FRUIT_APPEAR_PELLET_COUNT: list[int] = [50, 140]

BLACK: Color = (0, 0, 0)
YELLOW: Color = (255, 255, 0)
BLUE: Color = (0, 0, 255)
WHITE: Color = (255, 255, 255)
RED: Color = (255, 0, 0)
PINK: Color = (255, 100, 150)
TEAL: Color = (100, 255, 255)
ORANGE: Color = (230, 190, 40)
GREEN: Color = (0, 255, 0)


STARTING_LIVES: int = 3

SCATTER_TIME: float = 7.0
CHASE_TIME: float = 20.0
FREIGHT_TIME: float = 7.0

MAZE: str = "maze1.txt"


class EntityID(IntEnum):
    """Enumeration of unique identifiers for all game entities and items."""

    PACMAN = 0
    PELLET = 1
    POWERPELLET = 2
    GHOST = 3
    BLINKY = 4
    PINKY = 5
    INKY = 6
    CLYDE = 7
    FRUIT = 8


class GhostMode(IntEnum):
    """Enumeration of possible behavioral states for ghosts."""

    SCATTER = 0
    CHASE = 1
    FREIGHT = 2
    SPAWN = 3


class TextID(IntEnum):
    SCORETEXT = 0
    LEVELTEXT = 1
    READYTEXT = 2
    PAUSETEXT = 3
    GAMEOVERTEXT = 4
