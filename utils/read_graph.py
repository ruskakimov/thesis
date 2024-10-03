from pathlib import Path

graphs_dir = Path(__file__).resolve().parent.parent / 'graphs'

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

def read_all_graphs():
    graphs = []

    for file_path in graphs_dir.iterdir():
        if file_path.is_file():
            graphs.append(read_graph(file_path))

    # Sort by name and number of nodes
    graphs.sort(key=lambda g: (g.name.split('_')[0], int(g.name.split('_')[1])))

    return graphs