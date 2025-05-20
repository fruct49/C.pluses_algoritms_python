import pygame
import math
from queue import PriorityQueue

# Инициализация Pygame
pygame.init()  # Инициализируем библиотеку Pygame для работы с графикой

# Настройки окна
GRID_SIZE = 10  # Определяем размер сетки 10x10
CELL_SIZE = 50  # Устанавливаем размер одной ячейки в пикселях
WINDOW_SIZE = GRID_SIZE * CELL_SIZE  # Вычисляем общий размер окна
WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))  # Создаём окно с заданным размером
pygame.display.set_caption("A*")  # Устанавливаем заголовок окна

# Цвета
WHITE = (255, 255, 255)    # Цвет для пустой ячейки
BLACK = (0, 0, 0)          # Цвет для препятствий
ORANGE = (255, 165, 0)     # Цвет для начальной точки
TURQUOISE = (64, 224, 208) # Цвет для конечной точки
GREEN = (0, 255, 0)        # Цвет для ячеек в очереди (open set)
RED = (255, 0, 0)          # Цвет для посещённых ячеек (closed set)
PURPLE = (128, 0, 128)     # Цвет для итогового пути
GREY = (128, 128, 128)     # Цвет для линий сетки

# Класс ячейки
class Cell:
    def __init__(self, row, col):
        self.row = row  # Номер строки ячейки
        self.col = col  # Номер столбца ячейки
        self.x = row * CELL_SIZE  # Координата x для отрисовки
        self.y = col * CELL_SIZE  # Координата y для отрисовки
        self.color = WHITE  # Начальный цвет ячейки (пустая)
        self.neighbors = []  # Список соседних ячеек
        self.g = float("inf")  # Начальная стоимость пути от старта (бесконечность)
        self.h = 0  # Эвристическая оценка до цели
        self.f = float("inf")  # Полная оценка (g + h)
        self.came_from = None  # Родительская ячейка для восстановления пути
        self.is_barrier = False  # Флаг, обозначающий препятствие

    def get_pos(self):
        return self.row, self.col  # Возвращает позицию ячейки (row, col)

    def make_start(self):
        self.color = ORANGE  # Устанавливает цвет как начальную точку

    def make_end(self):
        self.color = TURQUOISE  # Устанавливает цвет как конечную точку

    def make_barrier(self):
        self.color = BLACK  # Устанавливает цвет как препятствие
        self.is_barrier = True  # Помечает ячейку как препятствие

    def make_open(self):
        self.color = GREEN  # Устанавливает цвет для ячеек в очереди

    def make_closed(self):
        self.color = RED  # Устанавливает цвет для посещённых ячеек

    def make_path(self):
        self.color = PURPLE  # Устанавливает цвет для итогового пути

    def reset(self):
        self.color = WHITE  # Сбрасывает цвет в исходное состояние
        self.is_barrier = False  # Снимает флаг препятствия

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))  # Отрисовка ячейки

    def update_neighbors(self, grid):
        self.neighbors = []  # Очищаем список соседей
        # Проверяем соседей (вверх, вниз, влево, вправо)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc  # Вычисляем координаты соседей
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and not grid[r][c].is_barrier:
                self.neighbors.append(grid[r][c])  # Добавляем допустимых соседей

# Создание сетки
def make_grid():
    grid = []  # Инициализируем список для сетки
    for i in range(GRID_SIZE):  # Проходим по строкам
        row = []  # Создаём строку
        for j in range(GRID_SIZE):  # Проходим по столбцам
            cell = Cell(i, j)  # Создаём ячейку
            row.append(cell)  # Добавляем ячейку в строку
        grid.append(row)  # Добавляем строку в сетку
    return grid  # Возвращаем созданную сетку

# Отрисовка линий сетки
def draw_grid_lines(win):
    for i in range(GRID_SIZE):  # Проходим по всем линиям
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE))  # Горизонтальные линии
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE))  # Вертикальные линии

# Отрисовка всего
def draw(win, grid):
    win.fill(WHITE)  # Заполняем окно белым фоном
    for row in grid:  # Проходим по всем строкам
        for cell in row:  # Проходим по всем ячейкам в строке
            cell.draw(win)  # Отрисовываем каждую ячейку
    draw_grid_lines(win)  # Рисуем линии сетки
    pygame.display.update()  # Обновляем дисплей

# Манхэттенское расстояние
def h(p1, p2):
    x1, y1 = p1  # Координаты первой точки
    x2, y2 = p2  # Координаты второй точки
    return abs(x1 - x2) + abs(y1 - y2)  # Вычисляем манхэттенское расстояние

# Восстановление пути
def reconstruct_path(came_from, current, draw_func):
    while current in came_from:  # Пока есть родительская ячейка
        current = came_from[current]  # Переходим к родителю
        current.make_path()  # Помечаем ячейку как часть пути
        draw_func()  # Обновляем визуализацию

# Алгоритм A*
def a_star_algorithm(draw_func, grid, start, end):
    count = 0  # Счётчик для разрешения конфликтов в PriorityQueue
    open_set = PriorityQueue()  # Создаём очередь с приоритетом для открытых узлов
    open_set.put((0, count, start))  # Добавляем начальную точку с f=0
    open_set_hash = {start}  # Множество для быстрого поиска узлов в open_set

    start.g = 0  # Устанавливаем стоимость пути от старта до старта
    start.h = h(start.get_pos(), end.get_pos())  # Вычисляем эвристику до цели
    start.f = start.g + start.h  # Вычисляем полную оценку f

    came_from = {}  # Словарь для хранения родительских узлов

    while not open_set.empty():  # Пока очередь не пуста
        for event in pygame.event.get():  # Проверяем события
            if event.type == pygame.QUIT:  # Если окно закрыто
                pygame.quit()  # Завершаем Pygame
                return False  # Прерываем алгоритм

        current = open_set.get()[2]  # Извлекаем узел с минимальным f
        open_set_hash.remove(current)  # Удаляем его из множества

        if current == end:  # Если достигли цели
            reconstruct_path(came_from, end, draw_func)  # Восстанавливаем путь
            start.make_start()  # Восстанавливаем цвет начальной точки
            end.make_end()  # Восстанавливаем цвет конечной точки
            return True  # Успешное завершение

        current.make_closed()  # Помечаем текущую ячейку как посещённую

        for neighbor in current.neighbors:  # Проверяем всех соседей
            temp_g = current.g + 1  # Увеличиваем стоимость пути на 1
            if temp_g < neighbor.g:  # Если новый путь короче
                came_from[neighbor] = current  # Запоминаем родителя
                neighbor.g = temp_g  # Обновляем стоимость пути
                neighbor.h = h(neighbor.get_pos(), end.get_pos())  # Обновляем эвристику
                neighbor.f = neighbor.g + neighbor.h  # Обновляем полную оценку

                if neighbor not in open_set_hash:  # Если сосед ещё не в очереди
                    count += 1  # Увеличиваем счётчик
                    open_set.put((neighbor.f, count, neighbor))  # Добавляем в очередь
                    open_set_hash.add(neighbor)  # Добавляем в множество
                    neighbor.make_open()  # Помечаем как открытый

        draw_func()  # Обновляем визуализацию

    return False  # Путь не найден

# Основная функция
def main():
    grid = make_grid()  # Создаём сетку
    obstacles = [
        (0, 0), (1, 0), (1, 1), (1, 2),
        (0, 4), (1, 4), (3, 4), (4, 4),
        (5, 0), (6, 0), (8, 1), (4, 2),
        (5, 2), (6, 2), (6, 0), (9, 2),
        (5, 3), (8, 4), (9, 4), (7, 5),
        (0, 6), (1, 6), (2, 6), (4, 6),
        (5, 6), (8, 6), (9, 6), (3, 7),
        (5, 7), (9, 7), (1, 8), (2, 8),
        (1, 9), (2, 9), (4, 9), (5, 9),
        (6, 9), (7, 9)
    ]  # Список координат препятствий
    for row, col in obstacles:  # Проходим по всем препятствиям
        grid[row][col].make_barrier()  # Помечаем ячейки как препятствия

    # Установка начальной и конечной точек
    start = grid[0][3]  # Устанавливаем начальную точку (0, 3)
    end = grid[9][9]    # Устанавливаем конечную точку (9, 9)
    start.make_start()  # Помечаем начальную точку
    end.make_end()  # Помечаем конечную точку

    # Обновление соседей для всех ячеек
    for row in grid:  # Проходим по всем строкам
        for cell in row:  # Проходим по всем ячейкам
            cell.update_neighbors(grid)  # Обновляем список соседей

    run = True  # Флаг для работы основного цикла
    started = False  # Флаг для запуска алгоритма

    while run:  # Основной цикл программы
        draw(WIN, grid)  # Отрисовываем текущее состояние
        for event in pygame.event.get():  # Проверяем события
            if event.type == pygame.QUIT:  # Если окно закрыто
                run = False  # Завершаем цикл

            if event.type == pygame.KEYDOWN:  # Обработка нажатий клавиш
                if event.key == pygame.K_SPACE and not started:  # Нажата клавиша пробела
                    started = True  # Запускаем алгоритм
                    a_star_algorithm(lambda: draw(WIN, grid), grid, start, end)  # Выполняем A*
                if event.key == pygame.K_r:  # Нажата клавиша R
                    main()  # Перезапускаем программу

    pygame.quit()  # Завершаем Pygame

if __name__ == "__main__":
    main()