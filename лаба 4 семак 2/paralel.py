import random
import time
import multiprocessing as mp
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy

def partition(arr, left, right):
    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1

def quicksort(arr, left, right):
    if left < right:
        pivot = partition(arr, left, right)
        quicksort(arr, left, pivot - 1)
        quicksort(arr, pivot + 1, right)
    return arr

def parallel_quicksort_task(args):
    arr, left, right = args
    if left < right:
        pivot = partition(arr, left, right)
        quicksort(arr, left, pivot - 1)
        quicksort(arr, pivot + 1, right)
    return arr[left:right + 1]

def parallel_quicksort(arr, left, right, num_processes):
    if right - left < 1000:  # Порог для последовательной сортировки
        quicksort(arr, left, right)
    else:
        pivot = partition(arr, left, right)
        tasks = [(deepcopy(arr), left, pivot - 1), (deepcopy(arr), pivot + 1, right)]
        with mp.Pool(processes=num_processes) as pool:
            results = pool.map(parallel_quicksort_task, tasks)
        # Обновляем массив
        arr[left:pivot] = results[0]
        arr[pivot + 1:right + 1] = results[1]

def generate_random_array(size):
    return [random.randint(1, 1000000) for _ in range(size)]

def measure_time(sort_func, arr, num_processes=None):
    start = time.time()
    arr_copy = deepcopy(arr)
    if num_processes:
        sort_func(arr_copy, 0, len(arr_copy) - 1, num_processes)
    else:
        sort_func(arr_copy, 0, len(arr_copy) - 1)
    return time.time() - start

def main():
    sizes = [100, 1000, 10000, 20000, 30000, 40000, 50000]
    threads = [2, 4, 8]
    results = []

    for size in sizes:
        arr = generate_random_array(size)
        row = {"Array Size": size}

        # Последовательная сортировка
        row["Sequential (s)"] = measure_time(quicksort, arr)

        # Параллельная сортировка
        for num_threads in threads:
            row[f"Parallel {num_threads} Processes (s)"] = measure_time(parallel_quicksort, arr, num_threads)

        results.append(row)

    # Сохранение результатов
    df = pd.DataFrame(results)
    df.to_csv("results.csv", index=False)
    print("Results saved to results.csv")

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(df["Array Size"], df["Sequential (s)"], label="Sequential", marker="o")
    for num_threads in threads:
        plt.plot(df["Array Size"], df[f"Parallel {num_threads} Processes (s)"], label=f"{num_threads} Processes", marker="o")
    plt.xlabel("Array Size")
    plt.ylabel("Time (seconds)")
    plt.title("Quicksort Performance")
    plt.legend()
    plt.grid(True)
    plt.savefig("quicksort_performance.png")
    plt.close()

if __name__ == "__main__":
    main()