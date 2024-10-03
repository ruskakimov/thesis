class Graph:
    def __init__(self, name, num_nodes, edges):
        self.name = name
        self.num_nodes = num_nodes
        self.edges = edges

    def __str__(self):
        return f"Graph(name={self.name}, num_nodes={self.num_nodes}, edges={self.edges})"

    def __repr__(self):
        return self.__str__()