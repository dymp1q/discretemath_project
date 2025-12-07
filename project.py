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
    if choise == 2:
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
def graph_input(directed = False):
    """
    This function reads graps
    """

    adjacency_dict = {}

    while True:
        line = input("Ребро (u v) або 'stop' якщо ввели всі точки:").strip()
        if line == 'stop':
            return adjacency_dict
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

    >>> g = {0: [1], 1: [0]}
    >>> add_vertex(g, 2)
    >>> g
    {0: [1], 1: [0], 2: []}

    >>> add_vertex(g, 1)
    >>> g
    {0: [1], 1: [0], 2: []}
    """
    if v not in graph:
        graph[v] = []

def remove_vertex(graph, v):
    """
    Removes vertex v from the graph.
    Also removes all edges connected to this vertex.

    graph : dict — graph in the form {vertex: [neighbors]}
    v : vertex to remove

    >>> g = {0: [1, 2], 1: [0], 2: [0]}
    >>> remove_vertex(g, 2)
    >>> g
    {0: [1], 1: [0]}

    >>> remove_vertex(g, 5)
    >>> g
    {0: [1], 1: [0]}
    """
    if v in graph:
        del graph[v]
    for u in graph:
        if v in graph[u]:
            graph[u].remove(v)

def add_edge(graph, u, v, directed = False):
    """
    Adds an edge between vertices u and v.
    If directed=False, the edge is added in both directions (undirected graph).
    If the vertices do not exist, they are created automatically.

    graph : dict — graph in the form {vertex: [neighbors]}
    u, v : vertices to connect
    directed : bool — whether the graph is directed

    >>> g = {0: [1], 1: [0], 2: []}
    >>> add_edge(g, 2, 0)
    >>> g
    {0: [1, 2], 1: [0], 2: [0]}

    >>> add_edge(g, 2, 1, directed = True)
    >>> g
    {0: [1, 2], 1: [0], 2: [0, 1]}

    >>> add_edge(g, 2, 0)
    >>> g
    {0: [1, 2], 1: [0], 2: [0, 1]}
    """
    if u not in graph:
        graph[u] = []
    if v not in graph[u]:
        graph[u].append(v)
    
    if not directed:
        if v not in graph:
            graph[v] = []
        if u not in graph[v]:
            graph[v].append(u)

def remove_edge(graph, u , v, directed = False):
    """
    Removes the edge between vertices u and v.
    If directed=False, removes the edge in both directions.
    Does nothing if the edge does not exist.

    graph : dict — graph in the form {vertex: [neighbors]}
    u, v : vertices whose edge is removed
    directed : bool — whether the graph is directed

    >>> g = {0: [1, 2], 1: [0], 2: [0, 1]}
    >>> remove_edge(g, 2, 1, directed=True)
    >>> g
    {0: [1, 2], 1: [0], 2: [0]}

    >>> remove_edge(g, 0, 2)
    >>> g
    {0: [1], 1: [0], 2: []}

    >>> remove_edge(g, 5, 6)
    >>> g
    {0: [1], 1: [0], 2: []}
    """
    if u in graph and v in graph[u]:
        graph[u].remove(v)
    if not directed:
        if v in graph and u in graph[v]:
            graph[v].remove(u)

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

def edges_to_adj_dict(edges: list[tuple[int, int]], vertices: list[int]) -> dict[int, list[int]]:
    """
    Зі списку ребер (u, v) будує неорієнтований граф
    у вигляді словника: вершина -> список сусідів.
    """
    planar_graph = {}

    for v in vertices:
        planar_graph[v] = []

    for u, v in edges:
        if v not in planar_graph[u]:
            planar_graph[u].append(v)
        if u not in planar_graph[v]:
            planar_graph[v].append(u)

    for v in planar_graph:
        planar_graph[v].sort()

    return planar_graph

def dfs_tree(graph: dict):
    '''
    Обхід графа в глибину (DFs).
    Повертає список ребер DFS-дерева у форматі (parent, child).

    >>> g = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
    >>> dfs_tree(g)
    [(0, 1), (1, 3), (0, 2)]
    '''
    if not graph:
        return []
    # if check_planarity(graph, faces):
    #     print(f'Граф - {graph}, який ви задали вже є планарним.')
    #     print('Граф який ви ввели:')
    #     input_graph_visualisation(graph)

    else:
        start = min(graph)

        visited = set()
        stack = [start]
        parent = {}
        edges = []

        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            if u in parent:
                edges.append((parent[u], u))
            neighbors = sorted(graph.get(u, []))
            for v in reversed(neighbors):
                if v not in visited and v not in parent:
                    parent[v] = u
                    stack.append(v)
        return edges

# print(dfs_tree({0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}))
# [(0, 1), (1, 3), (0, 2)]

def get_all_edges(graph: dict) -> list:
    """
    Повертає список усіх неорієнтованих ребер у вигляді (u, v) з u < v.
    """
    edges = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            if u == v:
                continue
            # робимо порядок (менший, більший), щоб не дублювати ребра
            if u < v:
                edge = (u, v)
            else: edge = (v, u)
            edges.add(edge)
    return sorted(edges)

def build_maximal_planar_subgraph(graph: dict) -> dict[int, list[int]]:
    """
    Будує максимальний планарний підграф:
    1) Беремо DFS-дерево (воно точно планарне).
    2) Перебираємо решту ребер і додаємо лише ті, які не псують планарність.

    Повертає список ребер планарного підграфу.
    """
    if not graph:
        return {}
    
    else:
        vertices = sorted(graph.keys())

        tree_edges = dfs_tree(graph)
        planar_edges = set(tree_edges)

        all_edges = get_all_edges(graph)

        for u, v in all_edges:
            if (u, v) in planar_edges or (v, u) in planar_edges:
                continue

            candidate_edges = list(planar_edges) + [(u, v)]

            if check_planarity(candidate_edges):
                planar_edges.add((u, v))

            result_edges = sorted(planar_edges)

            planar_graph = edges_to_adj_dict(result_edges, vertices)

    return planar_graph
    
def bfs_tree(graph: dict):
    '''
    Обхід графа в ширину (BFS).
    Повертає список ребер BFS-дерева у форматі (parent, child).

    >>> g = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
    >>> bfs_tree(g)
    Граф який ви ввели:
    [(0, 1), (0, 2), (1, 3)]
    '''
    if not graph:
        return []

    # if check_planarity(graph, faces):
    #     print(f'Граф - {graph}, який ви задали вже є планарним.')
    #     print('Граф який ви ввели:')
    #     input_graph_visualisation(graph)
    #     return

    start = min(graph)

    visited = set()
    queue = [start]
    parent = {}
    edges = []

    while queue:
        u = queue.pop(0)

        if u in visited:
            continue
        visited.add(u)

        if u in parent:
            edges.append((parent[u], u))

        neighbors = sorted(graph.get(u, []))
        for v in neighbors:
            if v not in visited and v not in parent:
                parent[v] = u
                queue.append(v)
    return edges

def check_planarity(graph: dict | list, F = int | None) -> bool:
    '''
    Checks planarity of a graph.
    '''
    if isinstance(graph, list):
        edges = set()
        vertices = set()

        for u, v in graph:
            vertices.add(u)
            vertices.add(v)

            edges.add(tuple(sorted((u, v))))

        V = len(vertices)
        E = len(edges)

    elif isinstance(graph, dict):
        vertices = set(graph.keys())
        edges = set()

        for u in graph:
            for v in graph[u]:
                edge = tuple(sorted((u, v)))
                edges.add(edge)

        V = len(vertices)
        E = len(edges)

    else:
        raise TypeError("Граф повинен бути поданий або у формі dict або list.")

    if F is not None:
        if V - E + F != 2:
            return False

    if V >= 3:
        if E > 3 * V - 6:
            return False

    return True
    
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
    graph = UI_read()
    if graph == 'False':
        return 'Введені дані через argparse - неправильні'
    ...#main algorithm, return planar dict()

    
    filepath = input('Введіть назву файлу для запису: ')
    write_graph_to_file_uv(filepath, graph)
    planar_graph_visual(graph) # stops there, cz constanly shows separeted window with planar graph
    































