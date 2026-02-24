# vim-man

A Python implementation of the classic arcade game Pac-Man, controlled with Vim motions.
Navigate the maze using `h`, `j`, `k`, and `l` — because arrow keys are for quitters.

Built with [Pygame](https://www.pygame.org/) and [NumPy](https://numpy.org/). Managed with [uv](https://github.com/astral-sh/uv).

---

## Features

- **Vim-native controls** — `h` (left), `j` (down), `k` (up), `l` (right)
- **Graph-based maze navigation** — nodes and edges parsed directly from a text-based maze layout file
- **Portal (warp tunnel) support** — walk off one side of the screen and appear on the other
- **Ghost AI** — ghosts alternate between Scatter, Chase, and Freight modes on a timer
- **Power pellets** — eat a power pellet to send ghosts into Freight mode and earn bonus points
- **Ghost–Pacman collision** — collision detection with death and respawn
- **Lives system** — start with 3 lives, game over when depleted
- **Fruits** — bonus items appear at 50 and 140 pellets eaten
- **Pause** — press Space to pause/unpause the game

---

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (package and project manager)

---

## Installation

If you don't have `uv` installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> See the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/) for alternative methods (Homebrew, pip, Windows, etc.).

Then clone and install the project:

```bash
git clone https://github.com/dbozbay/vim-man.git
cd vim-man
uv sync --locked --all-extras --dev
```

---

## Running the Game

```bash
uv run vim-man
```

---

## Controls

| Key  | Action        |
|------|---------------|
| `h`  | Move left     |
| `j`  | Move down     |
| `k`  | Move up       |
| `l`  | Move right    |
| `SPACE` | Pause/Unpause |

---

## Project Structure

```text
vim-man/
├── src/vim_man/
│   ├── data/
│   │   ├── maze1.txt         # Main level layout (nodes, paths, portals)
│   │   └── mazetest.txt      # Minimal maze used in testing
│   ├── main.py               # Game entry point and main loop
│   ├── constants.py          # Game-wide constants (screen size, colors, modes, direction vectors)
│   ├── utils.py              # Shared utilities: maze path resolution and file loading
│   ├── vector.py             # 2D vector math
│   ├── nodes.py              # Maze graph: node parsing, connection, and portal linking
│   ├── entity.py             # Base class for all moving entities (movement, targeting, rendering)
│   ├── pacman.py             # Player-controlled entity; handles keyboard input and pellet collision
│   ├── ghosts.py             # Ghost entity; Chase, Scatter, Freight, and Spawn mode logic
│   ├── modes.py              # Ghost mode state machine (MainMode + ModeController)
│   ├── pellets.py            # Pellet and PowerPellet entities + group management
│   ├── fruits.py             # Bonus fruit entity that appears temporarily
│   ├── level.py              # Maze loading and data management
│   ├── pauser.py             # Pause state management with timed pauses and callbacks
│   └── types.py              # Type aliases (MazeArray, TilePos, PixelCoord)
├── tests/
│   ├── test_vector.py        # Unit tests for Vector2D
│   └── test_level.py         # Unit tests for Maze loading
```

### Maze File Format

Mazes are plain text files where each character represents a tile.
The node parser uses this to build the navigation graph at startup.

| Symbol | Meaning                                      |
|--------|----------------------------------------------|
| `X`    | Wall                                         |
| `+`    | Node (junction) — also spawns a pellet       |
| `.`    | Path — spawns a pellet                       |
| `-`    | Horizontal path — no pellet                  |
| `\|`   | Vertical path — no pellet                    |
| `n`    | Node (junction) — no pellet                  |
| `p`    | Path — spawns a power pellet                 |
| `P`    | Node (junction) — spawns a power pellet      |
| `=`    | Ghost house door (passable for ghosts only)  |

---

## Development

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, [Pyrefly](https://github.com/facebook/pyrefly) for type checking,
and [Pytest](https://pytest.org/) for tests. All are managed via `uv`.

```bash
# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check
uv run pyrefly check .

# Test
uv run pytest
```

CI runs automatically on every push and pull request to `main` via GitHub Actions (see `.github/workflows/ci.yml`).

---

## Roadmap

### ✅ Completed

- [x] 2D vector math library (`Vector2D`)
- [x] Text-file-driven maze parsing into a node graph
- [x] Horizontal and vertical node connection (left/right/up/down neighbors)
- [x] Portal (warp tunnel) pairs
- [x] Base entity movement along the node graph with overshoot detection
- [x] Vim-motion player controls
- [x] Pellet and power pellet rendering with flashing effect
- [x] Pellet consumption and tracking
- [x] Ghosts with their own individual targeting personalities (**Scatter**, **Chase**, **Freight**, and **Spawn** modes)
- [x] Power pellet triggering Ghost Freight mode; eating ghost in Freight triggers Spawn
- [x] Merging Ghost home into node graph
- [x] Proper Pacman and Ghost start positions
- [x] Ghost–Pacman collision detection
- [x] Lives system — death animation, life counter, and game-over state
- [x] Win condition — detect when all pellets are eaten and advance to the next level
- [x] Pause and restart — keyboard shortcuts for pausing and resetting the game
- [x] Scoring system — points display, pellet scoring (10pts), power pellet scoring (50pts),
ghost scoring (200/400/800/1600pts chain)

### 🚧 In Progress / Planned

- [ ] **Sprite rendering** — replace placeholder circles with proper Pac-Man and ghost sprites,
  including directional and death animations
- [ ] **Sound effects** — chomp, power pellet, ghost eaten, death, intro music
- [ ] **HUD** — score display, high score, remaining lives, and level indicator
- [ ] **Multiple levels** — level progression with increasing ghost speed and shorter Freight windows
- [ ] **Main menu / title screen**
- [ ] **Packaged binary** — distribute as a standalone executable via `pyproject.toml` entry point (`vim-man`)
- [ ] **Expanded test coverage** — unit tests for node graph construction, entity movement, ghost mode transitions,
  and pellet collision

---

TODO: initialize all class attributes inside the init

## License

MIT
