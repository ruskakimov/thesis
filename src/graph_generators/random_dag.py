import networkx as nx
import random

def random_dag_with_density(num_nodes, edge_density=100):
    # Initialize directed graph
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))

    # Maximum possible edges in a DAG with num_nodes
    max_edges = num_nodes * (num_nodes - 1) // 2

    # Calculate the desired number of edges based on edge density percentage
    num_edges = int((edge_density / 100) * max_edges)

    # Generate all possible edges respecting the acyclic property
    possible_edges = [(i, j) for i in range(num_nodes) for j in range(i + 1, num_nodes)]

    # Randomly select the desired number of edges
    selected_edges = random.sample(possible_edges, num_edges)
    G.add_edges_from(selected_edges)

    return G
