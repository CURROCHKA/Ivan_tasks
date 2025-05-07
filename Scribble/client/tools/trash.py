import pygame

from Scribble.client.tools.tool import Tool


class Trash(Tool):
    def __init__(
        self,
        win: pygame.surface.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        **kwargs
    ) -> None:
        super().__init__(
            win,
            x,
            y,
            width,
            height,
            tag="brush",
            onClick=self.on_click,
            image=pygame.image.load("../images/trash.png"),
            **kwargs
        )

    def on_click(self) -> None:
        self.game.board.clear()
