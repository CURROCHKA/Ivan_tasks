import pygame
from pygame_widgets.button import ButtonArray

from config import (
    COLORS,
    get_font_size,
)


class BottomBar:
    def __init__(self, win: pygame.Surface, x: int, y: int, width: int, height: int, margin: float, game):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = margin
        self.game = game
        self.color_buttons = ButtonArray(
            self.win,
            self.x,
            self.y,
            self.width,
            self.height,
            (4, 2),
            border=0,
            colour=COLORS[0],
            inactiveColours=list(COLORS.values())[1::],
            separationThickness=0,
            onClicks=[self.color_click] * 8
        )

        self.brush_img, self.brush_text, self.brush_color =\
            self.set_spec_button('images/brush.png', 'Кисточка')
        self.erase_img, self.erase_text, self.erase_color =\
            self.set_spec_button('images/eraser.png', 'Ластик')
        self.filling_img, self.filling_text, self.filling_color =\
            self.set_spec_button('images/filling.png', 'Заливка')
        self.trash_img, self.trash_text, self.trash_color =\
            self.set_spec_button('images/trash.png', 'Очистка')
        self.spec_buttons_font_sizes = tuple(get_font_size(text, self.width, self.height) for text in [self.brush_text, self.erase_text, self.filling_text, self.trash_text])

        self.spec_buttons = ButtonArray(
            self.win,
            self.color_buttons.getWidth() + self.color_buttons.getX() + self.margin,
            self.y,
            self.width,
            self.height,
            (4, 1),
            border=0,
            colour=COLORS[0],
            inactiveColours=(self.brush_color, self.erase_color, self.filling_color, self.trash_color),
            texts=(self.brush_text, self.erase_text, self.filling_text, self.trash_text),
            images=(self.brush_img, self.erase_img, self.filling_img, self.trash_img),
            onClicks=(self.brush_click, self.erase_click, self.filling_click, self.trash_click),
            fontSizes=self.spec_buttons_font_sizes,
        )

        self.brush_already_pressed = False
        self.erase_already_pressed = False
        self.filling_already_pressed = False
        self.old_draw_color = self.game.draw_color

        self.active_spec_button = 'brush'
        self.enable_brush()

    def set_spec_button(self, path_to_img: str = '', text: str = '') -> tuple[pygame.Surface, str, tuple[int, int, int]]:
        try:
            img = pygame.image.load(path_to_img).convert_alpha()
            img.set_colorkey(COLORS[0])
            img = pygame.transform.scale(img, (self.height, self.height))

            button_text = ''
            button_color = COLORS[0]
        except Exception as e:
            print(e)
            img = None
            button_text = text
            button_color = COLORS[8]
        return img, button_text, button_color

    def enable_brush(self):
        if self.active_spec_button == 'filling':
            self.disable_filling()
        elif self.active_spec_button == 'erase':
            self.disable_erase()

        self.active_spec_button = 'brush'
        self.brush_already_pressed = True
        self.spec_buttons.buttons[0].inactiveColour = self.spec_buttons.buttons[0].pressedColour

    def disable_brush(self):
        self.brush_already_pressed = False
        self.spec_buttons.buttons[0].inactiveColour = self.brush_color

    def brush_click(self):
        if not self.brush_already_pressed:
            self.enable_brush()

    def enable_erase(self):
        if self.active_spec_button == 'filling':
            self.disable_filling()
        elif self.active_spec_button == 'brush':
            self.disable_brush()

        self.active_spec_button = 'erase'
        self.old_draw_color = self.game.draw_color
        self.game.set_draw_color(COLORS[0])
        self.erase_already_pressed = True
        self.spec_buttons.buttons[1].inactiveColour = self.spec_buttons.buttons[1].pressedColour

    def disable_erase(self):
        self.erase_already_pressed = False
        self.spec_buttons.buttons[1].inactiveColour = self.erase_color
        self.game.set_draw_color(self.old_draw_color)

    def erase_click(self):
        if self.erase_already_pressed:
            self.enable_brush()
        else:
            self.enable_erase()

    def enable_filling(self):
        if self.active_spec_button == 'erase':
            self.disable_erase()
        elif self.active_spec_button == 'brush':
            self.disable_brush()

        self.active_spec_button = 'filling'
        self.game.board.filling = True
        self.filling_already_pressed = True
        self.spec_buttons.buttons[2].inactiveColour = self.spec_buttons.buttons[2].pressedColour
        self.game.connection.send({11: self.game.board.filling})

    def disable_filling(self):
        self.game.board.filling = False
        self.filling_already_pressed = False
        self.spec_buttons.buttons[2].inactiveColour = self.filling_color
        self.game.connection.send({11: self.game.board.filling})

    def filling_click(self):
        if self.filling_already_pressed:
            self.enable_brush()
        else:
            self.enable_filling()

    def trash_click(self):
        self.game.board.clear()
        self.game.connection.send({9: []})

    def color_click(self):
        for color_button in self.color_buttons.buttons:
            if color_button.clicked:
                self.game.set_draw_color(color_button.inactiveColour)

