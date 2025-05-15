def find_first_occurrence(nums, target):
    left, right = 0, len(nums) - 1
    first_occurrence = -1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            first_occurrence = mid
            right = mid - 1  # Продолжаем искать в левой половине
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return first_occurrence

def find_last_occurrence(nums, target):
    left, right = 0, len(nums) - 1
    last_occurrence = -1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            last_occurrence = mid
            left = mid + 1  # Продолжаем искать в правой половине
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return last_occurrence

def find_occurrences(nums, target):
    first = find_first_occurrence(nums, target)
    last = find_last_occurrence(nums, target)

    if first == -1:
        print(f"Число {target} не найдено в массиве")
    else:
        print(f"Первое вхождение числа {target} находится по индексу {first}")
        print(f"Последнее вхождение числа {target} находится по индексу {last}")

# Пример использования
nums = [2, 5, 5, 5, 6, 6, 8, 9, 9, 9]
target = 5
find_occurrences(nums, target)

target = 4
find_occurrences(nums, target)