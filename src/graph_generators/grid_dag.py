import networkx as nx

def generate_grid_dag(n, m):
    """Generate a directed acyclic graph (DAG) with n * m vertices in a grid."""
    G = nx.DiGraph()
    
    G.add_nodes_from(range(n * m))

    for i in range(n):
        for j in range(m):
            # Add down edge
            if i < n - 1:
                G.add_edge(i * m + j, (i + 1) * m + j)

            # Add right edge
            if j < m - 1:
                G.add_edge(i * m + j, i * m + j + 1)

    return G
