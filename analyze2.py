import random
import time
import matplotlib.pyplot as plt
import pandas as pd
import sys

sys.setrecursionlimit(1000000)


# ---------------- QUICK SORT ----------------
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)


# ---------------- MERGE SORT ----------------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------- HEAP SORT ----------------
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

    return arr


# ---------------- SHELL SORT ----------------
def shell_sort(arr):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i

            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap

            arr[j] = temp

        gap //= 2

    return arr


# ---------------- EXPERIMENT ----------------

sizes = [100, 1000, 5000, 10000, 20000, 50000, 100000]

quick_times = []
merge_times = []
heap_times = []
shell_times = []

print("\n========== EXECUTION TIMES ==========\n")

for n in sizes:
    original = [random.randint(0, 999) for _ in range(n)]
    print(f"\nArray Size: {n}")

    # Quick
    arr = original.copy()
    start = time.perf_counter()
    quick_sort(arr)
    end = time.perf_counter()
    qt = end - start
    quick_times.append(qt)
    print(f"QuickSort:  {qt:.6f} seconds")

    # Merge
    arr = original.copy()
    start = time.perf_counter()
    merge_sort(arr)
    end = time.perf_counter()
    mt = end - start
    merge_times.append(mt)
    print(f"MergeSort:  {mt:.6f} seconds")

    # Heap
    arr = original.copy()
    start = time.perf_counter()
    heap_sort(arr)
    end = time.perf_counter()
    ht = end - start
    heap_times.append(ht)
    print(f"HeapSort:   {ht:.6f} seconds")

    # Shell
    arr = original.copy()
    start = time.perf_counter()
    shell_sort(arr)
    end = time.perf_counter()
    st = end - start
    shell_times.append(st)
    print(f"ShellSort:  {st:.6f} seconds")

# ---------------- TABLE ----------------
data = {
    "Size (n)": sizes,
    "QuickSort (s)": quick_times,
    "MergeSort (s)": merge_times,
    "HeapSort (s)": heap_times,
    "ShellSort (s)": shell_times
}

df = pd.DataFrame(data)

print("\n\n========== FINAL COMPARISON TABLE ==========\n")
print(df.to_string(index=False))


# ---------------- INDIVIDUAL GRAPHS ----------------

def plot_individual(x, y, title):
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.xlabel("Input Size (n)")
    plt.ylabel("Execution Time (seconds)")
    plt.title(title)
    plt.grid(True)
    plt.show()


plot_individual(sizes, quick_times, "QuickSort Performance")
plot_individual(sizes, merge_times, "MergeSort Performance")
plot_individual(sizes, heap_times, "HeapSort Performance")
plot_individual(sizes, shell_times, "ShellSort Performance")

# ---------------- COMBINED GRAPH ----------------
plt.figure()

plt.plot(sizes, quick_times, marker='o')
plt.plot(sizes, merge_times, marker='o')
plt.plot(sizes, heap_times, marker='o')
plt.plot(sizes, shell_times, marker='o')

plt.xlabel("Input Size (n)")
plt.ylabel("Execution Time (seconds)")
plt.title("Sorting Algorithms Comparison")
plt.legend(["QuickSort", "MergeSort", "HeapSort", "ShellSort"])
plt.grid(True)

plt.show()