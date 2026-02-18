from unittest.mock import patch

import numpy as np

from vim_man.level import Maze


def test_maze_load() -> None:
    """Test that the Maze class can load a maze file."""
    with patch("vim_man.level.Maze.read_maze_file") as mock_read:
        mock_read.return_value = np.array([[".", "#"], ["#", "."]])
        level = Maze("dummy.txt")

        # Verify the maze is not loaded yet
        assert level._data is None

        # Load the maze
        data = level.data

        # Verify the maze is loaded
        assert data is not None
        mock_read.assert_called_once_with("dummy.txt")
        assert data.shape == (2, 2)

        # Verify second access doesn't read file again
        _ = level.data
        mock_read.assert_called_once()
