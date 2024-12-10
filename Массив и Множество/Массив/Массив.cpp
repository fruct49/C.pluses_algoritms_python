#include <iostream>
#include <windows.h>

void filterArray(const int* A, int sizeA, int*& B, int& sizeB) {
    sizeB = 0;
    B = new int[sizeA];

    for (int i = 0; i < sizeA; i++) {
        if (A[i] > 10 && A[i] < 50) {
            B[sizeB] = A[i];
            sizeB++;
        }
    }
}

int main() {
    SetConsoleOutputCP(1251);
    SetConsoleCP(1251);

    const int sizeA = 10;
    int A[sizeA];

    std::cout << "Введите 10 элементов массива A (целые числа):" << std::endl;
    for (int i = 0; i < sizeA; i++) {
        std::cout << "A[" << i << "] = ";
        std::cin >> A[i];
    }

    int* B = nullptr;
    int sizeB = 0;

    filterArray(A, sizeA, B, sizeB);

    std::cout << "Массив B (элементы массива A, которые больше 10 и меньше 50): ";
    for (int i = 0; i < sizeB; i++) {
        std::cout << B[i] << " ";
    }
    std::cout << std::endl;

    delete[] B;

    std::cout << "Нажмите любую клавишу для завершения программы..." << std::endl;
    std::cin.get();
    std::cin.get();
    return 0;
}
