import sys
from typing import Any

import pygame
import pygame_widgets
from pygame_widgets.textbox import TextBox

from network import Network
from game import Game
from player import Player
from config import (
    Window,
    WINDOW_SIZE,
    COLORS,
    FRAME,
    FONT_NAME,
    MAIN_MENU_FONT_SIZE,
    render_text,
)

# for test
WINDOW_SIZE = (1360, 768)
# WINDOW_SIZE = (1920, 1080)
# WINDOW_SIZE = (1300, 1000)
# WINDOW_SIZE = (1366, 768)
# WINDOW_SIZE = (1280, 1024)


class MainMenu(Window):
    def __init__(self):
        super().__init__(WINDOW_SIZE[0], WINDOW_SIZE[1], caption='Scribble', frame=FRAME)
        self.network = None

        self.text_box = TextBox(self.win,
                                **self.__set_text_box(),
                                onSubmit=self.text_box_submit)

        self.title_render = render_text('Scribble', max_width=int(self.width / 3), max_height=self.height)

        self.enter_render = render_text('Нажмите ВВОД, чтобы присоединиться к игре...',
                                        max_width=self.title_render.get_width() * 3,
                                        max_height=self.title_render.get_height())

        self.waiting = False
        self.is_existing_nickname = False

    def __set_text_box(self) -> dict[str, Any]:
        width = self.width / 3
        height = self.height / 10
        x = self.width / 2 - width / 2
        y = self.height / 2 - height / 2
        text = 'Введите свой никнейм'
        font_size = int(self.width * MAIN_MENU_FONT_SIZE)
        font = pygame.font.SysFont(FONT_NAME, font_size)
        args = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'fontSize': font_size,
            'font': font,
            'placeholderText': text
        }
        return args

    def text_box_submit(self):
        name = self.text_box.getText()
        if len(name) >= 1:
            self.network = Network(name)

            connection_response = self.network.connection_response

            if connection_response == -1:
                self.is_existing_nickname = True
            if connection_response == 1:
                self.is_existing_nickname = False
                self.waiting = True
                self.text_box.hide()
                self.text_box.disable()

    def draw(self, events: list[pygame.event.Event]):
        self.clock.tick(self.frame)
        self.win.fill(COLORS[0])

        self.win.blit(self.title_render, (self.width / 2 - self.title_render.get_width() / 2, 0))

        title_width = self.title_render.get_width()
        title_height = y = self.title_render.get_height()
        if self.waiting:
            self.enter_render = render_text('В очереди', title_width, title_height)
            y = self.height / 2 - self.enter_render.get_height() / 2

        elif self.is_existing_nickname:
            self.enter_render = render_text('Этот никнейм уже занят', title_width * 2, title_height)

        else:
            self.enter_render = render_text('Нажмите ВВОД, чтобы присоединиться к игре...',
                                            self.width, title_height)

        self.win.blit(self.enter_render, (self.width / 2 - self.enter_render.get_width() / 2, y))

        pygame_widgets.update(events)
        pygame.display.flip()

    def check_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            events = pygame.event.get()
            if self.waiting:
                response = self.network.send({-1: []})
                if response:
                    game = Game(self.network)
                    for player_name in response:
                        player = Player(player_name)
                        game.add_player(player)
                    game.run()
                    break
            self.check_events(events)
            self.draw(events)


if __name__ == '__main__':
    pygame.init()
    main = MainMenu()
    main.run()
