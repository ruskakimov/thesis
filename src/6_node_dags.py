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
    dags = []
    
    for edge_subset in itertools.chain.from_iterable(itertools.combinations(all_possible_edges, r) for r in range(len(all_possible_edges) + 1)):
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edge_subset)
        
        if nx.is_directed_acyclic_graph(G):  # Ensure the graph is a DAG
            hash = frozenset(edge_subset)  # Use a hashable form to store unique DAGs
            if hash not in dag_hashes:
                dag_hashes.add(hash)
                dags.append(G)
    
    return dags

# Expected counts from OEIS A003024
correct_counts = [1, 1, 3, 25, 543, 29281, 3781503, 1138779265, 783702329343]

def solve(cnf):
    with Solver(name='Maplesat', bootstrap_with=cnf) as solver:
        result = solver.solve()
        model = solver.get_model() if result else None
        return (result, model)

n = 5
dags = generate_all_dags(n)
print(f"Generated {len(dags)} DAGs with {n} nodes.", file=sys.stderr)
print(f"Matches {correct_counts[n]}:", len(dags) == correct_counts[n], file=sys.stderr)

i = 0

cnf_dir = Path(__file__).resolve().parent.parent / 'cnf'

print('n, m, time(s)')

for G in dags:
    i += 1
    print(f"Working on graph {i}", file=sys.stderr)

    # T.start(G.name)
    
    cnf = encode_2UBE(G)
    # write_cnf(cnf, cnf_dir / 'all_dags' / f'{G.name}.cnf')
    
    # T.stop(G.name)

    T.start('solve')
    solve(cnf)
    solve_time = T.stop('solve')

    n = G.number_of_nodes()
    m = G.number_of_edges()

    print(f'{n}, {m}, {solve_time:.9f}')

    # print('---')
