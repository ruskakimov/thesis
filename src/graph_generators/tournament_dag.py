import networkx as nx

def generate_tournament_dag(n):
    """Generate a Tournament DAG, which is a complete graph with oriented edges without cycles."""
    G = nx.DiGraph()

    G.add_nodes_from(range(n))

    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j)

    return G
