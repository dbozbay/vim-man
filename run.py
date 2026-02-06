import pygame
from vim_man.constants import SCREENSIZE, BLACK
from pygame.locals import QUIT


class GameController(object):
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None

    def set_background(self) -> None:
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def start_game(self) -> None:
        self.set_background()

    def update(self) -> None:
        self.check_events()
        self.render()

    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self) -> None:
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
