'''Знаходження максимального планарного підграфу'''

import argparse
import matplotlib.pyplot as plt
import networkx as nx


def UI_read() -> dict | bool:
    '''
    Функція запису вхідного графу.
    Варіанти запису:
    1)Файл(graph.txt -> 0 1
                        1 2)
    2)List([[1,2],[4,1],[1,3]])
    3)Matrix(0,1,0;1,0,1;0,0,1)
    4)Input(вручну вписувати: 1 0
                              2 0)
    '''
    consol_input = argparse.ArgumentParser(
        description=(
            "Graph input reader:\n"
            "- file   : provide filename, e.g., data.txt\n"
            "- list   : provide list, e.g., [[1,2],[4,1],[1,3]]\n"
            "- matrix : provide matrix, e.g., 0,1,0;1,0,1;0,0,1\n"
            "- input  : manual input via console"
        ))
    consol_input.add_argument("mode", nargs="?", default="input",
                               help="file/list/matrix/input (default=input)")
    consol_input.add_argument("data", nargs="?", default=None,
                               help="graph data or filename (optional with input mode)")
    consol_result = consol_input.parse_args()
    mode = consol_result.mode
    data = consol_result.data

    if mode == "input":
        return graph_input()

    graph = {}
    try:
        match mode:
            case 'file':
                if not data:
                    print("Не вказано файл для читання.")
                    return False
                with open(data, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip().split(',')
                        top_1 = int(line[0])
                        top_2 = int(line[1])
                        graph.setdefault(top_1, []).append(top_2)
                        graph.setdefault(top_2, []).append(top_1)
                return graph
            case 'list':
                if not data:
                    print("Не вказано список для читання.")
                    return False
                data = eval(data)
                count_of_tops = sorted(set([num for edge in data for num in edge]))
                for key in count_of_tops:
                    graph[key] = []
                for top_1, top_2 in data:
                    graph[top_1].append(top_2)
                    graph[top_2].append(top_1)
                return graph
            case 'matrix':
                if not data:
                    print("Не вказано матрицю для читання.")
                    return False
                data = data.split(';')
                data = [part.split(',') for part in data]
                for i in range(1, len(data)+1):
                    graph[i] = []
                for i in range(len(data)):
                    for j in range(len(data[i])):
                        if data[i][j] == '1':
                            graph[i + 1].append(j + 1)
                return graph
            case _:
                print("Невідомий режим вводу.")
                return False
    except Exception as e:
        print("Помилка при читанні графа:", e)
        return False

def graph_input(directed=False):
    '''
    Функція для записування через input
    '''
    adjacency_dict = {}

    while True:
        line = input("Ребро (u v) або 'stop' якщо ввели всі точки:").strip()
        if line == 'stop':
            break

        parts = line.split()
        if len(parts) == 2:
            try:
                u = int(parts[0])
                v = int(parts[1])
            except ValueError:
                u = parts[0]
                v = parts[1]

            if u not in adjacency_dict:
                adjacency_dict[u] = set()
            adjacency_dict[u].add(v)

            if not directed:
                if v not in adjacency_dict:
                    adjacency_dict[v] = set()
                adjacency_dict[v].add(u)

            if v not in adjacency_dict:
                adjacency_dict[v] = set()
        else:
            print("Некоректний ввід")
            continue

    final_graph = {node: list(neighbours) for node, neighbours in adjacency_dict.items()}
    return final_graph

    
def add_vertex(graph, v):
    """
    Функція яка додає вершину
    """
    if v not in graph:
        graph[v] = []

def remove_vertex(graph, v):
    """
    Функція яка видаляє вершину
    """
    if v in graph:
        del graph[v]
    for u in graph:
        if v in graph[u]:
            graph[u].remove(v)

def input_graph_visualisation(graph: dict):
    '''
    Друкує вхідний граф у форматі "u -> v"
    '''
    printed = set()
    for u in sorted(graph):
        for v in sorted(graph[u]):
            edge = tuple(sorted((u, v)))
            if edge not in printed:
                printed.add(edge)
                print(f"{u} -> {v}")

def planar_graph_visualisation(planar_graph: list):
    '''
    Приймає список ребер (parent, child) і друкує їх у форматі "u -> v".
    '''
    for parent, child in planar_graph:
        print(f"{parent} -> {child}")

def check_planarity(graph: dict | list) -> bool:
    """
    Перевірка планарності графа (dict або список ребер).
    Використовується:
    - Ейлерова межа: E <= 3V - 6
    - K5 (5 вершин, 10 ребер)
    - K3,3 (6 вершин, 9 ребер, двочастковість)
    """
    vertices = set()
    edges = set()

    if isinstance(graph, list):
        for u, v in graph:
            vertices.add(u)
            vertices.add(v)
            edges.add(tuple(sorted((u, v))))
    elif isinstance(graph, dict):
        for u, nbrs in graph.items():
            vertices.add(u)
            for v in nbrs:
                vertices.add(v)
                edges.add(tuple(sorted((u, v))))
    else:
        raise TypeError("Граф повинен бути dict або list.")

    V = len(vertices)
    E = len(edges)

    # Ейлерова межа
    if V >= 3 and E > 3 * V - 6:
        return False

    verts = list(vertices)
    n = len(verts)

    # Перевірка K5
    if n >= 5:
        for i1 in range(n):
            for i2 in range(i1+1, n):
                for i3 in range(i2+1, n):
                    for i4 in range(i3+1, n):
                        for i5 in range(i4+1, n):
                            nodes5 = [verts[i1], verts[i2], verts[i3], verts[i4], verts[i5]]
                            count = 0
                            for a in range(5):
                                for b in range(a+1, 5):
                                    if tuple(sorted((nodes5[a], nodes5[b]))) in edges:
                                        count += 1
                            if count == 10:
                                return False

    # Перевірка K3,3
    if n >= 6:
        for i1 in range(n):
            for i2 in range(i1+1, n):
                for i3 in range(i2+1, n):
                    for i4 in range(i3+1, n):
                        for i5 in range(i4+1, n):
                            for i6 in range(i5+1, n):
                                nodes6 = [verts[i1], verts[i2], verts[i3], verts[i4], verts[i5], verts[i6]]
                                # Перебираємо усі розбиття 3+3
                                for p1 in range(6):
                                    for p2 in range(p1+1, 6):
                                        for p3 in range(p2+1, 6):
                                            left = [nodes6[p1], nodes6[p2], nodes6[p3]]
                                            right = [x for x in nodes6 if x not in left]
                                            count = 0
                                            for a in left:
                                                for b in right:
                                                    if tuple(sorted((a,b))) in edges:
                                                        count += 1
                                            if count == 9:
                                                return False
    return True

def edges_of(graph: dict) -> list[tuple]:
    """
    Список ребер (u, v), u < v.
    """
    edges = []
    seen = set()

    for u in graph:
        for v in graph[u]:
            if u == v:
                continue
            if u < v:
                edge = (u, v)
            else:
                edge = (v, u)
            if edge not in seen:
                seen.add(edge)
                edges.append(edge)

    return edges


def make_empty_copy(original: dict) -> dict:
    """
    Копія графа без ребер.
    """
    new_graph = {}
    for v in original:
        new_graph[v] = set()
    return new_graph


def add_edge(graph: dict, u, v) -> None:
    '''
    Функція яка додає ребро
    '''
    if u not in graph:
        graph[u] = set()
    if v not in graph:
        graph[v] = set()
    graph[u].add(v)
    graph[v].add(u)


def remove_edge(graph: dict, u, v) -> None:
    '''
    Функція яка видаляє ребро
    '''
    if u in graph and v in graph[u]:
        graph[u].remove(v)
    if v in graph and u in graph[v]:
        graph[v].remove(u)


def maximal_planar_subgraph(original: dict) -> dict:
    """
    Жадібний пошук максимального планарного підграфа.
    Додає по одному ребру і перевіряє на планарність.
    """
    planar = make_empty_copy(original)
    all_edges = edges_of(original)
    all_edges.sort()

    for (u, v) in all_edges:
        add_edge(planar, u, v)

        if not check_planarity(planar):
            remove_edge(planar, u, v)

    return planar
    
def write_graph_to_file_uv(filepath: str, graph: dict, directed: bool = False):
    """
    Записує максимальний планарний граф в файл який напише користувач
    """

    edges_to_write = []
    seen_edges = set()

    for u, neighbours in graph.items():
        for v in neighbours:
            if directed:
                edges_to_write.append(f"{u} {v}")
            else:
                edge = tuple(sorted((u, v)))
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    edges_to_write.append(f"{u} {v}")

    with open(filepath, "w", encoding="utf-8") as f:
        for edge_line in edges_to_write:
            f.write(edge_line + "\n")

    print(f"Graph is written into the file '{filepath}' in format u v.")

def planar_graph_visual(edges: dict[int, list[int]]) -> None | bool:   # draws a graph, only if dict -> planar
    '''
    Перевіряє чи граф який пройшов алгоритм справді планарний, і якщо так то малює графік за допмогою matplotlib & networkx
    '''
    Graph_planar = nx.Graph()
    planar_list = []
    for top_1 in edges:              # makes list of ribs
        for top_2 in edges[top_1]:
            planar_list.append((top_1, top_2))
    Graph_planar.add_edges_from(planar_list)
    try:
        pos = nx.planar_layout(Graph_planar) # makes coord for each point as planar graph
    except nx.NetworkXException: # if graph not planar
        return False # if dict not planar 
    nx.draw(
        Graph_planar,
        pos,
        with_labels=True,
        node_color='skyblue',
        node_size=800,
        font_size=12
    )

    plt.show()


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    graph = UI_read()  # читає граф через argparse або input

    if graph is False:
        print('Введені дані через argparse - неправильні')
        exit()

    # Будуємо максимальний планарний підграф
    planar = maximal_planar_subgraph(graph)

    # Запис у файл
    filepath = input('Введіть назву файлу для запису (наприклад result.txt): ')
    write_graph_to_file_uv(filepath, planar)

    if planar_graph_visual(planar) is False:
        print("Граф не є планарним для візуалізації.")
    else: 
        planar_graph_visual(planar)
