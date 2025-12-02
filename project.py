'''Знаходження максимального планарного підграфу'''

import argparse
import networkx as nx
import matplotlib.pyplot as plt

def planar_graph_visual(edges: dict[int, list]) -> None:
    '''
    Visualizes planar graph, by converting variable edges into list of typles, where each has a pair like A-B
    '''
    Graph_planar = nx.Graph()            # creates empty Graph, disoriented one
    planar_list = []
    for top_1 in edges:                          # dict -> list(pairs: (1,2),(3,1)...)
        for top_2 in edges[top_1]:
            planar_list.append((top_1, top_2))
    Graph_planar.add_edges_from(planar_list) # add list of ribs
    pos = nx.planar_layout(Graph_planar)     # adds each top its own coods by Fáry’s algorithm
    nx.draw(
        Graph_planar,
        pos,
        with_labels=True,
        node_color='skyblue',
        node_size=800,
        font_size=12
    )
    plt.show()
def graph_input(directed = False):
    """
    This function reads graps
    """

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

def dfs(graph: dict):
    '''
    Обхід графа в глибину (DFS).
    Повертає список ребер DFS-дерева у форматі (parent, child).

    >>> g = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
    >>> dfs(g)
    Граф який ви ввели:
    0 -> 1
    0 -> 2
    1 -> 3
    Найменший плананий граф:
    0 -> 1
    1 -> 3
    0 -> 2
    [(0, 1), (1, 3), (0, 2)]
    '''
    if not graph:
        return []
    if check_planarity(graph):
        print(f'Граф - {graph}, який ви задали вже є планарним.')
        print('Граф який ви ввели:')
        input_graph_visualisation(graph)

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
        print('Граф який ви ввели:')
        input_graph_visualisation(graph)
        print('Найменший плананий граф:')
        planar_graph_visualisation(edges)
        return edges

#print(dfs({0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}))

def bfs(graph: dict):
    '''
    Обхід графа в ширину (BFS).
    Повертає список ребер BFS-дерева у форматі (parent, child).

    >>> g = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
    >>> bfs(g)
    Граф який ви ввели:
    0 -> 1
    0 -> 2
    1 -> 3
    Найменший плананий граф (BFS):
    0 -> 1
    0 -> 2
    1 -> 3
    [(0, 1), (0, 2), (1, 3)]
    '''
    if not graph:
        return []

    if check_planarity(graph):
        print(f'Граф - {graph}, який ви задали вже є планарним.')
        print('Граф який ви ввели:')
        input_graph_visualisation(graph)
        return

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

    print('Граф який ви ввели:')
    input_graph_visualisation(graph)
    print('Найменший плананий граф (BFS):')
    planar_graph_visualisation(edges)

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

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

