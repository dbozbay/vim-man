import numpy as np
import pygame

from vim_man.constants import DOWN, LEFT, RED, RIGHT, TILEHEIGHT, TILEWIDTH, UP, WHITE
from vim_man.vector import Vector2D

type NodeKey = tuple[int, int]
type NodesLUT = dict[NodeKey, "Node"]
type MazeArray = np.ndarray[NodeKey, np.dtype[np.str_]]


class Node(object):
    def __init__(self, x: float, y: float) -> None:
        self.position = Vector2D(x, y)
        self.neighbors: dict[int, Node | None] = {
            UP: None,
            DOWN: None,
            LEFT: None,
            RIGHT: None,
        }

    def render(self, screen: pygame.SurfaceType) -> None:
        """Draw this node and connecting lines to its neighboring nodes on the screen."""
        for neighbor in self.neighbors.values():
            if neighbor is not None:
                line_start = self.position.as_tuple()
                line_end = neighbor.position.as_tuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.as_int(), 12)


class NodeGroup(object):
    def __init__(self, level: str) -> None:
        self.level = level
        self.nodes_LUT: NodesLUT = {}
        self.node_symbols = ["+"]
        self.path_symbols = ["."]
        data = self.read_maze_file(level)
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)

    def read_maze_file(self, textfile: str) -> MazeArray:
        """Load the maze layout from a text file into a NumPy array."""
        return np.loadtxt(textfile, dtype="<U1")

    def create_node_table(
        self, data: MazeArray, x_offset: int = 0, y_offset: int = 0
    ) -> None:
        """Create `Node` instances for all node symbols in the maze data and store them in the lookup table."""
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    x, y = self.construct_key(col + x_offset, row + y_offset)
                    self.nodes_LUT[(x, y)] = Node(x, y)

    def construct_key(self, x: int, y: int) -> NodeKey:
        """Convert tile coordinates into pixel coordinates used as node keys."""
        return x * TILEWIDTH, y * TILEHEIGHT

    def connect_horizontally(
        self, data: MazeArray, x_offset: int = 0, y_offset: int = 0
    ) -> None:
        """Connect horizontally adjacent node tiles as left and right neighbors."""
        for row in list(range(data.shape[0])):
            key: NodeKey | None = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col + x_offset, row + y_offset)
                    else:
                        otherkey = self.construct_key(col + x_offset, row + y_offset)
                        self.nodes_LUT[key].neighbors[RIGHT] = self.nodes_LUT[otherkey]
                        self.nodes_LUT[otherkey].neighbors[LEFT] = self.nodes_LUT[key]
                        key = otherkey
                elif data[row][col] not in self.path_symbols:
                    key = None

    def connect_vertically(
        self, data: MazeArray, x_offset: int = 0, y_offset: int = 0
    ) -> None:
        """Connect vertically adjacent node tiles as up and down neighbors."""
        dataT = data.transpose()  # (row, col) -> (col, row)
        for col in list(range(dataT.shape[0])):
            key: NodeKey | None = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col + x_offset, row + y_offset)
                    else:
                        otherkey = self.construct_key(col + x_offset, row + y_offset)
                        self.nodes_LUT[key].neighbors[DOWN] = self.nodes_LUT[otherkey]
                        self.nodes_LUT[otherkey].neighbors[UP] = self.nodes_LUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.path_symbols:
                    key = None

    def get_node_from_pixels(self, x_pixel: int, y_pixel: int) -> Node | None:
        """Return the node located at the given pixel coordinates, or `None` if none exists."""
        return self.nodes_LUT.get((x_pixel, y_pixel))

    def get_node_from_tiles(self, col: int, row: int) -> Node | None:
        """Return the node at the given tile coordinates, or `None` if none exists."""
        x, y = self.construct_key(col, row)
        return self.get_node_from_pixels(x, y)

    def get_start_temp_node(self) -> Node:
        """Return the temporary starting node for Pacman from the node lookup table."""
        # TODO: For now this will be the first node in the lookup stable. Change later on.
        nodes = list(self.nodes_LUT.values())
        return nodes[0]

    def render(self, screen: pygame.SurfaceType) -> None:
        """Render all nodes in the node group to the screen."""
        for node in self.nodes_LUT.values():
            node.render(screen)
