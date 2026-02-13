from importlib.resources import files

import numpy as np

from vim_man.types import MazeArray


def get_maze_path(filename: str) -> str:
    """Return the absolute path to a maze data file bundled with the package."""
    return str(files("vim_man.data").joinpath(filename))


def read_maze_file(textfile: str) -> MazeArray:
    """Load the maze layout from a text file into a NumPy array."""
    filepath = get_maze_path(textfile)
    return np.loadtxt(filepath, dtype="<U1")
