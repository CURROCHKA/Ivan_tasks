import sys
import pygame
import pygame_widgets

from Scribble.client.components.top_bar import TopBar
from Scribble.client.components.toolbar import Toolbar
from Scribble.client.tools.tool import Tool
from Scribble.client.components.board import Board
from Scribble.client.components.leaderboard import LeaderBoard
from Scribble.client.components.chat import Chat
from constants import (
    BACKGROUND_COLOR,
    TOP_BAR_HEIGHT,
    LEADERBOARD_WIDTH,
    MAX_PLAYERS,
)


class App:
    def __init__(self, width: int, height: int, fullscreen: bool = False) -> None:
        if fullscreen:
            self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.win.get_size()
        else:
            self.width, self.height = width, height
            self.win = pygame.display.set_mode((self.width, self.height))

        self.top_bar = TopBar(
            self.win,
            0,
            0,
            self.width,
            int(self.height * TOP_BAR_HEIGHT),
            self,
        )

        self.leaderboard = LeaderBoard(
            self.win,
            0,
            self.top_bar.y + 3 * self.top_bar.height // 2,
            int(self.width * LEADERBOARD_WIDTH),
            self.top_bar.height * 2,
        )

        self.board = Board(
            self.win,
            self.leaderboard.width,
            self.top_bar.y + 3 * self.top_bar.height // 2,
            self.width - self.leaderboard.width * 2,
            self.leaderboard.height * MAX_PLAYERS,
        )

        self.chat = Chat(
            self.win,
            self.board.x + self.board.width,
            self.top_bar.y + 3 * self.top_bar.height // 2,
            self.leaderboard.width,
            self.board.height,
            self.leaderboard.height,
        )

        self.toolbar = Toolbar(
            self.win,
            self.board.x,
            self.board.y + self.board.height,
            self.board.width,
            self.height - self.board.y - self.board.height,
        )

        self.drawing_color = (0, 0, 0)
        self.is_drawing = False

        self.tool = None
        for tool in self.toolbar.tools:
            tool.game = self

        pygame.display.set_icon(pygame.image.load("../images/icon.png"))
        pygame.display.set_caption("Scribble")

    def set_tool(self, tool: Tool) -> None:
        if self.tool:
            self.tool.inactiveColour = self.tool.old_colour
        self.tool = tool

    def run(self) -> None:
        while True:
            events = pygame.event.get()
            self.listen(events)
            self.chat.listen(events)
            self.draw(events)

    def listen(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self, events: list[pygame.event.Event]) -> None:
        self.win.fill(BACKGROUND_COLOR)
        self.top_bar.draw()
        self.toolbar.draw()
        self.leaderboard.draw()
        self.chat.draw()
        self.board.draw()

        pygame_widgets.update(events)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    app = App(800, 600, fullscreen=True)
    app.run()
