import pygame

from pygame_widgets.button import Button


class Tool(Button):
    def __init__(
        self,
        win: pygame.surface.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        tag: str,
        **kwargs
    ) -> None:
        super().__init__(win, x, y, width, height, **kwargs)
        self.tag = tag
        self.selected = False
        if self.image:
            self.image = pygame.transform.scale(self.image, (self._width, self._height))
        self.old_colour = self.colour
        self.game = None

    def on_click(self) -> None:
        pass
