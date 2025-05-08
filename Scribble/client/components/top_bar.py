import pygame


from Scribble.client.constants import (
    TOP_BAR_COLOR,
    BORDER_COLOR,
    BORDER_THICKNESS,
    FONT_NAME,
    TOP_BAR_TEXT_COLOR,
)


class TopBar:
    def __init__(
        self,
        win: pygame.surface.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        game,
        current_round: int = 1,
        max_rounds: int = 3,
        time: int = 60,
        word: str = "",
    ) -> None:
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.round = current_round
        self.max_rounds = max_rounds
        self.time = time
        self.word = word
        self.game = game

        self.font = pygame.font.SysFont(FONT_NAME, self.height // 2)

    def update_word(self, word: str):
        self.word = word

    def update_time(self, time: int):
        self.time = time

    def update_round(self, value: int):
        self.round = value

    def draw(self) -> None:
        time_render = self.font.render(str(self.time), 1, BORDER_COLOR)
        round_render = self.font.render(
            f"Раунд {self.round} из {self.max_rounds}", 1, BORDER_COLOR
        )

        self.win.blit(
            time_render,
            (
                self.x + 5 * self.height // 6 - time_render.get_width() // 2,
                self.y + self.height // 2 - time_render.get_height() // 2,
            ),
        )
        self.win.blit(
            round_render,
            (self.x + 5 * self.height // 3, self.y + self.height // 2 - round_render.get_height() // 2),
        )

        pygame.draw.circle(
            self.win,
            BORDER_COLOR,
            (self.x + 5 * self.height // 6, self.y + self.height / 2),
            self.height // 2 - 2 * BORDER_THICKNESS,
            width=BORDER_THICKNESS,
        )

        if self.game.is_drawing:
            word_render = self.font.render(self.word, 1, TOP_BAR_TEXT_COLOR)
            self.win.blit(
                word_render,
                (
                    self.x + self.width // 2 - word_render.get_width() // 2,
                    self.y + self.height // 2 - word_render.get_height() // 2,
                ),
            )
        else:
            for i in range(len(self.word)):
                word_render = self.font.render("_", 1, TOP_BAR_TEXT_COLOR)
                self.win.blit(
                    word_render,
                    (
                        self.x
                        + self.width // 2
                        - (len(self.word) * 2 - 1) * word_render.get_width() // 2
                        + word_render.get_width() * i * 2,
                        self.y + self.height // 2 - word_render.get_height() // 2,
                    ),
                )

        pygame.draw.rect(
            self.win,
            BORDER_COLOR,
            (self.x, self.y, self.width, self.height),
            width=BORDER_THICKNESS,
        )
