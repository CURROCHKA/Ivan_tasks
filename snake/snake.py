import pygame
from collections import deque


class Snake:
    def __init__(self, coord: tuple, size: tuple, color: tuple = (0, 255, 0)):
        self.x, self.y = coord
        self.size = size
        self.color = color
        self.snake_list = [(self.x, self.y)]
        self.moving_x, self.moving_y = 0, 0
        self.speed = 1
        self.len = 1
        self.direction_buffer = deque(maxlen=2)  # Буфер направлений движения змейки
        # (можно "запомнить" максимум 2 хода змейки)

    def update(self, screen_rect: pygame.Rect):
        if self.direction_buffer:
            if self.len == 1:  # Если у змейки длина 1 - она может двигаться в любых направлениях
                self.moving_x, self.moving_y = self.direction_buffer.popleft()
            elif (self.direction_buffer[0][0], self.direction_buffer[0][1]) != (-self.moving_x, -self.moving_y):
                # Проверка на совпадение первого направления в буфере с противоположным направлением змейки для того,
                # чтобы не было поворота на 180 градусов (чтобы змейка не пошла в себя)
                self.moving_x, self.moving_y = self.direction_buffer.popleft()
            else:
                self.direction_buffer.popleft()
        self.x += self.size[0] * self.moving_x * self.speed
        self.y += self.size[1] * self.moving_y * self.speed

        if self.x >= screen_rect.right:
            self.x = 0
        if self.x < 0:
            self.x = int(screen_rect.right - screen_rect.right % self.size[0])
        if self.y < 0:
            self.y = int(screen_rect.bottom - screen_rect.bottom % self.size[1])
        if self.y >= screen_rect.bottom:
            self.y = 0

        # ОБНОВЛЕНИЕ snake_list путем добавления ячейки змеи в список и удаление, если фактическая длина змеи меньше
        if self.speed == 1:
            self.snake_list.append((self.x, self.y))
        if len(self.snake_list) > self.len:
            del self.snake_list[0]

    def check_collisions(self):
        return self.len >= 2 and self.snake_list[0] in self.snake_list[1:]

    def draw(self, surface: pygame.Surface):
        for cell in self.snake_list:
            pygame.draw.rect(surface, self.color, [cell[0], cell[1], self.size[0], self.size[1]])
