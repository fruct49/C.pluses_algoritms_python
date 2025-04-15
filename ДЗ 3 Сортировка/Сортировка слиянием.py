import random
import time
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort(left)
        merge_sort(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

arr = [random.randint(1, 10000) for _ in range(1000)]
print("\nНеотсортированный массив (первые 10 элементов):", arr[:10])

start_time = time.time() * 1000
merge_sort(arr)
end_time = time.time() * 1000

print("Отсортированный массив (первые 10 элементов):", arr[:10])
print(f"Время выполнения Merge Sort: {end_time - start_time:.3f} мс")