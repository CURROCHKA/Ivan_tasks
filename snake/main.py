import pygame
import pygame_widgets
from pygame_widgets.button import Button
from random import randrange
from snake import Snake
from fruit import Fruit


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_size = self.screen.get_size()
        self.font_size = int(self.screen_rect.w * 0.045)
        self.font_style = pygame.font.SysFont('consolas', self.font_size)
        self.cell_size = (round(self.screen_size[0] * 0.013), round(self.screen_size[1] * 0.0231))
        self.clock = pygame.time.Clock()
        self.frame = 5
        self.score = 0
        self.snake = Snake(self.create_snake_coord(), self.cell_size)
        self.fruit = Fruit(self.create_fruit_coord(), self.cell_size)
        self.play_button = Button(
            self.screen,
            self.screen_rect.centerx * 0.75,
            self.screen_rect.centery * 0.75,
            round(self.font_style.size('Продолжить')[0] * 1.15),
            round(self.font_style.size('Продолжить')[1] * 1.3),
            text='Продолжить',
            font=self.font_style,
            textColour=(255, 255, 255),
            colour=(255, 0, 0),
            radius=round(self.font_style.size('Продолжить')[0] * 0.5),
            borderThickness=5,
            borderColour=(255, 255, 255),
            onRelease=self.play,
        )
        self.quit_button = Button(
            self.screen,
            self.screen_rect.centerx * 0.875,
            self.screen_rect.centery * 1.1,
            round(self.font_style.size('Выход')[0] * 1.15),
            round(self.font_style.size('Выход')[1] * 1.3),
            text='Выход',
            font=self.font_style,
            textColour=(255, 255, 255),
            colour=(255, 0, 0),
            radius=round(self.font_style.size('Выход')[0] * 0.5),
            borderThickness=5,
            borderColour=(255, 255, 255),
            onRelease=self.quit,
        )
        pygame.display.set_caption('Snake')

    def run(self):
        while True:
            events = pygame.event.get()
            if self.snake.check_collisions():
                self.quit()
            self.check_events(events)
            self.snake.update(self.screen_rect)
            self.update_screen(events)

    def play(self):
        self.snake.speed = 1

    @staticmethod
    def quit():
        pygame.quit()
        quit()

    def create_snake_coord(self) -> tuple:
        x = int(self.screen_rect.centerx - self.screen_rect.centerx % self.cell_size[0])
        y = int(self.screen_rect.centery - self.screen_rect.centery % self.cell_size[1])
        return x, y

    def create_fruit_coord(self) -> tuple:
        space_x = int(self.screen_size[0] - self.screen_size[0] % self.cell_size[0])
        space_y = int(self.screen_size[1] - self.screen_size[1] % self.cell_size[1])

        def generate_coord():
            x = randrange(0, space_x, self.cell_size[0])
            y = randrange(0, space_y, self.cell_size[1])
            return x, y

        while True:
            coord = generate_coord()
            if coord not in self.snake.snake_list:
                return coord

    def check_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)

        self.check_fruit_consume()

    def check_fruit_consume(self):
        if (self.snake.x, self.snake.y) == (self.fruit.x, self.fruit.y):
            self.snake.len += 1
            self.score += 1
            self.fruit.x, self.fruit.y = self.create_fruit_coord()
            self.frame += 1 if self.frame <= 15 and self.score % 3 == 0 else 0  # Увеличение скорости игры

    def check_keydown_events(self, event: pygame.event):
        key = event.key
        directions = {
            pygame.K_w: (0, -1),
            pygame.K_UP: (0, -1),
            pygame.K_a: (-1, 0),
            pygame.K_LEFT: (-1, 0),
            pygame.K_s: (0, 1),
            pygame.K_DOWN: (0, 1),
            pygame.K_d: (1, 0),
            pygame.K_RIGHT: (1, 0)
        }

        if key == pygame.K_ESCAPE:
            self.snake.speed = 0 if self.snake.speed == 1 else 1
        if key in directions and self.snake.speed != 0:
            dx, dy = directions[key]
            self.snake.direction_buffer.append((dx, dy))

    def print_message(self, msg: str, color: str, pos: tuple):
        print_msg = self.font_style.render(msg, True, color)
        msg_rect = print_msg.get_rect()
        msg_rect.center = pos
        self.screen.blit(print_msg, msg_rect)

    def update_screen(self, events):
        self.screen.fill('gray')
        self.print_message(f'Score {self.score}', 'yellow', (self.screen_rect.centerx, self.screen_rect.h * 0.04))
        self.snake.draw(self.screen)
        self.fruit.draw(self.screen)
        if self.snake.speed != 0:
            self.clock.tick(self.frame)
        else:
            pygame_widgets.update(events)
        pygame.display.update()


if __name__ == '__main__':
    snake_game = Game()
    snake_game.run()
