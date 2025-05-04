import random
import time
import multiprocessing as mp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import List
import heapq


def partition(arr: List[int], left: int, right: int) -> int:
    """Разделение массива для быстрой сортировки."""
    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


def quick_sort(arr: List[int]) -> List[int]:
    """Последовательная быстрая сортировка."""

    def _quick_sort(arr, left, right):
        if left < right:
            pivot = partition(arr, left, right)
            _quick_sort(arr, left, pivot - 1)
            _quick_sort(arr, pivot + 1, right)

    arr_copy = arr[:]
    _quick_sort(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def merge_sorted_arrays(arrays: List[List[int]]) -> List[int]:
    """Объединение отсортированных массивов с использованием heapq.merge."""
    return list(heapq.merge(*arrays))


def parallel_quick_sort(arr: List[int], num_processes: int) -> List[int]:
    """Параллельная быстрая сортировка с разделением на чанки."""
    if num_processes <= 1 or len(arr) < 10000:  # Увеличенный порог
        return quick_sort(arr)

    # Разделяем массив на чанки
    chunk_size = len(arr) // num_processes
    chunks = [arr[i * chunk_size:(i + 1) * chunk_size] for i in range(num_processes)]
    if len(arr) % num_processes != 0:
        chunks[-1].extend(arr[num_processes * chunk_size:])

    # Параллельная сортировка чанков
    with mp.Pool(processes=num_processes) as pool:
        sorted_chunks = pool.map(quick_sort, chunks)

    # Объединяем отсортированные чанки
    return merge_sorted_arrays(sorted_chunks)


def generate_random_array(size: int) -> List[int]:
    """Генерация случайного массива."""
    return [random.randint(1, 1000000) for _ in range(size)]


def measure_time(sort_func, arr: List[int], num_processes: int = None, runs: int = 3) -> float:
    """Замер времени выполнения с усреднением."""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        if num_processes:
            sort_func(arr, num_processes)
        else:
            sort_func(arr)
        times.append(time.perf_counter() - start)
    return np.mean(times)


def main():
    sizes = [100, 1000, 5000, 10000]  # Уменьшенные размеры для теста
    threads = [2, 4, 8]
    results = []

    print("Starting measurements...")
    for size in sizes:
        arr = generate_random_array(size)
        row = {"Array Size": size}

        # Последовательная сортировка
        seq_time = measure_time(quick_sort, arr)
        row["Sequential (s)"] = seq_time
        print(f"Size {size}: Sequential = {seq_time:.6f}s")

        # Параллельная сортировка
        for num_threads in threads:
            par_time = measure_time(parallel_quick_sort, arr, num_threads)
            row[f"Parallel {num_threads} Processes (s)"] = par_time
            print(f"Size {size}: Parallel {num_threads} processes = {par_time:.6f}s")

        # Расчет коэффициентов ускорения
        for num_threads in threads:
            parallel_time = row[f"Parallel {num_threads} Processes (s)"]
            row[f"Speedup ({num_threads} processes)"] = row[
                                                            "Sequential (s)"] / parallel_time if parallel_time > 0 else float(
                'inf')

        results.append(row)

    # Сохранение результатов
    df = pd.DataFrame(results)
    df.to_csv("results.csv", index=False)
    print("Results saved to results.csv")

    # График времени выполнения
    plt.figure(figsize=(10, 6))
    plt.plot(df["Array Size"], df["Sequential (s)"], label="Sequential", marker="o")
    for num_threads in threads:
        plt.plot(df["Array Size"], df[f"Parallel {num_threads} Processes (s)"], label=f"{num_threads} Processes",
                 marker="o")
    plt.xlabel("Array Size")
    plt.ylabel("Time (seconds)")
    plt.title("Quicksort Performance")
    plt.legend()
    plt.grid(True)
    plt.savefig("quicksort_performance.png")
    plt.close()

    # График коэффициентов ускорения
    plt.figure(figsize=(10, 6))
    for num_threads in threads:
        plt.plot(df["Array Size"], df[f"Speedup ({num_threads} processes)"], label=f"{num_threads} Processes",
                 marker="o")
    plt.xlabel("Array Size")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Array Size")
    plt.legend()
    plt.grid(True)
    plt.savefig("speedup_plot.png")
    plt.close()


if __name__ == "__main__":
    main()