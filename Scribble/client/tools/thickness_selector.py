import pygame

from pygame_widgets.slider import Slider

from Scribble.client.tools.tool import Tool


class ThicknessSelector(Tool):
    def __init__(self, win: pygame.surface.Surface, x: int, y: int, width: int, height: int, **kwargs) -> None:
        super().__init__(win, x, y, width, height, tag="selector", onClick=self.on_click, image=pygame.image.load("../images/line_weight.png"), **kwargs)
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selector = Slider(
            self.win,
            self.x,
            self.y - self.height * 12,
            self.height,
            self.height * 10,
            vertical=True,
            min=1,
            max=20,
            step=1,
            initial=1,
            valueColour=(200, 200, 200),
            handleRadius=self.height // 2,
        )
        self.selector.hide()

    def on_click(self) -> None:
        if self.selector._hidden:
            self.selector.show()
        else:
            self.selector.hide()
