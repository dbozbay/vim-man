import numpy as np
import pygame

from vim_man.constants import (
    BLUE,
    DOWN,
    LEFT,
    PORTAL,
    RED,
    RIGHT,
    TILEHEIGHT,
    TILEWIDTH,
    UP,
    WHITE,
)
from vim_man.vector import Vector2D

type NodeKey = tuple[int, int]
type NodesLUT = dict[NodeKey, "Node"]
type MazeArray = np.ndarray[NodeKey, np.dtype[np.str_]]


class Node(object):
    """Node represents a maze junction with links to its neighboring nodes."""

    def __init__(self, x: float, y: float) -> None:
        self.position = Vector2D(x, y)
        self.neighbors: dict[int, Node | None] = {
            UP: None,
            DOWN: None,
            LEFT: None,
            RIGHT: None,
            PORTAL: None,
        }

    def render(self, screen: pygame.SurfaceType) -> None:
        """Draw this node and connecting lines to its neighboring nodes on the screen."""
        for neighbor, node in self.neighbors.items():
            if node is not None:
                line_start = self.position.as_tuple()
                line_end = node.position.as_tuple()
                if neighbor == PORTAL:
                    line_color = BLUE
                else:
                    line_color = WHITE
                pygame.draw.line(screen, line_color, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.as_int(), 12)


class NodeGroup(object):
    """NodeGroup loads a maze layout and manages the network of connected nodes."""

    def __init__(self, level: str) -> None:
        self.level = level
        self.nodes_LUT: NodesLUT = {}
        self.node_symbols = ["+", "P", "n"]
        self.path_symbols = [".", "-", "|", "p"]
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
        # Walk each row from left to right, remembering the last node we saw.
        for row in list(range(data.shape[0])):
            key: NodeKey | None = None  # Start with no active node in this row.
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    if key is None:
                        # First node in a new horizontal run; just record its key.
                        key = self.construct_key(col + x_offset, row + y_offset)
                    else:
                        # We have a previous node in this run, so connect it to this one.
                        otherkey = self.construct_key(col + x_offset, row + y_offset)
                        self.nodes_LUT[key].neighbors[RIGHT] = self.nodes_LUT[otherkey]
                        self.nodes_LUT[otherkey].neighbors[LEFT] = self.nodes_LUT[key]
                        # This node becomes the new "previous" node for the run.
                        key = otherkey
                elif data[row][col] not in self.path_symbols:
                    # Hitting a wall or non-path tile breaks the current run.
                    key = None

    def connect_vertically(
        self, data: MazeArray, x_offset: int = 0, y_offset: int = 0
    ) -> None:
        """Connect vertically adjacent node tiles as up and down neighbors."""
        # Transpose so we can reuse the same "scan along rows" logic for columns.
        dataT = data.transpose()  # (row, col) -> (col, row)
        for col in list(range(dataT.shape[0])):
            key: NodeKey | None = None  # Start with no active node in this column.
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.node_symbols:
                    if key is None:
                        # First node in a new vertical run; just record its key.
                        key = self.construct_key(col + x_offset, row + y_offset)
                    else:
                        # We have a previous node in this column, so connect it to this one.
                        otherkey = self.construct_key(col + x_offset, row + y_offset)
                        self.nodes_LUT[key].neighbors[DOWN] = self.nodes_LUT[otherkey]
                        self.nodes_LUT[otherkey].neighbors[UP] = self.nodes_LUT[key]
                        # This node becomes the new "previous" node for the run.
                        key = otherkey
                elif dataT[col][row] not in self.path_symbols:
                    # Hitting a wall or non-path tile breaks the current run.
                    key = None

    def set_portal_pair(self, pair1: NodeKey, pair2: NodeKey) -> None:
        """Set the portal neighbors for the two given node keys."""
        key1 = self.construct_key(*pair1)
        key2 = self.construct_key(*pair2)
        if key1 in self.nodes_LUT.keys() and key2 in self.nodes_LUT.keys():
            self.nodes_LUT[key1].neighbors[PORTAL] = self.nodes_LUT[key2]
            self.nodes_LUT[key2].neighbors[PORTAL] = self.nodes_LUT[key1]

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
