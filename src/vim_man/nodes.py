import pygame

from vim_man.constants import (
    BLUE,
    RED,
    TILEHEIGHT,
    TILEWIDTH,
    WHITE,
    Direction,
    VERTICAL,
    HORIZONTAL
)

from vim_man.level import MazeLevel
from vim_man.types import MazeArray
from vim_man.vector import Vector2D

type NodesLUT = dict[tuple[int, int], "Node"]
# LUT = lookup table


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
                if neighbor == Direction.PORTAL:
                    line_color = BLUE
                else:
                    line_color = WHITE
                pygame.draw.line(screen, line_color, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.as_int(), 12)


class NodeGroup:
    """NodeGroup loads a maze layout and manages the network of connected nodes."""

    def __init__(self, level: MazeLevel) -> None:
        # TODO: Write docstring
        self.level = level
        self.nodes_LUT: NodesLUT = {}
        self.node_symbols = ["+", "P", "n", "S"]
        self.path_symbols = [".", "-", "|", "p"]
        self.start_node: Node | None = None
        data = self.level.data
        self.create_node_table(data)
        self.connect_all(data)
        # See line 83

    def create_node_table(
        self, data: MazeArray, x_offset: int = 0, y_offset: int = 0
    ) -> None:
        """Create `Node` instances for all node symbols in the maze data and store them in the lookup table."""
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in self.node_symbols:
                    x, y = self.construct_key(col + x_offset, row + y_offset)
                    new_node = Node(x, y)
                    self.nodes_LUT[(x, y)] = new_node
                    if data[row][col] == "S":
                        self.start_node = new_node

    def construct_key(self, col: int, row: int) -> tuple[int, int]:
        """
        Return the pixel coordinates of the top-left corner of the given tile (col, row).
        This will be the node's key in the node lookup table.
        """
        return col * TILEWIDTH, row * TILEHEIGHT
    
    # it looks like you're doing similar things
    # when connecting horizontally and vertically.
    # is there a way to reduce the amount of times
    # you are putting in this loop?

    def connect_all(
        self, data: MazeArray, x_offset: int = 0, y_offset: int = 0
    ) -> None:
        """Connect horizontally adjacent node tiles as left and right neighbors."""
        # Walk each row from left to right, remembering the last node we saw.
        vertical = (Direction.DOWN, Direction.UP)
        horizontal = (Direction.RIGHT, Direction.LEFT)
        stride = 1
        for orientation in [horizontal, vertical]:
            # Created a connect function which will take in an orientation
            # and stride and perform the operations accordingly. 
            self.connect(data, orientation, stride, x_offset, y_offset)
            data = data.transpose()
            stride -= 2 # This will turn the stride from 1 to -1, 
            # equivalent to reading the relevant tile tuple forwards then backwards.
            print("connected once")

    def connect(self, data: MazeArray, orientation: tuple[Direction, Direction], stride: int, x_offset: int, y_offset: int):
        for row in range(data.shape[0]):
            key: tuple[int, int] | None = None  # Start with no active node in this row.
            for col in range(data.shape[1]):
                if data[row][col] in self.node_symbols:
                    relevant_tile = (col + x_offset, row + y_offset)
                    if key is None:
                        # First node in a new horizontal run; just record its key.
                        key = self.construct_key(*relevant_tile[::stride])
                        # The star here means that each element is inserted as an argument. 
                    else:
                        # We have a previous node in this run, so connect it to this one.
                        otherkey = self.construct_key(*relevant_tile[::stride])
                        self.nodes_LUT[key].neighbors[orientation[0]] = self.nodes_LUT[
                            otherkey
                        ]
                        self.nodes_LUT[otherkey].neighbors[orientation[1]] = (
                            self.nodes_LUT[key]
                        )
                        # This node becomes the new "previous" node for the run.
                        key = otherkey
                elif data[row][col] not in self.path_symbols:
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
        return self.get_node_from_pixels(x, y)

    def get_start_node(self) -> Node:
        """Return the starting node for Pacman."""
        if self.start_node is None:
            # Fallback if no S node found, though arguably check should happen at load time
            return list(self.nodes_LUT.values())[0]
        return self.start_node

    def get_last_node(self) -> Node:
        """Return the last node in the nodes lookup table."""
        nodes = list(self.nodes_LUT.values())
        return nodes[-1]

    def render(self, screen: pygame.SurfaceType) -> None:
        """Render all nodes in the node group to the screen."""
        for node in self.nodes_LUT.values():
            node.render(screen)
