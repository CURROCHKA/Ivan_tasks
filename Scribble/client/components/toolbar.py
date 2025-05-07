import pygame

from Scribble.client.constants import (
    TOOLBAR_COLOR,
    TOOL_SIZE,
    BORDER_THICKNESS,
    BORDER_COLOR,
)

from Scribble.client.tools.brush import Brush
from Scribble.client.tools.eraser import Eraser
from Scribble.client.tools.trash import Trash
from Scribble.client.tools.undo import Undo
from Scribble.client.tools.redo import Redo


class Toolbar:
    def __init__(
        self, win: pygame.surface.Surface, x: int, y: int, width: int, height: int, game
    ) -> None:
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.game = game
        self.tool_width = self.tool_height = round(self.height * TOOL_SIZE)
        self.tools = [
            Brush(
                self.win,
                self.x + self.tool_width // 2,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            ),
            Eraser(
                self.win,
                self.x + self.tool_width * 2,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            ),
            Trash(
                self.win,
                self.x + 7 * self.tool_width // 2,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            ),
            Undo(
                self.win,
                self.x + self.width - self.tool_width * 3,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            ),
            Redo(
                self.win,
                self.x + self.width - self.tool_width - self.tool_width // 2,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            ),
        ]

    def draw(self) -> None:
        pygame.draw.rect(
            self.win, TOOLBAR_COLOR, (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            self.win,
            BORDER_COLOR,
            (self.x, self.y, self.width, self.height),
            width=BORDER_THICKNESS,
        )
