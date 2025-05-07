import pygame


from Scribble.client.constants import (
    BOARD_COLOR,
    BORDER_COLOR,
    BORDER_THICKNESS,
    MAX_UNDO_STEPS,
)


class Board:
    def __init__(
        self, win: pygame.surface.Surface, x: int, y: int, width: int, height: int
    ) -> None:
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.surface.Surface((self.width, self.height))
        self.surface.fill(BOARD_COLOR)
        self.undo_list = []
        self.redo_list = []

    def push_to_undo(self, surface: pygame.surface.Surface) -> None:
        self.undo_list.append(surface)
        if len(self.undo_list) > MAX_UNDO_STEPS:
            del self.undo_list[0]

    def undo(self) -> None:
        print(self.undo_list.__sizeof__())
        if self.undo_list:
            self.redo_list.append(self.surface.copy())
            self.surface = self.undo_list.pop()

    def redo(self) -> None:
        if self.redo_list:
            self.undo_list.append(self.surface.copy())
            self.surface = self.redo_list.pop()

    def contains(self, x: int, y: int) -> bool:
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def draw(self) -> None:
        self.win.blit(self.surface, (self.x, self.y))
        pygame.draw.rect(
            self.surface,
            BORDER_COLOR,
            (0, 0, self.width, self.height),
            width=BORDER_THICKNESS,
        )

    def clear(self) -> None:
        self.push_to_undo(self.surface.copy())
        self.surface.fill(BOARD_COLOR)
