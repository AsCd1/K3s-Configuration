import random
import time

# Imposta il seed per garantire un array diverso a ogni esecuzione
random.seed(time.time_ns())

# Funzione O(n): somma gli elementi di un array
def sum_array(arr):
    total = 0
    for val in arr:
        total += val
    return total

# Funzione O(n²): bubble sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# Genera un array casuale
def genera_array_random(size, max_val):
    return [random.randint(0, max_val) for _ in range(size)]

# Main test
for test_num in range(1, 4):
    print(f"\nTest #{test_num}")
    data = genera_array_random(10, 100)
    print("Array originale:", data)

    total = sum_array(data)
    print("Somma degli elementi:", total)

    bubble_sort(data)
    print("Array ordinato:", data)
