import numpy as np

type TilePos = tuple[int, int]
type PixelCoord = tuple[int, int]
type MazeArray = np.ndarray[TilePos, np.dtype[np.str_]]
