from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pygame

from vim_man.constants import (
    RED,
    TILEHEIGHT,
    TILEWIDTH,
    WHITE,
    Direction,
    EntityID,
)
from vim_man.level import Maze
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
        name = entity.name
        if name is not None and name in self.access[direction]:
            self.access[direction].remove(name)

    def allow_access(self, direction: Direction, entity: Entity) -> None:
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

    def __init__(self, maze: Maze) -> None:
        """Initialize the node group by parsing the maze data and creating links."""
        self.maze = maze
        self.nodes_LUT: NodesLUT = {}
        self.node_symbols = ["+", "P", "n"]
        self.path_symbols = [".", "-", "|", "p"]
        data = self.maze.data
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)
        self.homekey = None

    def create_node_table(self, data: MazeArray, x_offset: float = 0, y_offset: float = 0) -> None:
        """Create Node instances for all node symbols in the maze data."""
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in self.node_symbols:
                    x, y = self.construct_key(col + x_offset, row + y_offset)
                    self.nodes_LUT[(x, y)] = Node(x, y)

    def connect_horizontally(self, data: MazeArray, x_offset: float = 0, y_offset: float = 0) -> None:
        """Establish left and right neighbor connections between nodes in the same row."""
        for row in range(data.shape[0]):
            key: tuple[float, float] | None = None
            for col in range(data.shape[1]):
                if data[row][col] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col + x_offset, row + y_offset)
                    else:
                        otherkey = self.construct_key(col + x_offset, row + y_offset)
                        self.nodes_LUT[key].neighbors[Direction.RIGHT] = self.nodes_LUT[otherkey]
                        self.nodes_LUT[otherkey].neighbors[Direction.LEFT] = self.nodes_LUT[key]
                        key = otherkey
                elif data[row][col] not in self.path_symbols:
                    key = None

    def connect_vertically(self, data: MazeArray, x_offset: float = 0, y_offset: float = 0) -> None:
        """Establish up and down neighbor connections between nodes in the same column."""
        dataT = data.transpose()
        for col in range(dataT.shape[0]):
            key: tuple[float, float] | None = None
            for row in range(dataT.shape[1]):
                if dataT[col][row] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col + x_offset, row + y_offset)
                    else:
                        otherkey = self.construct_key(col + x_offset, row + y_offset)
                        self.nodes_LUT[key].neighbors[Direction.DOWN] = self.nodes_LUT[otherkey]
                        self.nodes_LUT[otherkey].neighbors[Direction.UP] = self.nodes_LUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.path_symbols:
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
        self.connect_horizontally(homedata, x_offset, y_offset)
        self.connect_vertically(homedata, x_offset, y_offset)
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
        node = self.get_node(col, row)
        node.allow_access(direction, entity)

    def deny_access(self, col: float, row: float, direction: Direction, entity: Entity) -> None:
        node = self.get_node(col, row)
        node.deny_access(direction, entity)

    def allow_access_list(self, col: float, row: float, direction: Direction, entities: list[Entity]) -> None:
        for entity in entities:
            self.allow_access(col, row, direction, entity)

    def deny_access_list(self, col: float, row: float, direction: Direction, entities: list[Entity]) -> None:
        for entity in entities:
            self.deny_access(col, row, direction, entity)

    def allow_home_access(self, entity: Entity) -> None:
        if self.homekey is not None:
            self.nodes_LUT[self.homekey].allow_access(Direction.DOWN, entity)

    def deny_home_access(self, entity: Entity) -> None:
        if self.homekey is not None:
            self.nodes_LUT[self.homekey].deny_access(Direction.DOWN, entity)

    def allow_home_access_list(self, entities: list[Entity]) -> None:
        for entity in entities:
            self.allow_home_access(entity)

    def deny_home_access_list(self, entities: list[Entity]) -> None:
        for entity in entities:
            self.deny_home_access(entity)

    def render(self, screen: pygame.Surface) -> None:
        """Render all nodes and their connections in the group to the screen."""
        for node in self.nodes_LUT.values():
            node.render(screen)
