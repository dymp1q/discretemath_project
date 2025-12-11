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

# g = read_graph_txt("k2,4.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

# g = read_graph_txt("k3,3.txt")
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


def generate_cycle_with_random_chords(n: int, num_chords: int, filename: str):
    """
    Генерує цикл C_n з випадковими хордами та записує граф у файл у форматі "u,v".

    Параметри:
        n : int
            Кількість вершин циклу (нумерація 0..n-1, n >= 3).
        num_chords : int
            Кількість додаткових ребер (хорд), що випадково додаються до циклу.
        filename : str
            Ім'я файлу для збереження графа.

    Опис:
        Спочатку будується планарний цикл C_n.
        Далі випадково додаються хорди, які:
        - не є ребрами циклу,
        - не дублюються,
        - не утворюють петель (u ≠ v).

        Отриманий граф зазвичай є непланарним.
    """

    edges = set()

    # Генеруємо цикл C_n
    for i in range(n):
        u = i
        v = (i + 1) % n
        edge = tuple(sorted((u, v)))
        edges.add(edge)

    # Генеруємо випадкові хорди
    while len(edges) < n + num_chords:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)

        # Забороняємо петлі
        if u == v:
            continue

        # Забороняємо ребра циклу
        if (v == (u + 1) % n) or (u == (v + 1) % n):
            continue

        chord = tuple(sorted((u, v)))

        if chord in edges:
            continue

        edges.add(chord)

    with open(filename, "w") as f:
        for (u, v) in sorted(edges):
            f.write(f"{u},{v}\n")


# generate_cycle_with_random_chords(6, 2, "cycle6_small.txt")
# g = read_graph_txt("cycle6_small.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

# generate_cycle_with_random_chords(20, 5, "cycle20_test.txt")
# g = read_graph_txt("cycle20_test.txt")
# result = build_maximal_planar_subgraph(g)
# print(result)

# generate_cycle_with_random_chords(200, 40, "cycle200_big.txt")
# g = read_graph_txt("200, 40, "cycle200_big.txt"")
# result = build_maximal_planar_subgraph(g)
# print(result)


def generate_random_graph(n, p, filename):
    """
    Генерує випадковий неорієнтований граф G(n, p) за моделлю Ердаша–Реньї
    та записує його у файл у форматі ребер "u,v".

    У моделі G(n, p) кожна з можливих пар вершин (u, v), де u < v,
    з’єднується ребром незалежно з імовірністю p.

    Параметри:
        n : int
            Кількість вершин графа. Вершини нумеруються від 0 до n-1.
        p : float
            Імовірність появи кожного ребра (0 ≤ p ≤ 1).
            Менші значення p відповідають розрідженим графам,
            більші — густим, часто непланарним графам.
        filename : str
            Назва файлу, у який буде записано згенерований граф.

    Формат вихідного файлу:
        Кожен рядок містить одне ребро у вигляді:
            u,v
        де u < v, оскільки граф є неорієнтованим.
    
    Зауваження:
        - При великих значеннях p граф швидко стає непланарним.
        - Для n ≥ 20 і p ≥ 0.3 більшість згенерованих графів є непланарними.
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
