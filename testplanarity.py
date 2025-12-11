def read_graph_txt(path: str, directed: bool = False) -> dict[int, list[int]]:
    """
    Зчитує граф із текстового файлу формату:
        u,v
    де u → v — орієнтоване ребро.

    Якщо directed=False (за замовчуванням),
    ребро додається в обидві сторони, тобто граф вважається неорієнтованим.

    Якщо directed=True — ребро додається лише як (u → v).

    Параметри:
        path : str
            шлях до файлу
        directed : bool
            чи орієнтований граф (True = орієнтований)

    Повертає:
        dict[int, list[int]] — словник суміжності

    Формат файлу:
        0,1
        1,2
        2,3
    """
    graph = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            u, v = line.strip().split(",")
            u, v = int(u), int(v)
            graph.setdefault(u, []).append(v)
            if not directed:
                graph.setdefault(v, []).append(u)
            else:
                graph.setdefault(v, [])
    return graph

# g = read_graph_txt("k24.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

# g = read_graph_txt("k33.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

# g = read_graph_txt("k4.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

# g = read_graph_txt("k5.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

# g = read_graph_txt("square.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

# g = read_graph_txt("tree.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)


def generate_grid_to_file(rows, cols, filename):
    """
    Генерує прямокутний ґратковий граф (grid graph) розміром rows × cols
    та записує його до файлу у форматі списку ребер "u,v".

    Кожна вершина має номер:
        v = r * cols + c
    де:
        r — номер рядка (0 ≤ r < rows)
        c — номер стовпця (0 ≤ c < cols)

    Ребра додаються між:
        • вершинами, що стоять поруч у рядку (праворуч)
        • вершинами, що стоять поруч у стовпці (внизу)

    Тобто граф є декартовим добутком P_rows × P_cols — класичний планарний grid graph.

    Параметри:
        rows : int
            кількість рядків ґратки
        cols : int
            кількість стовпців ґратки
        filename : str
            шлях до файлу, куди буде записано ребра

    Формат вихідного файлу:
        Кожен рядок містить одне ребро у вигляді:
            u,v
        Наприклад:
            0,1
            0,4
            1,2
            1,5
    """
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

# generate_grid_to_file(6, 6, "grid6x6.txt")
# g = read_graph_txt("grid6x6.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

def generate_random_graph(n, p, filename):
    """
    Генерує випадковий неорієнтований граф G(n, p)
    та записує його до файлу у форматі ребер "u,v".

    Кожне можливе ребро між вершинами u та v (u < v)
    додається з імовірністю p.

    Параметри:
        n : int
            Кількість вершин графа (вершини від 0 до n-1)
        p : float
            Імовірність появи кожного ребра (0 ≤ p ≤ 1)
        filename : str
            Назва файлу, у який буде записано згенерований граф

    Формат вихідного файлу:
        Кожен рядок містить одне ребро у вигляді:
            u,v
        Наприклад:
            0,3
            1,4
            2,3
    """
    with open(filename, "w") as f:
        for u in range(n):
            for v in range(u+1, n):
                if random.random() < p:
                    f.write(f"{u},{v}\n")

# generate_random_graph(10, 0.4, "rand_test.txt")
# g = read_graph_txt("rand_test.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)
