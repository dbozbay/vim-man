import pygame
from vim_man.vector import Vector2D
from vim_man.constants import WHITE, RED, UP, DOWN, LEFT, RIGHT
from typing import Self


class Node(object):
    def __init__(self, x: float, y: float) -> None:
        self.position = Vector2D(x, y)
        self.neighbors: dict[int, Self | None] = {
            UP: None,
            DOWN: None,
            LEFT: None,
            RIGHT: None,
        }

    def render(self, screen: pygame.SurfaceType) -> None:
        for neighbor in self.neighbors.values():
            if neighbor is not None:
                line_start = self.position.as_tuple()
                line_end = neighbor.position.as_tuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.as_int(), 12)


class NodeGroup(object):
    def __init__(self) -> None:
        self.node_list: list[Node] = []

    def setup_test_nodes(self) -> None:
        nodeA = Node(80, 80)
        nodeB = Node(160, 80)
        nodeC = Node(80, 160)
        nodeD = Node(160, 160)
        nodeE = Node(208, 160)
        nodeF = Node(80, 320)
        nodeG = Node(208, 320)
        nodeA.neighbors[RIGHT] = nodeB
        nodeA.neighbors[DOWN] = nodeC
        nodeB.neighbors[LEFT] = nodeA
        nodeB.neighbors[DOWN] = nodeD
        nodeC.neighbors[UP] = nodeA
        nodeC.neighbors[RIGHT] = nodeD
        nodeC.neighbors[DOWN] = nodeF
        nodeD.neighbors[UP] = nodeB
        nodeD.neighbors[LEFT] = nodeC
        nodeD.neighbors[RIGHT] = nodeE
        nodeE.neighbors[LEFT] = nodeD
        nodeE.neighbors[DOWN] = nodeG
        nodeF.neighbors[UP] = nodeC
        nodeF.neighbors[RIGHT] = nodeG
        nodeG.neighbors[LEFT] = nodeF
        nodeG.neighbors[UP] = nodeE
        self.node_list = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

    def render(self, screen: pygame.SurfaceType) -> None:
        for node in self.node_list:
            node.render(screen)
