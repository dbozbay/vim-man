import pygame

from vim_man.constants import BLACK, MAZE, SCREENSIZE, Direction, EntityID, GhostMode
from vim_man.fruits import Fruit
from vim_man.ghosts import GhostGroup
from vim_man.level import Maze
from vim_man.nodes import NodeGroup
from vim_man.pacman import Pacman
from vim_man.pauser import Pause
from vim_man.pellets import PelletGroup


class GameController:
    """GameController initializes and runs the main game loop for Vim-Man."""

    def __init__(self) -> None:
        """Initialize the game environment, display, and controller state."""
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.pause = Pause(True)
        self.level = 0
        self.lives = 3
        self.fruit: Fruit | None = None

        self.background: pygame.Surface
        self.maze: Maze
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
        self.set_background()

        # Initialize maze / nodes
        self.maze = Maze(MAZE)
        self.nodes = NodeGroup(self.maze)
        self.nodes.set_portal_pair((0, 17), (27, 17))
        homekey = self.nodes.create_home_nodes(11.5, 14)
        self.nodes.connect_home_nodes(homekey, (12, 14), Direction.LEFT)
        self.nodes.connect_home_nodes(homekey, (15, 14), Direction.RIGHT)

        # Initialize Entities (Pacman, Ghosts, Pellets)
        self.pacman = Pacman(self.nodes.get_node(15, 26))
        self.pellets = PelletGroup(self.maze)
        self.ghosts = GhostGroup(self.nodes.get_start_temp_node(), self.pacman)
        self.ghosts.blinky.set_start_node(self.nodes.get_node(2 + 11.5, 0 + 14))
        self.ghosts.pinky.set_start_node(self.nodes.get_node(2 + 11.5, 3 + 14))
        self.ghosts.inky.set_start_node(self.nodes.get_node(0 + 11.5, 3 + 14))
        self.ghosts.clyde.set_start_node(self.nodes.get_node(4 + 11.5, 3 + 14))
        self.ghosts.set_spawn_node(self.nodes.get_node(2 + 11.5, 3 + 14))

        # Initialize access rights to nodes
        self.nodes.deny_home_access(self.pacman)
        self.nodes.deny_home_access_list(self.ghosts)
        self.nodes.deny_access_list(2 + 11.5, 3 + 14, Direction.LEFT, self.ghosts)
        self.nodes.deny_access_list(2 + 11.5, 3 + 14, Direction.RIGHT, self.ghosts)
        self.ghosts.inky.start_node.deny_access(Direction.RIGHT, self.ghosts.inky)
        self.ghosts.clyde.start_node.deny_access(Direction.LEFT, self.ghosts.clyde)
        self.nodes.deny_access_list(12, 14, Direction.UP, self.ghosts)
        self.nodes.deny_access_list(15, 14, Direction.UP, self.ghosts)
        self.nodes.deny_access_list(12, 26, Direction.UP, self.ghosts)
        self.nodes.deny_access_list(15, 26, Direction.UP, self.ghosts)

    def restart_game(self) -> None:
        self.lives = 3
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.start_game()

    def reset_level(self) -> None:
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None

    def check_pellet_events(self) -> None:
        """Update pellet state when Pacman eats a pellet."""
        pellet = self.pacman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1

            if self.pellets.num_eaten == 30:
                self.ghosts.inky.start_node.allow_access(Direction.RIGHT, self.ghosts.inky)

            if self.pellets.num_eaten == 70:
                self.ghosts.clyde.start_node.allow_access(Direction.LEFT, self.ghosts.clyde)

            self.pellets.pellet_list.remove(pellet)

            if pellet.name == EntityID.POWERPELLET:
                self.ghosts.start_freight()

            if self.pellets.is_empty():
                self.hide_entities()
                self.pause.set_pause(pause_time=3, func=self.next_level)

    def check_ghost_events(self) -> None:
        """Check for and handle collisions between Pacman and the ghosts."""
        for ghost in self.ghosts:
            if self.pacman.collide_check(ghost):
                if ghost.mode.current is GhostMode.FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.pause.set_pause(pause_time=1, func=self.show_entities)
                    ghost.start_spawn()
                    self.nodes.allow_home_access(ghost)

                elif ghost.mode.current is not GhostMode.SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.pacman.die()
                        self.ghosts.hide()

                        if self.lives <= 0:
                            self.pause.set_pause(pause_time=3, func=self.restart_game)
                        else:
                            self.pause.set_pause(pause_time=3, func=self.reset_level)

    def check_fruit_events(self) -> None:
        """Check for and handle fruit appearance and consumption based on pellets eaten."""
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
            self.pacman.update(dt)
            self.ghosts.update(dt)
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
                if event.key == pygame.K_SPACE:
                    if self.pacman.alive:
                        self.pause.set_pause(player_paused=True)
                        if not self.pause.paused:
                            self.show_entities()
                        else:
                            self.hide_entities()

    def show_entities(self) -> None:
        """Make Pacman and all ghosts visible on the screen."""
        self.pacman.visible = True
        self.ghosts.show()

    def hide_entities(self) -> None:
        """Make Pacman and all ghosts invisible on the screen."""
        self.pacman.visible = False
        self.ghosts.hide()

    def next_level(self) -> None:
        """Reset the game state and advance to the next level of the maze."""
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.start_game()

    def render(self) -> None:
        """Draw the current game state (incl. maze, Pacman, Ghosts and pellets) to the screen."""
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
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
