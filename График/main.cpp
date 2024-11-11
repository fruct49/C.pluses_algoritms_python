#include <SFML/Graphics.hpp>
#include <functional> 
#include <cmath> 
#include <string>

// ������� ��� ��������� �������
void drawGraph(sf::RenderWindow& window, std::function<float(float)> func, float xMin, float xMax, float scaleX, float scaleY, sf::Color color) {
    sf::VertexArray graph(sf::LinesStrip);

    for (float x = xMin; x <= xMax; x += 0.1f) {
        float y = func(x); // ���������� �������� �������

        // �������������� ��������� � ��������
        float screenX = 400 + x * scaleX;
        float screenY = 300 - y * scaleY;

        // ���������� ����� � ������ ������
        graph.append(sf::Vertex(sf::Vector2f(screenX, screenY), color));
    }

    window.draw(graph);
}

int main() {
    // �������� ����
    sf::RenderWindow window(sf::VideoMode(800, 600), "���������� ��� ������ ��������");

    // ���������� ��� �������� ���������������� �����
    sf::CircleShape userPoint(5); // ������ 5 ��������
    userPoint.setFillColor(sf::Color::Red);
    bool userPointExists = false; // �������� ������������� ���������������� �����

    // �������� ������
    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        return -1;
    }

    // ����� ��� ����������� ��������� �����
    sf::Text coordinatesText;
    coordinatesText.setFont(font);
    coordinatesText.setCharacterSize(20);
    coordinatesText.setPosition(10, 10);
    coordinatesText.setFillColor(sf::Color::White);
    coordinatesText.setString("Coordinates: ( , )");

    // ��� X � Y
    sf::VertexArray xAxis(sf::Lines, 2);
    xAxis[0].position = sf::Vector2f(50, 300);
    xAxis[0].color = sf::Color::White;
    xAxis[1].position = sf::Vector2f(750, 300);
    xAxis[1].color = sf::Color::White;

    sf::VertexArray yAxis(sf::Lines, 2);
    yAxis[0].position = sf::Vector2f(400, 50);
    yAxis[0].color = sf::Color::White;
    yAxis[1].position = sf::Vector2f(400, 550);
    yAxis[1].color = sf::Color::White;

    // �������
    float scaleX = 20.0f;
    float scaleY = 50.0f;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();

            // �������� ����� �����
            if (event.type == sf::Event::MouseButtonPressed) {
                if (event.mouseButton.button == sf::Mouse::Left) {
                    sf::Vector2i mousePos = sf::Mouse::getPosition(window);

                    // �������������� �������� ��������� � "��������������"
                    float mathX = (mousePos.x - 400) / scaleX;
                    float mathY = -(mousePos.y - 300) / scaleY;

                    // ��������� ����� ���������������� �����
                    userPoint.setPosition(mousePos.x - userPoint.getRadius(), mousePos.y - userPoint.getRadius());
                    userPointExists = true;

                    // ������ �������� � ����������� ����
                    std::string zone;
                    float tolerance = 0.2f; // ���������� ����������

                    // �������� ��������� �� �������
                    if (std::abs(mathY - std::abs(mathX)) <= tolerance) {
                        zone = "Granitsa";
                    }
                    else if (std::abs(mathY - 5) <= tolerance) {
                        zone = "Granitsa";
                    }
                    else if (mathY > std::abs(mathX) && mathY > 5) {
                        zone = "Zone 1";
                    }
                    else if (mathY > 5 && mathX < 0) {
                        zone = "Zone 4";
                    }
                    else if (mathX > 0 && mathY > 5) {
                        zone = "Zone 3";
                    }
                    else if (mathY > std::abs(mathX) && mathY < 5) {
                        zone = "Zone 2";
                    }
                    else {
                        zone = "Zone 5";
                    }

                    // ���������� ������ � ������������ ����� � ����
                    coordinatesText.setString("Coordinates: (" + std::to_string(mathX) + ", " + std::to_string(mathY) + ") - " + zone);
                }
            }
        }

        // ������� ������
        window.clear();

        // ��������� ����
        window.draw(xAxis);
        window.draw(yAxis);

        // ��������� ��������
        drawGraph(window, [](float x) { return std::abs(x); }, -10, 10, scaleX, scaleY, sf::Color::Blue);
        drawGraph(window, [](float x) { return 5; }, -10, 10, scaleX, scaleY, sf::Color::Red);

        // ��������� ���������������� ����� � ������
        if (userPointExists) {
            window.draw(userPoint);
            window.draw(coordinatesText);
        }

        // ����������� ������ �����
        window.display();
    }
    return 0;
}
