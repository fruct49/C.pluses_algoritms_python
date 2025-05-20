import random
import time
def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

arr = [random.randint(1, 10000) for _ in range(1000)]
print("\nНеотсортированный массив (первые 10 элементов):", arr[:10])

start_time = time.time() * 1000
quick_sort(arr, 0, len(arr) - 1)
end_time = time.time() * 1000

print("Отсортированный массив (первые 10 элементов):", arr[:10])
print(f"Время выполнения Quick Sort: {end_time - start_time:.3f} мс")