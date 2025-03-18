import sys
import itertools
from pathlib import Path
import networkx as nx
from pysat.solvers import Solver
from helpers import T, write_cnf
from encoders import encode_2UBE

def generate_all_dags(n=3):
    nodes = list(range(n))
    all_possible_edges = [(u, v) for u in nodes for v in nodes if u != v]  # Allow any direction
    dag_hashes = set()  # Use a set to avoid duplicate isomorphic graphs
    count = 0
    
    for edge_subset in itertools.chain.from_iterable(itertools.combinations(all_possible_edges, r) for r in range(len(all_possible_edges) + 1)):
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edge_subset)
        
        if nx.is_directed_acyclic_graph(G):  # Ensure the graph is a DAG
            hash = frozenset(edge_subset)  # Use a hashable form to store unique DAGs
            if hash not in dag_hashes:
                print(f"{count / correct_counts[n] * 100}%", file=sys.stderr)
                dag_hashes.add(hash)
                count += 1
                print(G.edges())
    
    return dag_hashes

# Expected counts from OEIS A003024
correct_counts = [1, 1, 3, 25, 543, 29281, 3781503, 1138779265, 783702329343]

print('Done, generated graphs:', len(generate_all_dags(6)), file=sys.stderr)