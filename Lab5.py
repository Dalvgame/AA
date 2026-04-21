import heapq
import time
import random
import matplotlib.pyplot as plt
from collections import defaultdict


# ── Union-Find (Disjoint Set Union) for Kruskal ──────────────────────────────
class DSU:
    def __init__(self, n):
        self.root = list(range(n))
        self.depth = [0] * n

    def find(self, x):
        while self.root[x] != x:
            self.root[x] = self.root[self.root[x]]   # path halving
            x = self.root[x]
        return x

    def merge(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.depth[ra] < self.depth[rb]:
            ra, rb = rb, ra
        self.root[rb] = ra
        if self.depth[ra] == self.depth[rb]:
            self.depth[ra] += 1
        return True


# ── Kruskal's Algorithm ───────────────────────────────────────────────────────
def kruskal(n, edges):
    sorted_edges = sorted(edges)          # sort by (weight, u, v)
    dsu = DSU(n)
    total_weight = 0
    tree_edges = []
    for w, u, v in sorted_edges:
        if dsu.merge(u, v):
            total_weight += w
            tree_edges.append((u, v, w))
            if len(tree_edges) == n - 1:
                break
    return total_weight, tree_edges


# ── Prim's Algorithm ──────────────────────────────────────────────────────────
def prim(n, adj):
    in_tree = [False] * n
    heap = [(0, 0, -1)]                   # (cost, node, parent)
    total_weight = 0
    tree_edges = []
    while heap:
        cost, node, par = heapq.heappop(heap)
        if in_tree[node]:
            continue
        in_tree[node] = True
        total_weight += cost
        if par != -1:
            tree_edges.append((par, node, cost))
        for edge_cost, nbr in adj[node]:
            if not in_tree[nbr]:
                heapq.heappush(heap, (edge_cost, nbr, node))
    return total_weight, tree_edges


# ── Random connected graph generator ─────────────────────────────────────────
def build_random_graph(n, max_w=100):
    """
    Builds a random connected graph with ~2n edges.
    Connectivity is guaranteed by a random spanning tree;
    then ~n extra edges are added between random pairs.
    """
    edges = []
    adj   = defaultdict(list)
    nodes = list(range(n))
    random.shuffle(nodes)

    # Random spanning tree (not just a chain) using Prüfer-like shuffle
    for i in range(1, n):
        u = nodes[i]
        v = nodes[random.randint(0, i - 1)]   # connect to any earlier node
        w = random.randint(1, max_w)
        edges.append((w, u, v))
        adj[u].append((w, v))
        adj[v].append((w, u))

    # Extra random edges
    extra = n
    attempts = 0
    added = 0
    while added < extra and attempts < extra * 4:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            w = random.randint(1, max_w)
            edges.append((w, u, v))
            adj[u].append((w, v))
            adj[v].append((w, u))
            added += 1
        attempts += 1

    return edges, adj


# ── Small-graph demo ──────────────────────────────────────────────────────────
def demo():
    print("=== Demo on a 6-node graph ===")
    raw = [
        (1, 0, 1), (4, 0, 2), (3, 1, 2), (2, 1, 3),
        (5, 2, 3), (6, 2, 4), (7, 3, 4), (3, 3, 5),
        (8, 4, 5)
    ]
    n = 6
    adj = defaultdict(list)
    for w, u, v in raw:
        adj[u].append((w, v))
        adj[v].append((w, u))

    kw, ke = kruskal(n, raw)
    print(f"Kruskal  – MST weight: {kw},  edges: {ke}")

    pw, pe = prim(n, adj)
    print(f"Prim     – MST weight: {pw},  edges: {pe}")
    print()


# ── Empirical timing ──────────────────────────────────────────────────────────
def run_analysis():
    sizes   = [10, 50, 100, 200, 500, 1000, 2000, 3000, 5000]
    k_times = []
    p_times = []
    runs    = 3

    print(f"{'Nodes':>8}  {'Kruskal (ms)':>14}  {'Prim (ms)':>12}")
    print("-" * 40)

    for n in sizes:
        kt = pt = 0.0
        for _ in range(runs):
            edges, adj = build_random_graph(n)

            t = time.perf_counter()
            kruskal(n, edges)
            kt += time.perf_counter() - t

            t = time.perf_counter()
            prim(n, adj)
            pt += time.perf_counter() - t

        kt_ms = kt / runs * 1000
        pt_ms = pt / runs * 1000
        k_times.append(kt_ms)
        p_times.append(pt_ms)
        print(f"{n:>8}  {kt_ms:>14.3f}  {pt_ms:>12.3f}")

    return sizes, k_times, p_times


# ── Plotting ──────────────────────────────────────────────────────────────────
KRUSKAL_COLOR = "#27ae60"   # green
PRIM_COLOR    = "#e67e22"   # orange
RATIO_COLOR   = "#8e44ad"   # purple

# Plots are saved in the same folder as this script.
# Change OUTPUT_DIR to any path you prefer, e.g. r"C:\Users\You\Desktop\plots"
import os
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def make_plots(sizes, k_times, p_times):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Prim alone ---
    plt.figure(figsize=(7, 5))
    plt.plot(sizes, p_times, "D-", color=PRIM_COLOR, linewidth=2, markersize=6)
    plt.title("Prim's Algorithm – Execution Time vs Number of Nodes")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (ms)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "plot_prim.png"), dpi=150)
    plt.close()

    # --- Kruskal alone ---
    plt.figure(figsize=(7, 5))
    plt.plot(sizes, k_times, "o-", color=KRUSKAL_COLOR, linewidth=2, markersize=6)
    plt.title("Kruskal's Algorithm – Execution Time vs Number of Nodes")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (ms)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "plot_kruskal.png"), dpi=150)
    plt.close()

    # --- Combined ---
    plt.figure(figsize=(7, 5))
    plt.plot(sizes, p_times,  "D-", color=PRIM_COLOR,    linewidth=2, markersize=6, label="Prim")
    plt.plot(sizes, k_times,  "o-", color=KRUSKAL_COLOR, linewidth=2, markersize=6, label="Kruskal")
    plt.title("Prim vs Kruskal – Execution Time vs Number of Nodes")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (ms)")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "plot_combined.png"), dpi=150)
    plt.close()

    # --- Speedup ratio (Kruskal / Prim) ---
    ratio = [k / p if p > 0 else 1.0 for k, p in zip(k_times, p_times)]
    plt.figure(figsize=(7, 5))
    plt.plot(sizes, ratio, "^-", color=RATIO_COLOR, linewidth=2, markersize=6)
    plt.axhline(y=1.0, color="gray", linestyle="--", linewidth=1, label="Equal speed (ratio = 1)")
    plt.title("Speedup Ratio: Kruskal Time / Prim Time")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Ratio  (> 1  →  Kruskal is slower)")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "plot_ratio.png"), dpi=150)
    plt.close()

    print(f"\nAll plots saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    demo()
    sizes, k_times, p_times = run_analysis()
    make_plots(sizes, k_times, p_times)