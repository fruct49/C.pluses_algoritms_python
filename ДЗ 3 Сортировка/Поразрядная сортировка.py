import random
def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        index = (num // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        num = arr[i]
        index = (num // exp) % 10
        output[count[index] - 1] = num
        count[index] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]

random_array = [random.randint(1, 10000) for _ in range(100)]

print("Неотсортированный массив:")
print(random_array)

radix_sort(random_array)

print("\nОтсортированный массив:")
print(random_array)