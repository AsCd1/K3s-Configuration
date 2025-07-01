# quadratic_operations.py

import random
import time

# Imposta seed per rendere l'array casuale sempre diverso
random.seed(time.time_ns())

# Funzione O(n²): Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# Funzione per generare un array casuale
def genera_array_random(size, max_val):
    return [random.randint(0, max_val) for _ in range(size)]

# Test
if __name__ == "__main__":
    data = genera_array_random(10, 100)
    print("Array generato:", data)

    bubble_sort(data)
    print("Array ordinato con Bubble Sort (O(n²)):", data)
