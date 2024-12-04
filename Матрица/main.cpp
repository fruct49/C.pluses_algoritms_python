#include <SFML/Graphics.hpp>
#include <iostream>

int main() {
    // ������ ���� � �������
    const int windowSize = 500;
    const int n = 10;           // ����������� ������� (5x5)
    const int cellSize = windowSize / n; // ������ ������ ��� ������������ ������������� �� ����

    // �������� ����
    sf::RenderWindow window(sf::VideoMode(windowSize, windowSize), "Matrix Visualization");

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // ������� ���� ����� ����� ����������
        window.clear(sf::Color::White);

        // ������� ���� ��� ��������� ������ ������ � ����� n x n
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                sf::RectangleShape cell(sf::Vector2f(cellSize, cellSize));
                cell.setPosition(j * cellSize, i * cellSize);

                // ������������� ���� ����� � �������
                cell.setOutlineThickness(1);
                cell.setOutlineColor(sf::Color::Black);

                // ���������, ��� ������� ������
                if ((j + 1) % 2 == 0) { // ��� ������� ���������, ��� ������� 2-�, 4-�, 6-� � �.�.
                    // ��� ������ �������� ����������, ������� ������ ����� ���������
                    int num_cells_to_fill = j;  

                    // ��������� ������, � ������� �������� �����������
                    int start_row = n - num_cells_to_fill; // �������� ����������� � ���� ������

                    // ���� ������ i >= start_row, �� ������ ������ ���� ���������
                    if (i >= start_row) {
                        cell.setFillColor(sf::Color::Green);
                    }
                    else {
                        cell.setFillColor(sf::Color::White); // ���� ������ �� �������� � ������ �������, �� ������ �����
                    }
                }
                else {
                    cell.setFillColor(sf::Color::White); // ��� �������� �������� ������ �������� ������
                }

                // ��������� ������
                window.draw(cell);
            }
        }

        // ����������� ����������
        window.display();
    }

    return 0;
}
