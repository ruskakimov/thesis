import networkx as nx

def generate_complete_binary_arborescence(levels):
    """Generate a Complete Binary Arborescence (DAG), which is a Complete Binary Tree with all edges pointing away from root."""
    G = nx.DiGraph()

    N = 2**levels - 1

    G.add_nodes_from(range(N))

    for i in range(N):
        G.add_edge(i, 2*i + 1)
        G.add_edge(i, 2*i + 2)
    
    return G
