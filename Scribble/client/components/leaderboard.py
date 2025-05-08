import pygame

from Scribble.client.player.player import Player
from Scribble.client.constants import (
    LEADERBOARD_COLOR,
    BORDER_COLOR,
    BACKGROUND_COLOR,
    BORDER_THICKNESS,
    LEADERBOARD_NAME_COLOR,
    LEADERBOARD_SCORE_COLOR,
    FONT_NAME,
)


class LeaderBoard:
    def __init__(
        self, win: pygame.surface.Surface, x: int, y: int, width: int, height_line: int
    ):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height_line  # One line height

        # Name font
        self.name_font_size = self.height // 4
        self.name_font = pygame.font.SysFont(FONT_NAME, self.name_font_size)
        self.name_offset = self.width // 3

        # Score font
        self.score_font_size = self.height // 4
        self.score_font = pygame.font.SysFont(FONT_NAME, self.score_font_size)
        self.score_offset = self.width // 3

        # Rank font
        self.rank_font_size = self.height // 3
        self.rank_font = pygame.font.SysFont(FONT_NAME, self.rank_font_size)
        self.rank_offset = self.rank_font_size // 3

        self.players = [
            Player("Ivan"),
            Player("Petr"),
            Player("Sergey"),
            Player("Ivan"),
            Player("Petr"),
            Player("Sergey"),
            Player("Ivan"),
            Player("Petr"),
        ]
        self.players[-1].add_score(100)

    def assign_ranks(self):
        self.players.sort(key=lambda player: player.get_score(), reverse=True)

    def draw_players(self):
        previous_score = 0
        rank = 1
        for i, player in enumerate(self.players):
            name = player.get_name()
            score = player.get_score()

            if score != previous_score:
                rank = str(i + 1)
                previous_score = score

            rank_render = self.rank_font.render(rank, 1, LEADERBOARD_NAME_COLOR)
            name_render = self.name_font.render(name, 1, LEADERBOARD_NAME_COLOR)
            score_render = self.score_font.render(
                f"{score} очков", 1, LEADERBOARD_SCORE_COLOR
            )

            self.win.blit(
                rank_render,
                (
                    self.x + self.rank_offset,
                    self.y
                    + self.height * i
                    + self.height // 2
                    - rank_render.get_height() // 2,
                ),
            )
            self.win.blit(
                name_render,
                (
                    self.x + self.name_offset,
                    self.y + self.height * i + name_render.get_height(),
                ),
            )
            self.win.blit(
                score_render,
                (
                    self.x + self.score_offset,
                    self.y + self.height * i + self.height / 2,
                ),
            )

    def draw(self):
        self.assign_ranks()  # Maybe need to call in another place
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

        self.draw_players()
