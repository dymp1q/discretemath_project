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

print(read_graph("test_undirected.txt"))
# discretemath_project
Проект з дискретної математики на тему "Знаходження максимального планарного підграфу"
