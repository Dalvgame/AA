import random
import time
import matplotlib.pyplot as plt
from collections import defaultdict, deque


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)  # undirected graph

    # ================= DFS =================
    def dfs_util(self, node, visited):
        visited.add(node)
        for neighbor in self.graph[node]:
            if neighbor not in visited:
                self.dfs_util(neighbor, visited)

    def dfs(self, start):
        visited = set()
        self.dfs_util(start, visited)

    # ================= BFS =================
    def bfs(self, start):
        visited = set()
        queue = deque()

        visited.add(start)
        queue.append(start)

        while queue:
            node = queue.popleft()
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


# ================= GRAPH GENERATION =================
def generate_graph(n, edges_per_node=3):
    g = Graph()

    for i in range(n):
        for _ in range(edges_per_node):
            j = random.randint(0, n - 1)
            if j != i:
                g.add_edge(i, j)

    return g


# ================= EXPERIMENT =================
def measure_time(graph, method):
    start = time.perf_counter()
    method(0)  # always start from node 0
    end = time.perf_counter()
    return end - start


def run_experiment():
    sizes = [10, 50, 100, 200, 300, 400, 500]

    dfs_times = []
    bfs_times = []

    for n in sizes:
        g = generate_graph(n)

        dfs_time = measure_time(g, g.dfs)
        bfs_time = measure_time(g, g.bfs)

        dfs_times.append(dfs_time)
        bfs_times.append(bfs_time)

        print(f"n={n} | DFS={dfs_time:.6f} | BFS={bfs_time:.6f}")

    return sizes, dfs_times, bfs_times


# ================= PLOT =================
def plot_bfs(sizes, bfs_times):
    plt.figure()

    plt.plot(sizes, bfs_times, marker='s')

    plt.xlabel("Number of Nodes (n)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("BFS Empirical Analysis")
    plt.grid()

    plt.show()
def plot_dfs(sizes, dfs_times):
    plt.figure()

    plt.plot(sizes, dfs_times, marker='o')

    plt.xlabel("Number of Nodes (n)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("DFS Empirical Analysis")
    plt.grid()

    plt.show()
def plot_results(sizes, dfs_times, bfs_times):
    plt.figure()

    plt.plot(sizes, dfs_times, marker='o', label='DFS')
    plt.plot(sizes, bfs_times, marker='s', label='BFS')

    plt.xlabel("Number of Nodes (n)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("DFS vs BFS Empirical Analysis")
    plt.legend()
    plt.grid()

    plt.show()



# ================= MAIN =================
if __name__ == "__main__":
    sizes, dfs_times, bfs_times = run_experiment()

    # Separate graphs
    plot_dfs(sizes, dfs_times)
    plot_bfs(sizes, bfs_times)

    # Combined graph (optional but recommended)
    plot_results(sizes, dfs_times, bfs_times)