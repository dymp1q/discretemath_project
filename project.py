'''Знаходження максимального планарного підграфу'''

import argparse

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

def check_planarity(graph: dict | list, F = int | None=None) -> bool:
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

