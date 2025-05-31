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
from Scribble.client.tools.thickness_selector import ThicknessSelector


class Toolbar:
    def __init__(
            self, win: pygame.surface.Surface, x: int, y: int, width: int, height: int
    ) -> None:
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tool_width = self.tool_height = round(self.height * TOOL_SIZE)
        self.tools = {
            "brush": Brush(
                self.win,
                self.x + self.tool_width // 2,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            ),
            "eraser": Eraser(
                self.win,
                self.x + self.tool_width * 2,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            ),
            "trash": Trash(
                self.win,
                self.x + 7 * self.tool_width // 2,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            ),
            "undo": Undo(
                self.win,
                self.x + self.width - self.tool_width * 3,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            ),
            "redo": Redo(
                self.win,
                self.x + self.width - self.tool_width - self.tool_width // 2,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            ),
            "thickness_selector": ThicknessSelector(
                self.win,
                self.x
                + self.width
                - self.tool_width * 4
                - self.tool_width // 2,
                self.y + (self.height - self.tool_height) // 2,
                self.tool_width,
                self.tool_height,
                colour=TOOLBAR_COLOR,
            )
        }
        # self.tools["thickness_selector"].hide()

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
