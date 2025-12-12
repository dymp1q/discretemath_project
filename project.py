'''Знаходження максимального планарного підграфу'''

import argparse
import matplotlib.pyplot as plt
import networkx as nx


def UI_read() -> dict | bool:
    '''
    reads 3 types of input into the console:
    - file
    - list
    - matrix
    output: dictionary
    if there is an error in the format, returns a bool value - False
    '''
    consol_input = argparse.ArgumentParser(description=( # my command --help, call samll instruction
        "Graph input reader:\n"
        "- file   : provide filename, e.g., data.txt\n"
        "- list   : provide list, e.g., [[1,2][4,1][1,3][3,2][2,4][4,3]]\n"
        "- matrix : provide matrix, e.g., 0,1,0;1,0,1;0,0,1"
    ))
    consol_input.add_argument("mode") # adds mode argument
    consol_input.add_argument("data") # adds data argument
    consol_result = consol_input.parse_args()
    mode = consol_result.mode
    data = consol_result.data
    print('================= Вибір =================')
    print('       1. Йти за алгоритмом Argparse')
    print('       2. Вести дані в Input')
    choise = input('Введіть 1 або 2: ')
    if choise == '2':
        return graph_input()
    graph = {}
    try:
        match mode:
            case 'file':
                with open(data, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip().split(',')
                        top_1 = int(line[0])
                        top_2 = int(line[1])
                        graph.setdefault(top_1, []).append(top_2)
                        graph.setdefault(top_2, []).append(top_1)
                print(graph)
                return graph
            case 'list':
                data = eval(data)
                count_of_tops = sorted(set([num for edge in data for num in edge])) # sorted list of vertices
                for key in count_of_tops:       # creates list for each vertice
                    graph[key] = []
                for top_1, top_2 in data:          # makes dict with reverse conection
                    graph[top_1].append(top_2)     # if A has B -> B has A
                    graph[top_2].append(top_1)
                return graph
            case 'matrix':
                data = data.split(';')
                data = [part.split(',') for part in data]
                for i in range(1,len(data)):
                    graph[i] = []
                for i in range(len(data)):              # for a row in matrix
                    for j in range(len(data[i])):       # for a num in each row
                        if data[i][j] == '1':           # if num has connecion 
                            graph[i + 1].append(j + 1)  # append num to dict
                return graph
            case _:
                return False
    except:                     # if any other porblem went off
        return False

def graph_input(directed=False):
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
    Adds a new vertex v to the graph.
    Does nothing if the vertex already exists.

    graph : dict — graph in the form {vertex: [neighbors]}
    v : any — the vertex to add
    """
    if v not in graph:
        graph[v] = []

def remove_vertex(graph, v):
    """
    Removes vertex v from the graph.
    Also removes all edges connected to this vertex.
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

def check_planarity(graph) -> bool:
    """
    check planarity
    """
    vertices = set()
    edges = set()
    if isinstance(graph, dict):
        for u, nbrs in graph.items():
            vertices.add(u)
            for v in nbrs:
                vertices.add(v)
                if u == v:
                    continue
                a, b = (u, v) if u <= v else (v, u)
                edges.add((a, b))
    else:
        for pair in graph:
            if not pair:
                continue
            u, v = pair
            vertices.add(u)
            vertices.add(v)
            if u == v:
                continue
            a, b = (u, v) if u <= v else (v, u)
            edges.add((a, b))

    V = len(vertices)
    E = len(edges)

    if V >= 3 and E > 3 * V - 6:
        return False

    verts = list(vertices)

    def combinations(lst, k):
        n = len(lst)
        if k > n:
            return
        idx = list(range(k))
        while True:
            yield [lst[i] for i in idx]

            for i in range(k - 1, -1, -1):
                if idx[i] != i + n - k:
                    break
            else:
                return
            idx[i] += 1
            for j in range(i + 1, k):
                idx[j] = idx[j - 1] + 1

    edges_set = edges
    def induced_edge_count(subset):
        sset = set(subset)
        cnt = 0
        for (u, v) in edges_set:
            if u in sset and v in sset:
                cnt += 1
        return cnt

    def is_bipartite_subset(subset):
        sset = set(subset)

        nbrs = {v: [] for v in subset}
        for (u, v) in edges_set:
            if u in sset and v in sset:
                nbrs[u].append(v)
                nbrs[v].append(u)

        color = {}
        for start in subset:
            if start in color:
                continue

            queue = [start]
            qi = 0
            color[start] = 0
            while qi < len(queue):
                u = queue[qi]; qi += 1
                for w in nbrs[u]:
                    if w not in color:
                        color[w] = 1 - color[u]
                        queue.append(w)
                    elif color[w] == color[u]:
                        return False
        return True

    if V >= 5:
        for comb in combinations(verts, 5):
            if induced_edge_count(comb) == 10:
                return False

    if V >= 6:
        for comb in combinations(verts, 6):
            if induced_edge_count(comb) == 9 and is_bipartite_subset(comb):
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
    if u not in graph:
        graph[u] = set()
    if v not in graph:
        graph[v] = set()
    graph[u].add(v)
    graph[v].add(u)


def remove_edge(graph: dict, u, v) -> None:
    if u in graph and v in graph[u]:
        graph[u].remove(v)
    if v in graph and u in graph[v]:
        graph[v].remove(u)


def maximal_planar_subgraph(original: dict) -> dict:
    """
    Жадібний пошук максимального планарного підграфа з перевіркою на K3,3.
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
    Writes a graph (adjacency dictionary) to a file in the format of a list of edges (u v),
    where u and v are separated by a space.

    For an undirected graph (directed=False), each edge is written only once.

    Args:
        filepath: Path to the file for writing.
        graph: Adjacency dictionary {vertex: [neighbors]}.
        directed: Whether the graph is directed.
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
    Visualizes planar graph by converting variable edges (adjacency dict)
    into list of tuples, where each tuple is a pair like A-B
    + planar check, if not planar, return bool variable - False
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
    else: planar_graph_visual(planar)
