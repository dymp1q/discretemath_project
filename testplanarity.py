def read_graph_txt(path: str) -> dict[int, list[int]]:
    graph = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            u, v = line.strip().split(",")
            u, v = int(u), int(v)
            graph.setdefault(u, []).append(v)
            graph.setdefault(v, []).append(u)
    return graph

# g = read_graph_txt("k4.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

# g = read_graph_txt("cycle_with_chord.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

# g = read_graph_txt("k33.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

def generate_grid_to_file(rows, cols, filename):
    with open(filename, "w") as f:
        for r in range(rows):
            for c in range(cols):
                v = r * cols + c
                if c + 1 < cols:
                    f.write(f"{v},{v+1}\n")
                if r + 1 < rows:
                    f.write(f"{v},{v+cols}\n")

# generate_grid_to_file(4, 4, "grid4x4.txt")
# g = read_graph_txt("grid4x4.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

def generate_random_graph(n, p, filename):
    with open(filename, "w") as f:
        for u in range(n):
            for v in range(u+1, n):
                if random.random() < p:
                    f.write(f"{u},{v}\n")

# generate_random_graph(10, 0.4, "rand_test.txt")
# g = read_graph_txt("rand_test.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)
