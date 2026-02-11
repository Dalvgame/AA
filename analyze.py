import time
import math
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

# Algorithms


# Dynamic Programming
def fib_dp(n):
    if n <= 1:
        return n

    F = [0] * (n + 1)
    F[1] = 1

    for i in range(2, n + 1):
        F[i] = F[i-1] + F[i-2]

    return F[n]


# Matrix method
def multiply(A, B):
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0],
         A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0],
         A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]


def matrix_power(M, n):
    result = [[1, 0], [0, 1]]
    base = M

    while n > 0:
        if n % 2 == 1:
            result = multiply(result, base)
        base = multiply(base, base)
        n //= 2

    return result


def fib_matrix(n):
    if n <= 1:
        return n

    M = [[0, 1], [1, 1]]
    result = matrix_power(M, n)
    return result[0][1]


# Binet method
def fib_binet(n):
    getcontext().prec = n + 5

    sqrt5 = Decimal(5).sqrt()
    phi = (Decimal(1) + sqrt5) / Decimal(2)
    psi = (Decimal(1) - sqrt5) / Decimal(2)

    result = (phi**n - psi**n) / sqrt5
    return int(result.to_integral_value())


# Iterative method
def fib_iterative(n):
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b

    return b


# Input set

inputs = [
    501, 631, 794, 1000,
    1259, 1585, 1995, 2512,
    3162, 3981, 5012, 6310,
    7943, 10000, 12589, 15849
]

algorithms = [
    ("DP", fib_dp),
    ("Matrix", fib_matrix),
    ("Binet", fib_binet),
    ("Iterative", fib_iterative)
]

# Measure execution times

results = []

for name, func in algorithms:
    row = []

    for n in inputs:
        runs = 5
        total = 0

        for _ in range(runs):
            start = time.perf_counter()
            func(n)
            end = time.perf_counter()
            total += (end - start)

        row.append(total / runs)

    results.append((name, row))


# Print table

print("\nFibonacci Algorithm Comparison\n")

col_width = 11

print("idx".ljust(3), end="")
for n in inputs:
    print(str(n).center(col_width), end="")
print()

print("-" * (5 + col_width * len(inputs)))

for i, (name, row) in enumerate(results):
    print(str(i).ljust(5), end="")
    for t in row:
        print(f"{t:.8f}".center(col_width), end="")
    print()

print()


# Graph comparison (all methods)

plt.figure()

for name, row in results:
    plt.plot(inputs, row, marker='o', label=name)

plt.title("Fibonacci Algorithm Comparison")
plt.xlabel("Fibonacci Term (n)")
plt.ylabel("Execution Time (seconds)")
plt.legend()
plt.grid(True)
plt.show()


# Separate graph for Iterative

plt.figure()

for name, row in results:
    if name == "Iterative":
        plt.plot(inputs, row, marker='o')

plt.title("Iterative Fibonacci Method Performance")
plt.xlabel("Fibonacci Term (n)")
plt.ylabel("Execution Time (seconds)")
plt.grid(True)
plt.show()
