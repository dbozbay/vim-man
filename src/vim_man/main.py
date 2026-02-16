import pygame

from vim_man.constants import BLACK, MAZE, SCREENSIZE, EntityID, GhostMode
from vim_man.ghosts import GhostGroup
from vim_man.level import MazeLevel
from vim_man.nodes import NodeGroup
from vim_man.pacman import Pacman
from vim_man.pellets import PelletGroup


class GameController:
    """GameController initializes and runs the main game loop for Vim-Man."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.set_background()
        self.clock = pygame.time.Clock()

        self.level: MazeLevel
        self.nodes: NodeGroup
        self.pacman: Pacman
        self.pellets: PelletGroup
        self.ghosts: GhostGroup

    def set_background(self) -> None:
        """Create and fill the background surface for the game screen."""
        self.background = pygame.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def start_game(self) -> None:
        """Initialize the maze, Pacman, pellets, and prepare the game to start."""
        # self.set_background() # TODO: Do we need this when background is set in init?
        self.level = MazeLevel(MAZE)
        self.nodes = NodeGroup(self.level)
        self.nodes.set_portal_pair((0, 17), (27, 17))
        self.pacman = Pacman(self.nodes.get_start_temp_node())
        self.pellets = PelletGroup(self.level)
        self.ghosts = GhostGroup(self.nodes.get_start_temp_node(), self.pacman)
        self.ghosts.set_spawn_node(self.nodes.get_node_from_tiles(15,14))

    def check_pellet_events(self) -> None:
        """Update pellet state when Pacman eats a pellet."""
        pellet = self.pacman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.pellets.pellet_list.remove(pellet)
            if pellet.name == EntityID.POWERPELLET:
                self.ghosts.start_freight()

    def check_ghost_events(self):
        for ghost in self.ghosts:
            if self.pacman.collide_check(ghost):
                if ghost.mode.current is GhostMode.FREIGHT:
                    ghost.start_spawn()

    def update(self) -> None:
        """Advance the game state by one frame, handling logic and rendering."""
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghosts.update(dt)
        self.pellets.update(dt)
        self.check_pellet_events()
        self.check_ghost_events()
        self.check_events()
        self.render()

    def check_events(self) -> None:
        """Process incoming Pygame events and exit on a quit event."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def render(self) -> None:
        """Draw the current game state (incl. maze, Pacman, Ghosts and pellets) to the screen."""
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        pygame.display.update()


def main() -> None:
    game = GameController()
    game.start_game()
    while True:
        game.update()


if __name__ == "__main__":
    main()
