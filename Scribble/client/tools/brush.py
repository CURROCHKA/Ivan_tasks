from math import hypot
import pygame

from Scribble.client.tools.tool import Tool


class Brush(Tool):
    def __init__(
        self,
        win: pygame.surface.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        thickness: int = 1,
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
            image=pygame.image.load("../images/brush.png"),
            **kwargs
        )
        self.thickness = thickness
        self.mouse_down = False
        self.last_pos = None

    def on_click(self) -> None:
        self.game.set_tool(self)
        self.inactiveColour = self.pressedColour

    def listen(self, events: list[pygame.event.Event]) -> None:
        super().listen(events)
        if self.game.tool is self:
            for event in events:
                try:
                    pos = event.pos
                except AttributeError:
                    continue

                if not self.game.board.contains(*pos):
                    self.mouse_down = False
                    self.last_pos = None
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down_handler()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_up_handler()
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_motion_handler(pos)

    def mouse_down_handler(self) -> None:
        self.mouse_down = True
        self.game.board.push_to_undo(self.game.board.surface.copy())

    def mouse_up_handler(self) -> None:
        self.mouse_down = False
        self.last_pos = None

    def mouse_motion_handler(self, pos: tuple[int, int]) -> None:
        if self.mouse_down:
            self.draw_to_board(*pos)

    @staticmethod
    def interpolate_points(point1, point2) -> list[tuple[float, float]]:
        x1, y1 = point1
        x2, y2 = point2
        distance = int(hypot(x2 - x1, y2 - y1))
        points = [
            (x1 + i * (x2 - x1) / distance, y1 + i * (y2 - y1) / distance)
            for i in range(distance)
        ]
        return points

    def draw_to_board(self, x: float, y: float) -> None:
        x -= self.game.board.x
        y -= self.game.board.y

        if self.last_pos:
            for px, py in self.interpolate_points(self.last_pos, (x, y)):
                for i in range(self.thickness):
                    for j in range(self.thickness):
                        self.game.board.surface.set_at(
                            (int(px) + i, int(py) + j), self.game.drawing_color
                        )

        self.last_pos = (x, y)
