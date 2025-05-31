import pygame

from math import hypot

from Scribble.client.tools.tool import Tool
from Scribble.client.constants import (
    BOARD_COLOR,
    BORDER_COLOR,
    BORDER_THICKNESS,
)


class Eraser(Tool):
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
            tag="eraser",
            onClick=self.on_click,
            image=pygame.image.load("../images/eraser.png"),
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

            if self.cursor is None:
                self.cursor = self.create_cursor()
            pygame.mouse.set_cursor(self.cursor)

            self.mouse_down = pygame.mouse.get_pressed()[0]

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down_handler()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up_handler(pos)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_motion_handler(pos)

    def set_thickness(self, thickness):
        self.thickness = thickness
        self.cursor = self.create_cursor()

    def create_cursor(self):
        size = self.thickness
        cursor_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        cursor_surface.fill(BOARD_COLOR)

        pygame.draw.rect(
            cursor_surface,
            BORDER_COLOR,
            (0, 0, size, size),
            width=BORDER_THICKNESS,
        )

        return pygame.cursors.Cursor((size // 2, size // 2), cursor_surface)

    def mouse_down_handler(self) -> None:
        self.mouse_down = True

    def mouse_up_handler(self, pos: tuple[int, int]) -> None:
        x, y = pos
        x -= self.game.board.x
        y -= self.game.board.y
        self.mouse_down = False
        self.last_pos = None
        pygame.draw.rect(
            self.game.board.surface,
            BOARD_COLOR,
            (
                int(x) - self.thickness // 2,
                int(y) - self.thickness // 2,
                self.thickness,
                self.thickness,
            ),
            width=BORDER_THICKNESS,
        )

    def mouse_motion_handler(self, pos: tuple[int, int]) -> None:
        if self.mouse_down:
            self.erase_from_board(*pos)

    @staticmethod
    def interpolate_points(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        distance = int(hypot(x2 - x1, y2 - y1))
        points = [
            (x1 + i * (x2 - x1) / distance, y1 + i * (y2 - y1) / distance)
            for i in range(distance)
        ]
        return points

    def erase_from_board(self, x: int, y: int) -> None:
        x -= self.game.board.x
        y -= self.game.board.y

        if self.last_pos:
            for px, py in self.interpolate_points(self.last_pos, (x, y)):
                for i in range(self.thickness):
                    for j in range(self.thickness):
                        self.game.board.surface.set_at(
                            (
                                int(px) + i - self.thickness // 2,
                                int(py) + j - self.thickness // 2,
                            ),
                            BOARD_COLOR,
                        )

        self.last_pos = (x, y)

        # pygame.draw.rect(
        #     self.game.board.surface,
        #     BOARD_COLOR,
        #     (
        #         int(x) - self.thickness // 2,
        #         int(y) - self.thickness // 2,
        #         self.thickness,
        #         self.thickness,
        #     ),
        # )
        # pygame.draw.rect(
        #     self.game.board.surface,
        #     BORDER_COLOR,
        #     (
        #         int(x) - self.thickness // 2,
        #         int(y) - self.thickness // 2,
        #         self.thickness,
        #         self.thickness,
        #     ),
        #     width=BORDER_THICKNESS,
        # )
