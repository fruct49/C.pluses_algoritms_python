import pygame
import math
from queue import PriorityQueue

# Инициализация Pygame
pygame.init()

# Настройки окна
GRID_SIZE = 10  # Размер сетки 10x10
CELL_SIZE = 50  # Размер ячейки в пикселях
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("A*")

# Цвета
WHITE = (255, 255, 255)    # Пустая ячейка
BLACK = (0, 0, 0)          # Препятствие
ORANGE = (255, 165, 0)     # Начало
TURQUOISE = (64, 224, 208) # Конец
GREEN = (0, 255, 0)        # В очереди
RED = (255, 0, 0)          # Посещённая
PURPLE = (128, 0, 128)     # Итоговый путь
GREY = (128, 128, 128)     # Серые линии сетки

# Класс ячейки
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * CELL_SIZE
        self.y = col * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.g = float("inf")  # Расстояние от старта
        self.h = 0             # Эвристика до цели
        self.f = float("inf")  # Полная оценка (g + h)
        self.came_from = None  # Для восстановления пути
        self.is_barrier = False

    def get_pos(self):
        return self.row, self.col

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_barrier(self):
        self.color = BLACK
        self.is_barrier = True

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    def make_path(self):
        self.color = PURPLE

    def reset(self):
        self.color = WHITE
        self.is_barrier = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Проверяем соседей (вверх, вниз, влево, вправо)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and not grid[r][c].is_barrier:
                self.neighbors.append(grid[r][c])

# Создание сетки
def make_grid():
    grid = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            cell = Cell(i, j)
            row.append(cell)
        grid.append(row)
    return grid

# Отрисовка линий сетки
def draw_grid_lines(win):
    for i in range(GRID_SIZE):
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE))
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE))

# Отрисовка всего
def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)
    draw_grid_lines(win)
    pygame.display.update()

# Манхэттенское расстояние
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Восстановление пути
def reconstruct_path(came_from, current, draw_func):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw_func()

# Алгоритм A*
def a_star_algorithm(draw_func, grid, start, end):
    count = 0  # Для разрешения конфликтов в PriorityQueue
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}  # Для быстрого поиска

    start.g = 0
    start.h = h(start.get_pos(), end.get_pos())
    start.f = start.g + start.h

    came_from = {}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw_func)
            start.make_start()
            end.make_end()
            return True

        current.make_closed()

        for neighbor in current.neighbors:
            temp_g = current.g + 1  # Стоимость перехода = 1
            if temp_g < neighbor.g:
                came_from[neighbor] = current
                neighbor.g = temp_g
                neighbor.h = h(neighbor.get_pos(), end.get_pos())
                neighbor.f = neighbor.g + neighbor.h

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw_func()

    return False

# Основная функция
def main():
    grid = make_grid()
    obstacles = [
        (0, 0), (1, 0), (1, 1), (1, 2),
        (0, 4), (1, 4), (3, 4), (4, 4),
        (5, 0), (6, 0), (8, 1), (4, 2),
        (5, 2), (6, 2),(6, 0), (9, 2),
        (5, 3), (8, 4), (9, 4), (7, 5),
        (0, 6), (1, 6), (2, 6), (4, 6),
        (5, 6), (8, 6), (9, 6),(3, 7),
        (5, 7), (9, 7),(1, 8), (2, 8),
        (1, 9),(2, 9), (4, 9), (5, 9),
        (6, 9),(7,9)
    ]
    for row, col in obstacles:
        grid[row][col].make_barrier()

    # Установка начальной и конечной точек
    start = grid[0][3]  # Начало (0, 3)
    end = grid[9][9]    # Конец (9, 9)
    start.make_start()
    end.make_end()

    # Обновление соседей для всех ячеек
    for row in grid:
        for cell in row:
            cell.update_neighbors(grid)

    run = True
    started = False

    while run:
        draw(WIN, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    a_star_algorithm(lambda: draw(WIN, grid), grid, start, end)
                if event.key == pygame.K_r:  # Сброс
                    main()  # Перезапуск

    pygame.quit()

if __name__ == "__main__":
    main()