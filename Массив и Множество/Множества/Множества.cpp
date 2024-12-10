#include <iostream>
#include <windows.h>
#include <set>
#include <numeric> 

std::set<int> findIntersection(const std::set<int>& A, const std::set<int>& B) {
    std::set<int> intersection;
    for (const int& elem : A) {
        if (B.find(elem) != B.end()) { 
            intersection.insert(elem);
        }
    }
    return intersection;
}

int calculateSum(const std::set<int>& s) {
    return std::accumulate(s.begin(), s.end(), 0); 
}

int main() {
    SetConsoleOutputCP(1251);
    SetConsoleCP(1251);

    int sizeA, sizeB;

    std::cout << "Введите размер множества A: ";
    std::cin >> sizeA;
    std::set<int> A;

    std::cout << "Введите элементы множества A:" << std::endl;
    for (int i = 0; i < sizeA; i++) {
        int elem;
        std::cout << "A[" << i << "] = ";
        std::cin >> elem;
        A.insert(elem); 
    }

    std::cout << "Введите размер множества B: ";
    std::cin >> sizeB;
    std::set<int> B;

    std::cout << "Введите элементы множества B:" << std::endl;
    for (int i = 0; i < sizeB; i++) {
        int elem;
        std::cout << "B[" << i << "] = ";
        std::cin >> elem;
        B.insert(elem); 
    }

    std::set<int> intersection = findIntersection(A, B);

    std::cout << "Пересечение множеств A и B: ";
    for (const int& elem : intersection) {
        std::cout << elem << " ";
    }
    std::cout << std::endl;

    int sum = calculateSum(intersection);
    std::cout << "Сумма элементов пересечения: " << sum << std::endl;

    std::cout << "Нажмите любую клавишу для завершения программы..." << std::endl;
    std::cin.get();
    std::cin.get();

    return 0;
}
