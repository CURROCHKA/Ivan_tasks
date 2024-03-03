import sys
import pygame
from random import randrange
from snake import Snake
from fruit import Fruit


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_size = self.screen.get_size()
        self.cell_size = (25, 25)
        self.snake = Snake(self.screen_rect)
        self.fruit = Fruit(self.create_fruit_coord(), self.cell_size)
        self.clock = pygame.time.Clock()
        self.frame = 5
        pygame.display.set_caption('Snake')

    def run(self):
        while True:
            self.check_events()
            self.snake.update()
            self.update_screen()

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

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)

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

        if key in directions and self.snake.speed != 0:
            dx, dy = directions[key]
            if (dx, dy) != (-self.snake.moving_x, -self.snake.moving_y):
                self.snake.moving_x, self.snake.moving_y = dx, dy

    def update_screen(self):
        self.screen.fill('gray')
        self.snake.draw(self.screen)
        self.fruit.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.frame)


if __name__ == '__main__':
    snake_game = Game()
    snake_game.run()
