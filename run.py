import pygame

from vim_man.constants import BLACK, SCREENSIZE
from vim_man.nodes import NodeGroup
from vim_man.pacman import Pacman


class GameController(object):
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
        """Initialize the maze and Pacman, and prepare the game to start."""
        self.set_background()
        self.nodes = NodeGroup("mazetest.txt")
        self.pacman = Pacman(self.nodes.get_start_temp_node())

    def update(self) -> None:
        """Advance the game state by one frame, handling logic and rendering."""
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.check_events()
        self.render()

    def check_events(self) -> None:
        """Process incoming Pygame events and exit on a quit event."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def render(self) -> None:
        """Draw the current game state, including maze and Pacman, to the screen."""
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pacman.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
