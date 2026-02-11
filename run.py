import pygame

from vim_man.constants import BLACK, SCREENSIZE
from vim_man.ghosts import Ghost
from vim_man.nodes import NodeGroup
from vim_man.pacman import Pacman
from vim_man.pellets import PelletGroup


class GameController(object):
    """GameController initializes and runs the main game loop for Vim-Man."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.set_background()
        self.clock = pygame.time.Clock()

    def set_background(self):
        """Create and fill the background surface for the game screen."""
        self.background = pygame.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def start_game(self) -> None:
        """Initialize the maze, Pacman, pellets, and prepare the game to start."""
        # self.set_background() # TODO: Do we need this when background is set in init?
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.set_portal_pair((0, 17), (27, 17))
        self.pacman = Pacman(self.nodes.get_start_temp_node())
        self.pellets = PelletGroup("maze1.txt")
        self.ghost = Ghost(self.nodes.get_start_temp_node())

    def check_pellet_events(self) -> None:
        """Update pellet state when Pacman eats a pellet."""
        pellet = self.pacman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.pellets.pellet_list.remove(pellet)

    def update(self) -> None:
        """Advance the game state by one frame, handling logic and rendering."""
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghost.update(dt)
        self.pellets.update(dt)
        self.check_pellet_events()
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
        self.ghost.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
