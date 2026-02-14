from unittest.mock import patch

import numpy as np

from vim_man.level import MazeLevel


def test_maze_level_load() -> None:
    with patch("vim_man.level.read_maze_file") as mock_read:
        mock_read.return_value = np.array([[".", "#"], ["#", "."]])
        level = MazeLevel("dummy.txt")
        assert level._data is None
        data = level.data
        assert data is not None
        mock_read.assert_called_once_with("dummy.txt")
        assert data.shape == (2, 2)
        # Verify second access doesn't read file again
        _ = level.data
        mock_read.assert_called_once()
