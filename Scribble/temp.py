import pygame


def create_brush_cursor(radius=10, color=(255, 255, 255)):
    """Создает круглый курсор для кисти с заданным радиусом."""
    diameter = radius * 2 + 1  # +1 чтобы был четкий центр
    cursor_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
    # cursor_surface.fill((255, 255, 255))

    pygame.draw.circle(
        cursor_surface,
        color,
        (radius, radius),  # Центр
        radius,
    )

    # Создаем курсор из поверхности (hotspot в центре)
    return pygame.cursors.Cursor((radius, radius), cursor_surface)


# Пример использования:
# brush_cursor = create_brush_cursor(radius=10)  # Курсор с радиусом 10
# pygame.mouse.set_cursor(brush_cursor)


if __name__ == "__main__":
    import sys

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    brush_cursor = create_brush_cursor(radius=10)
    pygame.mouse.set_cursor(brush_cursor)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
