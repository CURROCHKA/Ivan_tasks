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
        thickness: int = 10,
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

        self.cursor = None

    def on_click(self) -> None:
        self.game.set_tool(self)
        self.inactiveColour = self.pressedColour

    def listen(self, events: list[pygame.event.Event]) -> None:
        super().listen(events)
        if not self.selected:
            return

        for event in events:
            try:
                pos = event.pos
            except AttributeError:
                continue

            if not self.game.board.contains(*pos):
                self.mouse_down = False
                self.last_pos = None
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                break

            if self.game.toolbar.tools["thickness_selector"].selector.contains(*pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                break

            if self.cursor is None or self.thickness != self.game.toolbar.tools["thickness_selector"].selector.getValue():
                self.thickness = self.game.toolbar.tools["thickness_selector"].selector.getValue()
                self.cursor = self.create_cursor()
            pygame.mouse.set_cursor(self.cursor)

            self.mouse_down = pygame.mouse.get_pressed()[0]

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down_handler(pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up_handler()
            elif event.type == pygame.MOUSEMOTION and self.game.toolbar.tools["thickness_selector"].selector._hidden:
                self.mouse_motion_handler(pos)

    def create_cursor(self):
        radius = self.thickness
        diameter = self.thickness * 2 + 1
        cursor_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

        pygame.draw.circle(
            cursor_surface,
            self.game.drawing_color,
            (radius, radius),
            radius,
        )

        return pygame.cursors.Cursor((radius, radius), cursor_surface)

    def mouse_down_handler(self, pos: tuple[int, int]) -> None:
        if not self.game.toolbar.tools["thickness_selector"].selector._hidden:
            self.game.toolbar.tools["thickness_selector"].selector.hide()

        x, y = pos
        x -= self.game.board.x
        y -= self.game.board.y

        self.game.board.push_to_undo(self.game.board.surface.copy())

        for i in range(-self.thickness + 1, self.thickness):
            for j in range(-self.thickness + 1, self.thickness):
                if i**2 + j**2 <= self.thickness**2:
                    self.game.board.surface.set_at(
                        (int(x) + i, int(y) + j), self.game.drawing_color
                    )

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
                for i in range(-self.thickness + 1, self.thickness):
                    for j in range(-self.thickness + 1, self.thickness):
                        if i**2 + j**2 <= self.thickness**2:
                            self.game.board.surface.set_at(
                                (int(px) + i, int(py) + j), self.game.drawing_color
                            )

        self.last_pos = (x, y)
