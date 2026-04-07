import random
import time
import heapq
import matplotlib.pyplot as plt

INF = float('inf')

# ---------------- GRAPH GENERATION ----------------

def generate_matrix(n, density):
    matrix = [[INF] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0
        for j in range(n):
            if i != j and random.random() < density:
                matrix[i][j] = random.randint(1, 10)
    return matrix

def matrix_to_list(matrix):
    n = len(matrix)
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != INF and i != j:
                graph[i].append((j, matrix[i][j]))
    return graph

# ---------------- DIJKSTRA ARRAY ----------------

def dijkstra_array(matrix, start):
    n = len(matrix)
    dist = [INF] * n
    visited = [False] * n
    dist[start] = 0

    for _ in range(n):
        u = -1
        min_dist = INF

        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        if u == -1:
            break

        visited[u] = True

        for v in range(n):
            if matrix[u][v] != INF and not visited[v]:
                if dist[u] + matrix[u][v] < dist[v]:
                    dist[v] = dist[u] + matrix[u][v]

    return dist

# ---------------- DIJKSTRA HEAP ----------------

def dijkstra_heap(graph, start):
    dist = {node: INF for node in graph}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, node = heapq.heappop(pq)

        for neighbor, weight in graph[node]:
            new_dist = current_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return dist

# ---------------- FLOYD-WARSHALL ----------------

def floyd_warshall(matrix):
    n = len(matrix)
    dist = [row[:] for row in matrix]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

# ---------------- EXPERIMENT ----------------

sizes = [10, 20, 30, 40, 50]

dij_array_sparse, dij_heap_sparse, fw_sparse = [], [], []
dij_array_dense, dij_heap_dense, fw_dense = [], [], []

for n in sizes:
    # Sparse
    matrix_s = generate_matrix(n, 0.1)
    list_s = matrix_to_list(matrix_s)

    start = time.perf_counter()
    dijkstra_array(matrix_s, 0)
    dij_array_sparse.append(time.perf_counter() - start)

    start = time.perf_counter()
    dijkstra_heap(list_s, 0)
    dij_heap_sparse.append(time.perf_counter() - start)

    start = time.perf_counter()
    floyd_warshall(matrix_s)
    fw_sparse.append(time.perf_counter() - start)

    # Dense
    matrix_d = generate_matrix(n, 0.9)
    list_d = matrix_to_list(matrix_d)

    start = time.perf_counter()
    dijkstra_array(matrix_d, 0)
    dij_array_dense.append(time.perf_counter() - start)

    start = time.perf_counter()
    dijkstra_heap(list_d, 0)
    dij_heap_dense.append(time.perf_counter() - start)

    start = time.perf_counter()
    floyd_warshall(matrix_d)
    fw_dense.append(time.perf_counter() - start)

# ---------------- CLEAN OUTPUT ----------------

print("\n===== SPARSE GRAPH RESULTS =====")

print("\nDijkstra Array:")
for i in range(len(sizes)):
    print(f"Nodes: {sizes[i]} -> {dij_array_sparse[i]:.6f} s")

print("\nDijkstra Heap:")
for i in range(len(sizes)):
    print(f"Nodes: {sizes[i]} -> {dij_heap_sparse[i]:.6f} s")

print("\nFloyd-Warshall:")
for i in range(len(sizes)):
    print(f"Nodes: {sizes[i]} -> {fw_sparse[i]:.6f} s")


print("\n===== DENSE GRAPH RESULTS =====")

print("\nDijkstra Array:")
for i in range(len(sizes)):
    print(f"Nodes: {sizes[i]} -> {dij_array_dense[i]:.6f} s")

print("\nDijkstra Heap:")
for i in range(len(sizes)):
    print(f"Nodes: {sizes[i]} -> {dij_heap_dense[i]:.6f} s")

print("\nFloyd-Warshall:")
for i in range(len(sizes)):
    print(f"Nodes: {sizes[i]} -> {fw_dense[i]:.6f} s")


# ---------------- INDIVIDUAL GRAPHS ----------------

# Dijkstra Array
plt.figure()
plt.plot(sizes, dij_array_sparse, marker='o', label="Sparse")
plt.plot(sizes, dij_array_dense, marker='o', label="Dense")
plt.title("Dijkstra Array Performance")
plt.xlabel("Number of Nodes")
plt.ylabel("Execution Time (s)")
plt.legend()
plt.grid()
plt.show()

# Dijkstra Heap
plt.figure()
plt.plot(sizes, dij_heap_sparse, marker='o', label="Sparse")
plt.plot(sizes, dij_heap_dense, marker='o', label="Dense")
plt.title("Dijkstra Heap Performance")
plt.xlabel("Number of Nodes")
plt.ylabel("Execution Time (s)")
plt.legend()
plt.grid()
plt.show()

# Floyd-Warshall
plt.figure()
plt.plot(sizes, fw_sparse, marker='o', label="Sparse")
plt.plot(sizes, fw_dense, marker='o', label="Dense")
plt.title("Floyd-Warshall Performance")
plt.xlabel("Number of Nodes")
plt.ylabel("Execution Time (s)")
plt.legend()
plt.grid()
plt.show()

# ---------------- COMBINED GRAPHS ----------------

# Sparse (ALL METHODS)
plt.figure()
plt.plot(sizes, dij_array_sparse, marker='o', label="Dijkstra Array")
plt.plot(sizes, dij_heap_sparse, marker='o', label="Dijkstra Heap")
plt.plot(sizes, fw_sparse, marker='o', label="Floyd-Warshall")
plt.title("All Algorithms - Sparse Graph")
plt.xlabel("Number of Nodes")
plt.ylabel("Execution Time (s)")
plt.legend()
plt.grid()
plt.show()

# Dense (ALL METHODS)
plt.figure()
plt.plot(sizes, dij_array_dense, marker='o', label="Dijkstra Array")
plt.plot(sizes, dij_heap_dense, marker='o', label="Dijkstra Heap")
plt.plot(sizes, fw_dense, marker='o', label="Floyd-Warshall")
plt.title("All Algorithms - Dense Graph")
plt.xlabel("Number of Nodes")
plt.ylabel("Execution Time (s)")
plt.legend()
plt.grid()
plt.show()