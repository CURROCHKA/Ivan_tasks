from enum import Enum

import pygame


class Color(Enum):
    WHITE = {0: (255, 255, 255)}
    RED = {1: (255, 0, 0)}
    GREEN = {2: (0, 255, 0)}
    BLUE = {3: (0, 0, 255)}
    YELLOW = {4: (255, 255, 0)}
    PINK = {5: (255, 0, 255)}
    BROWN = {6: (150, 75, 0)}
    BLACK = {7: (0, 0, 0)}
    GRAY = {8: (200, 200, 200)}


FRAME = 120
WINDOW_SIZE = (0, 0)
COLS, ROWS = (160, 90)
FONT_NAME = 'consolas'

# as a percentage
MARGIN = 0.78125
PIXEL_SIZE_X = 0.121293
PIXEL_SIZE_Y = 0.18480
MAIN_MENU_FONT_SIZE = 0.02734375
CHAT_FONT_SIZE = 0.01484375

BORDER_THICKNESS = 2.5
BOARD_WIDTH = 1.6
BOTTOM_BAR_WIDTH = 2.5
SKIP_FONT_SIZE = 2.5

PLAYERS = 1
MAX_PLAYERS = 8
COLORS = {list(color.value.keys())[0]: list(color.value.values())[0] for color in Color}


class Window:
    def __init__(self, width: int, height: int,
                 background_color: tuple[int, int, int] = COLORS[0],
                 fullscreen: bool = False,
                 caption: str = 'Window',
                 frame: int = FRAME):
        self.width = width
        self.height = height

        if fullscreen:
            self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.win.get_size()
        else:
            self.win = pygame.display.set_mode((self.width, self.height))

        self.BG_color = background_color
        self.frame = frame
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(caption)

    def check_events(self, events: list[pygame.event.Event]):
        pass

    def draw(self, events: list[pygame.event.Event]):
        pass

    def run(self):
        pass


def get_font_size(text: str, max_width: int, max_height: int) -> int:
    min_font_size = 1
    max_font_size = 100  # Ограничиваем максимальный размер шрифта
    optimal_font_size = min_font_size

    while min_font_size <= max_font_size:
        font_size = (min_font_size + max_font_size) // 2
        font = pygame.font.SysFont(FONT_NAME, font_size)
        text_width, text_height = font.size(text)

        if text_width <= max_width and text_height <= max_height:
            # Текущий размер подходит, пробуем увеличить
            optimal_font_size = font_size
            min_font_size = font_size + 1
        else:
            # Текущий размер слишком велик, уменьшаем
            max_font_size = font_size - 1

    return optimal_font_size


def render_text(text: str, max_width: int = 0, max_height: int = 0, font_size: int = 0, color: tuple[int, int, int] = COLORS[7]) -> pygame.Surface:
    if font_size == 0:
        font_size = get_font_size(text, max_width, max_height)
    font = pygame.font.SysFont(FONT_NAME, font_size)
    render = font.render(text, 1, color)
    return render
