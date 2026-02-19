from vim_man.constants import YELLOW
from vim_man.constants import TILEWIDTH
from vim_man.constants import WHITE
from vim_man.constants import TILEHEIGHT
from pygame import Surface
from pygame.font import Font
import pygame
from vim_man.vector import Vector2D
from vim_man.constants import Color, TextID


class Text:
    def __init__(
        self,
        text: str,
        color: Color,
        x: float,
        y: float,
        size: int,
        lifespan: float | None = None,
        id: int | None = None,
        visible: bool = True,
    ) -> None:
        self.text = text
        self.color = color
        self.size = size
        self.lifespan = lifespan
        self.id = id
        self.visible = visible

        self.position = Vector2D(x, y)
        self.timer = 0.0
        self.destroy = False

        self.font: Font
        self.label: Surface

        self.setup_font("PressStart2P-Regular.ttf")
        self.create_label()

    def setup_font(self, font_path: str) -> None:
        self.font = pygame.font.Font(font_path, self.size)

    def create_label(self) -> None:
        self.label = self.font.render(self.text, 1, self.color)

    def set_text(self, new_text: str) -> None:
        self.text = new_text
        self.create_label()

    def update(self, dt: float) -> None:
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0.0
                self.lifespan = None
                self.destroy = True

    def render(self, screen: Surface) -> None:
        if self.visible:
            x, y = self.position.as_int()
            screen.blit(self.label, (x, y))


class TextGroup:
    def __init__(self) -> None:
        self.next_id = 10
        self.all_text: dict[int, Text] = {}
        self.setup_text()
        self.show_text(TextID.READYTEXT)

    def add_text(
        self,
        text: str,
        color: Color,
        x: float,
        y: float,
        size: int,
        lifespan: float | None = None,
        id: int | None = None,
    ) -> int:
        self.next_id += 1
        self.all_text[self.next_id] = Text(text, color, x, y, size, lifespan, id)
        return self.next_id

    def remove_text(self, id: int) -> None:
        self.all_text.pop(id)

    def setup_text(self) -> None:
        size = TILEHEIGHT
        self.all_text[TextID.SCORETEXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, size)
        self.all_text[TextID.LEVELTEXT] = Text("1".zfill(3), WHITE, 23 * TILEWIDTH, TILEHEIGHT, size)
        self.all_text[TextID.READYTEXT] = Text("READY!", YELLOW, 11.25 * TILEWIDTH, 20 * TILEHEIGHT, size)
        self.all_text[TextID.PAUSETEXT] = Text("PAUSED!", YELLOW, 10.625 * TILEWIDTH, 20 * TILEHEIGHT, size)
        self.all_text[TextID.GAMEOVERTEXT] = Text("GAMEOVER!", YELLOW, 10 * TILEWIDTH, 20 * TILEHEIGHT, size)
        self.add_text("SCORE", WHITE, 0, 0, size)
        self.add_text("LEVEL", WHITE, 23 * TILEWIDTH, 0, size)

    def update(self, dt: float) -> None:
        for key, text in self.all_text.items():
            text.update(dt)
            if text.destroy:
                self.remove_text(key)

    def show_text(self, id: int) -> None:
        self.hide_text()
        self.all_text[id].visible = True

    def hide_text(self) -> None:
        for id in (TextID.READYTEXT, TextID.PAUSETEXT, TextID.GAMEOVERTEXT):
            self.all_text[id].visible = True

    def update_score(self, score: int) -> None:
        self.update_text(TextID.SCORETEXT, str(score).zfill(8))

    def update_level(self, level: int) -> None:
        self.update_text(TextID.LEVELTEXT, str(level + 1).zfill(3))

    def update_text(self, id: int, value: str) -> None:
        if id in self.all_text.keys():
            self.all_text[id].set_text(value)

    def render(self, screen: Surface) -> None:
        for text in self.all_text.values():
            text.render(screen)
