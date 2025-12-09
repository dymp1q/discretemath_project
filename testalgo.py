def is_planar_euler(graph: dict) -> bool:
    """
    Перевірка умови m <= 3n - 6.
    """
    n = len(graph)
    edge_count = 0
    for v in graph:
        edge_count += len(graph[v])
    m = edge_count // 2

    if n < 3:
        return True

    return m <= 3 * n - 6


def is_maximal_by_euler(graph: dict) -> bool:
    """
    Перевірка, що m = 3n - 6.
    """
    n = len(graph)
    edge_count = 0
    for v in graph:
        edge_count += len(graph[v])
    m = edge_count // 2

    if n < 3:
        return True

    return m == 3 * n - 6


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
    Жадібний пошук максимального планарного підграфа.
    """
    planar = make_empty_copy(original)
    all_edges = edges_of(original)
    all_edges.sort()

    for (u, v) in all_edges:
        if is_maximal_by_euler(planar):
            break

        add_edge(planar, u, v)

        if not is_planar_euler(planar):
            remove_edge(planar, u, v)

    return planar
