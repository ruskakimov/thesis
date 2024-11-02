import networkx as nx

def generate_directed_cycle_graph(n):
    """Generate a directed cycle graph with n vertices."""
    G = nx.DiGraph()
    
    G.add_nodes_from(range(n))

    for i in range(n):
        G.add_edge(i, (i + 1) % n)

    return G
