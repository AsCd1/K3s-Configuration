# linear_operations.py

import random
import time

# Imposta seed per rendere l'array casuale sempre diverso
random.seed(time.time_ns())

# Funzione O(n): somma tutti gli elementi dell'array
def sum_array(arr):
    total = 0
    for val in arr:
        total += val
    return total

# Funzione per generare un array casuale
def genera_array_random(size, max_val):
    return [random.randint(0, max_val) for _ in range(size)]

# Test
if __name__ == "__main__":
    data = genera_array_random(10, 100)
    print("Array generato:", data)

    result = sum_array(data)
    print("Somma degli elementi (O(n)):", result)

