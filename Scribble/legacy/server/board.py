from collections import deque

from config import (
    COLS,
    ROWS,
)


class Board:
    def __init__(self):
        self.grid = self.create_empty_board()
        self.filling = False

    @staticmethod
    def is_valid_coord(row: int, col: int):
        return 0 <= row < ROWS and 0 <= col < COLS

    def flood_fill(self, start_x: int, start_y: int, new_color: tuple[int, int, int] | int):
        original_color = self.grid[start_y][start_x]

        if original_color == new_color:
            return

        queue = deque([(start_x, start_y)])
        visited = {(start_x, start_y)}

        while queue:
            x, y = queue.popleft()
            self.grid[y][x] = new_color

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (
                        self.is_valid_coord(ny, nx) and
                        self.grid[ny][nx] == original_color and
                        (nx, ny) not in visited
                ):
                    queue.append((nx, ny))
                    visited.add((nx, ny))

    def update(self, x: int, y: int, color: tuple[int, int, int] | int, thickness: int = 0):
        neighbours = {(x, y)}
        for _ in range(thickness // 2):
            for n in list(neighbours):
                neighs = self.get_neighbours(*n)
                for neighbour in neighs:
                    neighbours.add(neighbour)

        for x, y in list(neighbours):
            if self.is_valid_coord(y, x):
                if self.filling:
                    self.flood_fill(x, y, color)
                else:
                    self.grid[y][x] = color

    @staticmethod
    def get_neighbours(x: int, y: int) -> list[tuple[int, int]]:
        return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y),
                (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

    @staticmethod
    def create_empty_board() -> list[list[int]]:
        return [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def clear(self):
        self.grid = self.create_empty_board()

    def get_board(self):
        return self.grid
