from pathlib import Path

class Graph:
    def __init__(self, name, num_nodes, edges):
        self.name = name
        self.num_nodes = num_nodes
        self.edges = edges

    def __str__(self):
        return f"Graph(name={self.name}, num_nodes={self.num_nodes}, edges={self.edges})"

    def __repr__(self):
        return self.__str__()
    
def read_graph(file_path):
    file_path = Path(file_path)

    num_nodes = None
    edges = []

    with file_path.open('r') as file:
        num_nodes = int(file.readline().strip())

        for line in file:
            u, v = map(int, line.strip().split())
            edges.append((u, v))

    return Graph(name=file_path.name.split('.')[0], num_nodes=num_nodes, edges=edges)
