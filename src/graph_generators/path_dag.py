import networkx as nx

def generate_path_dag(n):
    """Generate a directed acyclic graph (DAG) with n vertices in a path."""
    G = nx.DiGraph()
    
    G.add_nodes_from(range(n))

    for i in range(n - 1):
        G.add_edge(i, i + 1)

    return G
