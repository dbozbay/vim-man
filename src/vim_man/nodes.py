from __future__ import annotations

from typing import TYPE_CHECKING, Iterable
import numpy as np
import pygame

from vim_man.constants import (
    RED,
    TILEHEIGHT,
    TILEWIDTH,
    WHITE,
    Direction,
    EntityID,
    HORIZONTAL,
    VERTICAL,
)

from vim_man.types import MazeArray
from vim_man.vector import Vector2D

if TYPE_CHECKING:
    from vim_man.entity import Entity

type NodesLUT = dict[tuple[float, float], "Node"]


class Node:
    """Node represents a maze junction with links to its neighboring nodes."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize a node at a specific pixel position with no initial neighbors."""
        self.position = Vector2D(x, y)
        self.neighbors: dict[Direction, Node | None] = {
            Direction.UP: None,
            Direction.DOWN: None,
            Direction.LEFT: None,
            Direction.RIGHT: None,
            Direction.PORTAL: None,
        }
        self.access: dict[Direction, list[EntityID]] = {
            Direction.UP: [
                EntityID.PACMAN,
                EntityID.BLINKY,
                EntityID.PINKY,
                EntityID.INKY,
                EntityID.CLYDE,
                EntityID.FRUIT,
            ],
            Direction.DOWN: [
                EntityID.PACMAN,
                EntityID.BLINKY,
                EntityID.PINKY,
                EntityID.INKY,
                EntityID.CLYDE,
                EntityID.FRUIT,
            ],
            Direction.LEFT: [
                EntityID.PACMAN,
                EntityID.BLINKY,
                EntityID.PINKY,
                EntityID.INKY,
                EntityID.CLYDE,
                EntityID.FRUIT,
            ],
            Direction.RIGHT: [
                EntityID.PACMAN,
                EntityID.BLINKY,
                EntityID.PINKY,
                EntityID.INKY,
                EntityID.CLYDE,
                EntityID.FRUIT,
            ],
        }

    def deny_access(self, direction: Direction, entity: Entity) -> None:
        """Remove the entity from the access list for the given direction."""
        name = entity.name
        if name is not None and name in self.access[direction]:
            self.access[direction].remove(name)

    def allow_access(self, direction: Direction, entity: Entity) -> None:
        """Add the entity to the access list for the given direction."""
        name = entity.name
        if name is not None and name not in self.access[direction]:
            self.access[direction].append(name)

    def render(self, screen: pygame.Surface) -> None:
        """Draw the node and its connections to neighbors on the screen."""
        for neighbor, node in self.neighbors.items():
            if node is not None:
                line_start = self.position.as_tuple()
                line_end = node.position.as_tuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.as_int(), 12)


class NodeGroup:
    """Manages the creation and organization of the network of maze nodes."""

    def __init__(self, maze: MazeArray) -> None:
        """Initialize the node group by parsing the maze data and creating links."""
        self.maze = maze
        self.nodes_LUT: NodesLUT = {}
        self.node_symbols = ["+", "P", "n"]
        self.path_symbols = [".", "-", "|", "p"]

        data = self.maze.data
        self.create_node_table(data)
        self.connect_all(data)

        self.homekey: tuple[float, float]

    def create_node_table(self, data: MazeArray, x_offset: float = 0, y_offset: float = 0) -> None:
        """Create Node instances for all node symbols in the maze data."""
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in self.node_symbols:
                    x, y = self.construct_key(col + x_offset, row + y_offset)
                    self.nodes_LUT[(x, y)] = Node(x, y)

    def connect_all(self, data: MazeArray, x_offset: float = 0.0, y_offset: float = 0.0) -> None:
        """Connect horizontally adjacent node tiles as left and right neighbors."""
        # Walk each row from left to right, remembering the last node we saw.
        for orientation in [HORIZONTAL, VERTICAL]:
            # Created a connect function which will take in an orientation
            # and stride and perform the operations accordingly.
            self.connect(data, orientation, x_offset, y_offset)
            data = data.transpose()
            # equivalent to reading the relevant tile tuple forwards then backwards.
            print("connected once")

    def connect(
        self,
        data: MazeArray,
        orientation: tuple[Direction, Direction],
        x_offset: float,
        y_offset: float,
    ):
        if orientation == HORIZONTAL:
            # Read backwards
            stride = 1
            offset0, offset1 = x_offset, y_offset
        elif orientation == VERTICAL:
            # Read forwards
            stride = -1
            offset0, offset1 = y_offset, x_offset
        else:
            # I don't think this should ever happen so will just return None
            print("Invalid orientation may have been given.")
            return
        for row in range(data.shape[0]):
            key: tuple[float, float] | None = None
            for col in range(data.shape[1]):
                if data[row][col] in self.node_symbols:
                    relevant_tile = (col + offset0, row + offset1)
                    if key is None:
                        key = self.construct_key(*relevant_tile[::stride])
                    else:
                        otherkey = self.construct_key(*relevant_tile[::stride])
                        self.nodes_LUT[key].neighbors[orientation[0]] = self.nodes_LUT[otherkey]
                        self.nodes_LUT[otherkey].neighbors[orientation[1]] = self.nodes_LUT[key]
                        # First node in a new horizontal run; just record its key.
                        key = otherkey
                        # The star here means that each element is inserted as an argument.
                elif data[row][col] not in self.path_symbols:
                    key = None

    def construct_key(self, col: float, row: float) -> tuple[float, float]:
        """Convert tile coordinates to pixel coordinates used as lookup table keys."""
        return col * TILEWIDTH, row * TILEHEIGHT

    def create_home_nodes(self, x_offset: float, y_offset: float) -> tuple[float, float]:
        """Create a specialized set of nodes for the ghosts' starting area."""
        homedata = np.array(
            [
                ["X", "X", "+", "X", "X"],
                ["X", "X", ".", "X", "X"],
                ["+", "X", ".", "X", "+"],
                ["+", ".", "+", ".", "+"],
                ["+", "X", "X", "X", "+"],
            ]
        )
        self.create_node_table(homedata, x_offset, y_offset)
        self.connect_all(homedata, x_offset, y_offset)
        self.homekey = self.construct_key(x_offset + 2, y_offset)
        return self.homekey

    def connect_home_nodes(
        self,
        homekey: tuple[float, float],
        otherkey: tuple[float, float],
        direction: Direction,
    ) -> None:
        """Establish a bi-directional connection between the ghost house and the main maze."""
        key = self.construct_key(*otherkey)
        self.nodes_LUT[homekey].neighbors[direction] = self.nodes_LUT[key]
        self.nodes_LUT[key].neighbors[Direction(direction * -1)] = self.nodes_LUT[homekey]

    def set_portal_pair(self, pair1: tuple[int, int], pair2: tuple[int, int]) -> None:
        """Link two nodes as portals to allow teleportation between distant maze points."""
        key1 = self.construct_key(*pair1)
        key2 = self.construct_key(*pair2)
        if key1 in self.nodes_LUT and key2 in self.nodes_LUT:
            self.nodes_LUT[key1].neighbors[Direction.PORTAL] = self.nodes_LUT[key2]
            self.nodes_LUT[key2].neighbors[Direction.PORTAL] = self.nodes_LUT[key1]

    def get_node(self, col: float, row: float) -> Node:
        """Return the node at the given tile coordinates or raise common errors if missing."""
        node = self.get_node_from_tiles(col, row)
        if node is None:
            raise ValueError(f"No node found at tile coordinates ({col}, {row})")
        return node

    def get_node_from_tiles(self, col: float, row: float) -> Node | None:
        """Return the node at the given tile coordinates if it exists."""
        x, y = self.construct_key(col, row)
        return self.nodes_LUT.get((x, y))

    def get_node_from_pixels(self, x_pixel: float, y_pixel: float) -> Node | None:
        """Return the node at the given pixel coordinates if it exists."""
        return self.nodes_LUT.get((x_pixel, y_pixel))

    def get_start_temp_node(self) -> Node:
        """Return the first node created in the lookup table as a temporary starting point."""
        nodes = list(self.nodes_LUT.values())
        return nodes[0]

    def get_last_node(self) -> Node:
        """Return the last node created in the lookup table."""
        nodes = list(self.nodes_LUT.values())
        return nodes[-1]

    def allow_access(self, col: float, row: float, direction: Direction, entity: Entity) -> None:
        """Grant the entity access to move in the given direction from the specified tile."""
        node = self.get_node(col, row)
        node.allow_access(direction, entity)

    def deny_access(self, col: float, row: float, direction: Direction, entity: Entity) -> None:
        """Deny the entity access to move in the given direction from the specified tile."""
        node = self.get_node(col, row)
        node.deny_access(direction, entity)

    def allow_access_list(self, col: float, row: float, direction: Direction, entities: Iterable[Entity]) -> None:
        """Grant all entities access to move in the given direction from the specified tile."""
        for entity in entities:
            self.allow_access(col, row, direction, entity)

    def deny_access_list(self, col: float, row: float, direction: Direction, entities: Iterable[Entity]) -> None:
        """Deny all entities access to move in the given direction from the specified tile."""
        for entity in entities:
            self.deny_access(col, row, direction, entity)

    def allow_home_access(self, entity: Entity) -> None:
        """Grant the entity access to move downward into the ghost house."""
        self.nodes_LUT[self.homekey].allow_access(Direction.DOWN, entity)

    def deny_home_access(self, entity: Entity) -> None:
        """Deny the entity access to move downward into the ghost house."""
        self.nodes_LUT[self.homekey].deny_access(Direction.DOWN, entity)

    def allow_home_access_list(self, entities: Iterable[Entity]) -> None:
        """Grant all entities access to move downward into the ghost house."""
        for entity in entities:
            self.allow_home_access(entity)

    def deny_home_access_list(self, entities: Iterable[Entity]) -> None:
        """Deny all entities access to move downward into the ghost house."""
        for entity in entities:
            self.deny_home_access(entity)

    def render(self, screen: pygame.Surface) -> None:
        """Render all nodes and their connections in the group to the screen."""
        for node in self.nodes_LUT.values():
            node.render(screen)
