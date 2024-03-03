import pygame


class Fruit:
    def __init__(self, coord: tuple, size: tuple, color: str = 'red'):
        self.x, self.y = coord
        self.size = size
        self.color = color

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, [(self.x, self.y), self.size])