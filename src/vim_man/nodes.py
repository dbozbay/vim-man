import pygame

from vim_man.constants import (
    BLUE,
    RED,
    TILEHEIGHT,
    TILEWIDTH,
    WHITE,
    Direction,
)
from vim_man.level import MazeLevel
from vim_man.types import MazeArray
from vim_man.vector import Vector2D

type NodesLUT = dict[tuple[int, int], "Node"]


class Node:
    """Node represents a maze junction with links to its neighboring nodes."""

    def __init__(self, x: float, y: float) -> None:
        self.position = Vector2D(x, y)
        self.neighbors: dict[Direction, Node | None] = {
            Direction.UP: None,
            Direction.DOWN: None,
            Direction.LEFT: None,
            Direction.RIGHT: None,
            Direction.PORTAL: None,
        }

    def render(self, screen: pygame.Surface) -> None:
        """Draw this node and connecting lines to its neighboring nodes on the screen."""
        for neighbor, node in self.neighbors.items():
            if node is not None:
                line_start = self.position.as_tuple()
                line_end = node.position.as_tuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.as_int(), 12)


class NodeGroup:
    """NodeGroup loads a maze layout and manages the network of connected nodes."""

    def __init__(self, level: MazeLevel) -> None:
        # TODO: Write docstring
        self.level = level
        self.nodes_LUT: NodesLUT = {}
        self.node_symbols = ["+", "P", "n"]
        self.path_symbols = [".", "-", "|", "p"]
        data = self.level.data
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)

    def create_node_table(
        self, data: MazeArray, x_offset: int = 0, y_offset: int = 0
    ) -> None:
        """Create `Node` instances for all node symbols in the maze data and store them in the lookup table."""
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in self.node_symbols:
                    x, y = self.construct_key(col + x_offset, row + y_offset)
                    self.nodes_LUT[(x, y)] = Node(x, y)

    def construct_key(self, col: int, row: int) -> tuple[int, int]:
        """
        Return the pixel coordinates of the top-left corner of the given tile (col, row).
        This will be the node's key in the node lookup table.
        """
        return col * TILEWIDTH, row * TILEHEIGHT

    def connect_horizontally(
        self, data: MazeArray, x_offset: int = 0, y_offset: int = 0
    ) -> None:
        """Connect horizontally adjacent node tiles as left and right neighbors."""
        # Walk each row from left to right, remembering the last node we saw.
        for row in range(data.shape[0]):
            key: tuple[int, int] | None = None  # Start with no active node in this row.
            for col in range(data.shape[1]):
                if data[row][col] in self.node_symbols:
                    if key is None:
                        # First node in a new horizontal run; just record its key.
                        key = self.construct_key(col + x_offset, row + y_offset)
                    else:
                        # We have a previous node in this run, so connect it to this one.
                        otherkey = self.construct_key(col + x_offset, row + y_offset)
                        self.nodes_LUT[key].neighbors[Direction.RIGHT] = self.nodes_LUT[
                            otherkey
                        ]
                        self.nodes_LUT[otherkey].neighbors[Direction.LEFT] = (
                            self.nodes_LUT[key]
                        )
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
        for col in range(dataT.shape[0]):
            key: tuple[int, int] | None = (
                None  # Start with no active node in this column.
            )
            for row in range(dataT.shape[1]):
                if dataT[col][row] in self.node_symbols:
                    if key is None:
                        # First node in a new vertical run; just record its key.
                        key = self.construct_key(col + x_offset, row + y_offset)
                    else:
                        # We have a previous node in this column, so connect it to this one.
                        otherkey = self.construct_key(col + x_offset, row + y_offset)
                        self.nodes_LUT[key].neighbors[Direction.DOWN] = self.nodes_LUT[
                            otherkey
                        ]
                        self.nodes_LUT[otherkey].neighbors[Direction.UP] = (
                            self.nodes_LUT[key]
                        )
                        # This node becomes the new "previous" node for the run.
                        key = otherkey
                elif dataT[col][row] not in self.path_symbols:
                    # Hitting a wall or non-path tile breaks the current run.
                    key = None

    def set_portal_pair(self, pair1: tuple[int, int], pair2: tuple[int, int]) -> None:
        """Set the portal neighbors for the two given tile coordinates."""
        key1 = self.construct_key(*pair1)
        key2 = self.construct_key(*pair2)
        if key1 in self.nodes_LUT and key2 in self.nodes_LUT:
            self.nodes_LUT[key1].neighbors[Direction.PORTAL] = self.nodes_LUT[key2]
            self.nodes_LUT[key2].neighbors[Direction.PORTAL] = self.nodes_LUT[key1]

    def get_node_from_pixels(self, x_pixel: int, y_pixel: int) -> Node | None:
        """Return the node located at the given pixel coordinates, or `None` if none exists."""
        return self.nodes_LUT.get((x_pixel, y_pixel))

    def get_node_from_tiles(self, col: int, row: int) -> Node | None:
        """Return the node at the given tile coordinates, or `None` if none exists."""
        x, y = self.construct_key(col, row)
        return self.nodes_LUT.get((x, y))

    def get_start_temp_node(self) -> Node:
        nodes = list(self.nodes_LUT.values())
        return nodes[0]

    def get_last_node(self) -> Node:
        """Return the last node in the nodes lookup table."""
        nodes = list(self.nodes_LUT.values())
        return nodes[-1]

    def render(self, screen: pygame.SurfaceType) -> None:
        """Render all nodes in the node group to the screen."""
        for node in self.nodes_LUT.values():
            node.render(screen)
