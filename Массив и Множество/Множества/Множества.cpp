#include <iostream>
#include <windows.h>

void findIntersection(const int* A, const int* B, int sizeA, int sizeB, int*& intersection, int& sizeIntersection) {
    sizeIntersection = 0;
    intersection = new int[sizeA < sizeB ? sizeA : sizeB];

    for (int i = 0; i < sizeA; i++) {
        for (int j = 0; j < sizeB; j++) {
            if (A[i] == B[j]) {
                bool alreadyExists = false;
                for (int k = 0; k < sizeIntersection; k++) {
                    if (intersection[k] == A[i]) {
                        alreadyExists = true;
                        break;
                    }
                }
                if (!alreadyExists) {
                    intersection[sizeIntersection++] = A[i];
                }
            }
        }
    }
}

int calculateSum(const int* arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

int main() {
    SetConsoleOutputCP(1251);  
    SetConsoleCP(1251);        

    int sizeA, sizeB;

    std::cout << "Введите размер множества A: ";
    std::cin >> sizeA;
    int* A = new int[sizeA];

    std::cout << "Введите элементы множества A:" << std::endl;
    for (int i = 0; i < sizeA; i++) {
        std::cout << "A[" << i << "] = ";
        std::cin >> A[i];
    }

    std::cout << "Введите размер множества B: ";
    std::cin >> sizeB;
    int* B = new int[sizeB];

    std::cout << "Введите элементы множества B:" << std::endl;
    for (int i = 0; i < sizeB; i++) {
        std::cout << "B[" << i << "] = ";
        std::cin >> B[i];
    }

    int* intersection = nullptr;
    int sizeIntersection = 0;

    findIntersection(A, B, sizeA, sizeB, intersection, sizeIntersection);

    std::cout << "Пересечение множеств A и B: ";
    for (int i = 0; i < sizeIntersection; i++) {
        std::cout << intersection[i] << " ";
    }
    std::cout << std::endl;

    int sum = calculateSum(intersection, sizeIntersection);
    std::cout << "Сумма элементов пересечения: " << sum << std::endl;

    delete[] A;
    delete[] B;
    delete[] intersection;

    std::cout << "Нажмите любую клавишу для завершения программы..." << std::endl;
    std::cin.get();   
    std::cin.get();  

    return 0;
}
