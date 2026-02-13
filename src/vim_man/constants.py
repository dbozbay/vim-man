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

STOP: int = 0
UP: int = 1
DOWN: int = -1
LEFT: int = 2
RIGHT: int = -2
PORTAL: int = 3

PACMAN: int = 0
PELLET: int = 1
POWERPELLET: int = 2
GHOST: int = 3

SCATTER: int = 0
CHASE: int = 1
FREIGHT: int = 2
SPAWN: int = 3

MAZE: str = "maze1.txt"
