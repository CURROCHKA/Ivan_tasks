import pygame

from config import (
    COLORS,
    BORDER_THICKNESS,
    render_text,
)


class TopBar:
    def __init__(self, win: pygame.Surface, x: float, y: float, width: int, height: int, margin: float, game):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = margin
        self.game = game
        self.border_thickness = int(self.margin / BORDER_THICKNESS)

        self.round = 0
        self.max_round = self.round
        self.word = ''
        self.time = 75

        self.font_size = int(self.height / 2)
        self.round_render = render_text(f'Раунд {self.round} из {self.max_round}', font_size=self.font_size)
        self.word_render = render_text(self.word, font_size=self.font_size)
        self.timer_render = render_text(str(self.time), font_size=self.font_size)

    def draw(self):
        # draw round
        self.win.blit(self.round_render,
                      (self.x + self.margin, self.y + self.height / 2 - self.round_render.get_height() / 2))

        self.win.blit(self.word_render, (self.x + self.width / 2 - self.word_render.get_width() / 2,
                                         self.y + self.height / 2 - self.word_render.get_height() / 2 + self.margin))

        pygame.draw.rect(self.win, COLORS[7], (self.x - self.border_thickness / 2,
                                               self.y - self.border_thickness / 2,
                                               self.width + self.border_thickness,
                                               self.height + self.border_thickness),
                         self.border_thickness)

        radius = self.height / 2
        pygame.draw.circle(self.win, COLORS[7], (int(self.x + self.width - radius),
                                                 int(self.y + self.height / 2)), radius, self.border_thickness)

        self.win.blit(self.timer_render, (self.x + self.width - self.timer_render.get_width() / 2 - radius,
                                          self.y + self.height / 2 - self.timer_render.get_height() / 2))

    @staticmethod
    def underscore_text(text: str):
        new_text = ''

        for char in text:
            if char != ' ':
                new_text += ' _ '
            else:
                new_text += '   '
        return new_text

    def update_time(self, time: int):
        self.time = time
        self.timer_render = render_text(str(time), font_size=self.font_size)

    def update_word(self, word: str):
        self.word = word
        if self.game.drawing:
            wrd = word
        else:
            wrd = self.underscore_text(word)

        self.word_render = render_text(wrd, font_size=self.font_size)

    def update_round(self, rnd: int):
        self.round = rnd
        self.round_render = render_text(f'Раунд {self.round} из {self.max_round}', font_size=self.font_size)

    def update_max_round(self, max_round: int):
        self.max_round = max_round
        self.round_render = render_text(f'Раунд {self.round} из {self.max_round}', font_size=self.font_size)
