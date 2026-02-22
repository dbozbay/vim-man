from importlib.resources import files

import numpy as np

from vim_man.types import MazeArray


class Maze:
    """Maze loads and holds the maze layout data."""

    def __init__(self, level_file: str, rotation_file: str | None = None) -> None:
        """Initialize the level with the name of the maze layout file."""
        self.level_file = level_file
        self.rotation_file = rotation_file
        self._data: MazeArray | None = None
        self._rot_data: MazeArray | None = None

    @property
    def data(self) -> MazeArray:
        """Return the maze layout as a NumPy array. Loads it on first access."""
        if self._data is None:
            self._data = self.read_maze_file(self.level_file)
        return self._data

    @property
    def rot_data(self) -> MazeArray | None:
        if self.rotation_file is None:
            return None
        if self._rot_data is None:
            self._rot_data = self.read_maze_file(self.rotation_file)
        return self._rot_data

    def get_maze_path(self, filename: str) -> str:
        """Return the absolute path to a maze data file bundled with the package."""
        return str(files("vim_man.data").joinpath(filename))

    def read_maze_file(self, textfile: str) -> MazeArray:
        """Load the maze layout from a text file into a NumPy array."""
        filepath = self.get_maze_path(textfile)
        return np.loadtxt(filepath, dtype="<U1")
