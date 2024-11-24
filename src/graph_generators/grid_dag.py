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

def generate_cube_dag(n):
    """Generate a directed acyclic graph (DAG) with n^3 vertices in a cube."""
    G = nx.DiGraph()
    
    G.add_nodes_from(range(n ** 3))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                u = i * n ** 2 + j * n + k

                # Add down edge
                if i < n - 1:
                    v = (i + 1) * n ** 2 + j * n + k
                    G.add_edge(u, v)

                # Add right edge
                if j < n - 1:
                    v = i * n ** 2 + (j + 1) * n + k
                    G.add_edge(u, v)

                # Add back edge
                if k < n - 1:
                    v = i * n ** 2 + j * n + k + 1
                    G.add_edge(u, v)

    return G

def generate_4d_grid_dag(n):
    """Generate a directed acyclic graph (DAG) with n^4 vertices in a 4D grid."""
    G = nx.DiGraph()
    
    G.add_nodes_from(range(n ** 4))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    u = i * n ** 3 + j * n ** 2 + k * n + l

                    # Add down edge
                    if i < n - 1:
                        v = (i + 1) * n ** 3 + j * n ** 2 + k * n + l
                        G.add_edge(u, v)

                    # Add right edge
                    if j < n - 1:
                        v = i * n ** 3 + (j + 1) * n ** 2 + k * n + l
                        G.add_edge(u, v)

                    # Add back edge
                    if k < n - 1:
                        v = i * n ** 3 + j * n ** 2 + (k + 1) * n + l
                        G.add_edge(u, v)

                    # Add up edge
                    if l < n - 1:
                        v = i * n ** 3 + j * n ** 2 + k * n + l + 1
                        G.add_edge(u, v)

    return G