import itertools
import networkx as nx

def generate_all_dags(n=3):
    nodes = list(range(n))
    all_possible_edges = [(u, v) for u in nodes for v in nodes if u != v]  # Allow any direction
    dags = set()  # Use a set to avoid duplicate isomorphic graphs
    
    for edge_subset in itertools.chain.from_iterable(itertools.combinations(all_possible_edges, r) for r in range(len(all_possible_edges) + 1)):
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edge_subset)
        
        if nx.is_directed_acyclic_graph(G):  # Ensure the graph is a DAG
            dags.add(frozenset(edge_subset))  # Use a hashable form to store unique DAGs
    
    return dags

# Expected counts from OEIS A003024
correct_counts = [1, 1, 3, 25, 543, 29281, 3781503, 1138779265, 783702329343]

# Generate all DAGs for a small test case

for n in range(7):
    dags = generate_all_dags(n)
    print(f"Generated {len(dags)} DAGs with {n} nodes.")
    print(f"Matches {correct_counts[n]}:", len(dags) == correct_counts[n])
