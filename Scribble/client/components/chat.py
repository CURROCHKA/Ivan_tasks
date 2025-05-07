import pygame

from pygame_widgets.textbox import TextBox

from Scribble.client.constants import (
    CHAT_COLOR,
    BORDER_COLOR,
    FONT_NAME,
    CHAT_TEXT_COLOR,
    BORDER_THICKNESS,
)


class Chat:
    def __init__(
        self,
        win: pygame.surface.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        textbox_height: int,
    ):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.textbox_height = textbox_height
        self.font_size = self.get_font_size()
        self.font = pygame.font.SysFont(FONT_NAME, self.font_size)
        self.text_offset = self.font_size // 3
        self.scroll_offset = 0
        self.actual_width = self.width - self.text_offset * 2 - BORDER_THICKNESS * 2
        self.textbox = TextBox(
            self.win,
            self.x,
            self.y + self.height - self.textbox_height,
            self.width,
            self.textbox_height,
            placeholderText="Напишите что-нибудь",
            fontSize=self.font_size,
            borderThickness=1,
            onSubmit=self.add_content,
            font=self.font,
            textColour=CHAT_TEXT_COLOR,
        )

        self.surface = pygame.surface.Surface(
            (self.width, self.height - self.textbox_height)
        )
        self.content = []

    def listen(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_offset += event.y * self.font_size
                # self.scroll_offset = max(min(self.scroll_offset, 0), self.height - self.textbox_height)
                # self.surface.scroll(dy=event.y)

    def get_font_size(self):
        text = "Напишите что-нибудь"
        font_size = self.width // 2
        width = pygame.font.SysFont(FONT_NAME, font_size).size(text)[0]
        text_offset_left = font_size // 3
        while width + text_offset_left > self.width:
            font_size -= 1
            width = pygame.font.SysFont(FONT_NAME, font_size).size(text)[0]
        return font_size

    def add_content(self):
        self.content.append(self.textbox.getText().strip())
        self.textbox.setText("")

    def draw(self):
        self.win.blit(self.surface, (self.x, self.y))
        self.surface.fill(CHAT_COLOR)
        pygame.draw.rect(
            self.surface,
            BORDER_COLOR,
            (0, 0, self.width, self.height - self.textbox_height),
            width=BORDER_THICKNESS,
        )

        shift = 0
        for i, msg in enumerate(self.content):
            x = [self.text_offset]
            for char in msg:
                if x[-1] >= self.actual_width or char == "\n":
                    shift += 1
                    x = [self.text_offset]
                    if char == "\n":
                        continue
                char_render = self.font.render(char, True, CHAT_TEXT_COLOR)
                char_rect = char_render.get_rect(
                    bottomleft=(
                        x[-1],
                        self.text_offset
                        + self.font_size * (i + 1 + shift)
                        + self.scroll_offset,
                    )
                )
                self.surface.blit(char_render, char_rect)
                x.append(x[-1] + char_render.get_width())
