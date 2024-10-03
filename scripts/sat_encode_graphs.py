from pathlib import Path
from utils.read_graph import read_all_graphs

cnf_dir = Path(__file__).resolve().parent.parent / 'graphs'

def sat_encode_graph(graph):
    pass

def write_cnf_to_file(num_vars, clauses, name):
    with open(cnf_dir / f'{name}.cnf', 'w') as file:
        file.write(f'p cnf {num_vars} {len(clauses)}\n')
        for clause in clauses:
            file.write(' '.join(map(str, clause)) + " 0\n")

graphs = read_all_graphs()

for graph in graphs:
    num_vars, clauses = sat_encode_graph(graph)
    write_cnf_to_file(num_vars, clauses, graph.name)
