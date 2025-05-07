import pygame

from Scribble.client.tools.tool import Tool


class Redo(Tool):
    def __init__(self,
                 win: pygame.surface.Surface,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 **kwargs) -> None:
        super().__init__(win,
                         x,
                         y,
                         width,
                         height,
                         tag="redo",
                         image=pygame.image.load("../images/redo.png"),
                         onClick=self.on_click,
                         **kwargs)

    def on_click(self) -> None:
        self.game.board.redo()
