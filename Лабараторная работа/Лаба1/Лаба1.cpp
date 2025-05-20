#include <iostream>
#include <cmath> 
#include <locale>
int main() {
    setlocale(LC_ALL, "Russian");
    system("chcp 1251");

    float x, y;
    std::cout << "Введите X и Y: ";
    std::cin >> x >> y;

    float R = (-x - sqrt(exp(2) - 4 * x * y)) / (2 * x); 
    float S = log(x) * tan(y);

    std::cout << "R = " << R << std::endl;
    std::cout << "S = " << S << std::endl;

    float C = std::fmax(R, S); 

    std::cout << "Максимальное значение C = " << C << std::endl;
    system("pause");
    return 0;
}
