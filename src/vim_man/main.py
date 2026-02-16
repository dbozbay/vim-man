import pygame

from vim_man.constants import BLACK, MAZE, SCREENSIZE, Direction, EntityID, GhostMode
from vim_man.fruits import Fruit
from vim_man.ghosts import GhostGroup
from vim_man.level import Maze
from vim_man.nodes import NodeGroup
from vim_man.pacman import Pacman
from vim_man.pellets import PelletGroup
from vim_man.pauser import Pause


class GameController:
    """GameController initializes and runs the main game loop for Vim-Man."""

    def __init__(self) -> None:
        """Initialize the game environment, display, and controller state."""
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.pause = Pause(True)
        self.level = 0

        self.background: pygame.Surface | None = None
        self.maze: Maze | None = None
        self.nodes: NodeGroup | None = None
        self.pacman: Pacman | None = None
        self.pellets: PelletGroup | None = None
        self.ghosts: GhostGroup | None = None
        self.fruit: Fruit | None = None

    def set_background(self) -> None:
        """Create and fill the background surface for the game screen."""
        self.background = pygame.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def start_game(self) -> None:
        """Initialize the maze, Pacman, pellets, and prepare the game to start."""
        self.set_background()
        self.maze = Maze(MAZE)
        self.nodes = NodeGroup(self.maze)
        self.nodes.set_portal_pair((0, 17), (27, 17))
        homekey = self.nodes.create_home_nodes(11.5, 14)
        self.nodes.connect_home_nodes(homekey, (12, 14), Direction.LEFT)
        self.nodes.connect_home_nodes(homekey, (15, 14), Direction.RIGHT)
        self.pacman = Pacman(self.nodes.get_node(15, 26))
        self.pellets = PelletGroup(self.maze)
        self.ghosts = GhostGroup(self.nodes.get_start_temp_node(), self.pacman)
        self.ghosts.blinky.set_start_node(self.nodes.get_node(2 + 11.5, 0 + 14))
        self.ghosts.pinky.set_start_node(self.nodes.get_node(2 + 11.5, 3 + 14))
        self.ghosts.inky.set_start_node(self.nodes.get_node(0 + 11.5, 3 + 14))
        self.ghosts.clyde.set_start_node(self.nodes.get_node(4 + 11.5, 3 + 14))
        self.ghosts.set_spawn_node(self.nodes.get_node(2 + 11.5, 3 + 14))

    def check_pellet_events(self) -> None:
        """Update pellet state when Pacman eats a pellet."""
        if self.pellets is None or self.pacman is None or self.ghosts is None:
            return

        pellet = self.pacman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.pellets.pellet_list.remove(pellet)
            if pellet.name == EntityID.POWERPELLET:
                self.ghosts.start_freight()

            if self.pellets.is_empty():
                self.hide_entities()
                self.pause.set_pause(pause_time=3, func=self.next_level)

    def check_ghost_events(self) -> None:
        """Check for and handle collisions between Pacman and the ghosts."""
        if self.ghosts is None or self.pacman is None:
            return

        for ghost in self.ghosts:
            if self.pacman.collide_check(ghost):
                if ghost.mode.current is GhostMode.FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.pause.set_pause(pause_time=1, func=self.show_entities)
                    ghost.start_spawn()

    def check_fruit_events(self) -> None:
        """Check for and handle fruit appearance and consumption based on pellets eaten."""
        if self.pellets is None or self.pacman is None or self.nodes is None:
            return

        if self.pellets.num_eaten == 50 or self.pellets.num_eaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.get_node(9, 20))

        if self.fruit is not None:
            if self.pacman.collide_check(self.fruit):
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def update(self) -> None:
        """Advance the game state by one frame, handling logic and rendering."""
        dt = self.clock.tick(30) / 1000.0

        if not self.pause.paused:
            if self.pacman is not None:
                self.pacman.update(dt)
            if self.ghosts is not None:
                self.ghosts.update(dt)
            if self.pellets is not None:
                self.pellets.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)

            self.check_pellet_events()
            self.check_ghost_events()
            self.check_fruit_events()

        after_pause_method = self.pause.update(dt)
        if after_pause_method is not None:
            after_pause_method()

        self.check_events()
        self.render()

    def check_events(self) -> None:
        """Process incoming Pygame events and exit on a quit event."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause.set_pause(player_paused=True)
                    if not self.pause.paused:
                        self.show_entities()
                    else:
                        self.hide_entities()

    def show_entities(self) -> None:
        if self.pacman is not None:
            self.pacman.visible = True
        if self.ghosts is not None:
            self.ghosts.show()

    def hide_entities(self) -> None:
        if self.pacman is not None:
            self.pacman.visible = False
        if self.ghosts is not None:
            self.ghosts.hide()

    def next_level(self) -> None:
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.start_game()

    def render(self) -> None:
        """Draw the current game state (incl. maze, Pacman, Ghosts and pellets) to the screen."""
        if self.background is not None:
            self.screen.blit(self.background, (0, 0))
        if self.nodes is not None:
            self.nodes.render(self.screen)
        if self.pellets is not None:
            self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        if self.pacman is not None:
            self.pacman.render(self.screen)
        if self.ghosts is not None:
            self.ghosts.render(self.screen)

        pygame.display.update()


def main() -> None:
    """Initialize the game controller and start the primary game loop."""
    game = GameController()
    game.start_game()
    while True:
        game.update()


if __name__ == "__main__":
    main()
