import pygame

from Scribble.client.constants import (
    LEADERBOARD_COLOR,
    BORDER_COLOR,
    BACKGROUND_COLOR,
    BORDER_THICKNESS,
)


class LeaderBoard:
    def __init__(
        self, win: pygame.surface.Surface, x: int, y: int, width: int, height: int
    ):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height  # Высота одной строчки
        self.players = [1, 2, 3, 4, 5, 6, 7, 8]

    def draw(self):
        for i in range(len(self.players)):
            if i % 2 == 0:
                color = LEADERBOARD_COLOR
            else:
                color = BACKGROUND_COLOR
            pygame.draw.rect(
                self.win,
                color,
                (self.x, self.y + self.height * i, self.width, self.height),
            )
        pygame.draw.rect(
            self.win,
            BORDER_COLOR,
            (self.x, self.y, self.width, self.height * len(self.players)),
            width=BORDER_THICKNESS,
        )
