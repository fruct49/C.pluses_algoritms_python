#include <SFML/Graphics.hpp>
#include <iostream>

int main() {
    // Размер окна и матрицы
    const int windowSize = 500;
    const int n = 10;           // размерность матрицы (5x5)
    const int cellSize = windowSize / n; // размер ячейки для равномерного распределения по окну

    // Создание окна
    sf::RenderWindow window(sf::VideoMode(windowSize, windowSize), "Matrix Visualization");

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Очистка окна перед новой отрисовкой
        window.clear(sf::Color::White);

        // Двойной цикл для отрисовки каждой ячейки в сетке n x n
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                sf::RectangleShape cell(sf::Vector2f(cellSize, cellSize));
                cell.setPosition(j * cellSize, i * cellSize);

                // Устанавливаем цвет рамки и заливки
                cell.setOutlineThickness(1);
                cell.setOutlineColor(sf::Color::Black);

                // Проверяем, что столбец чётный
                if ((j + 1) % 2 == 0) { // Это условие проверяет, что столбец 2-й, 4-й, 6-й и т.д.
                    // Для чётных столбцов определяем, сколько клеток нужно закрасить
                    int num_cells_to_fill = j;  

                    // Вычисляем строку, с которой начинаем закрашивать
                    int start_row = n - num_cells_to_fill; // Начинаем закрашивать с этой строки

                    // Если строка i >= start_row, то клетка должна быть закрашена
                    if (i >= start_row) {
                        cell.setFillColor(sf::Color::Green);
                    }
                    else {
                        cell.setFillColor(sf::Color::White); // Если строка не попадает в нужную область, то клетка белая
                    }
                }
                else {
                    cell.setFillColor(sf::Color::White); // Для нечётных столбцов клетки остаются белыми
                }

                // Отрисовка ячейки
                window.draw(cell);
            }
        }

        // Отображение результата
        window.display();
    }

    return 0;
}
