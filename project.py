'''Знаходження максимального планарного підграфу'''

import argparse

def read_graph(filepath, directed = False):
    """This function reads graps
    """

    adjacency_dict = {}

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
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

        final_graph = {node: list(neighbours) for node, neighbours in adjacency_dict.items()}

        return final_graph

#print(read_graph("test_undirected.txt"))

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

def dfs_method(graph: dict):
    '''
    Обхід графа в глибину (DFS) без рекурсії.
    Повертає список ребер DFS-дерева у форматі (parent, child).

    Стартуємо з найменшої вершини (min(graph)).

    >>> g = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
    >>> dfs_method(g)
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
#print(dfs_method({0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}))

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
