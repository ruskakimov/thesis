from pathlib import Path
from pysat.solvers import Solver
from helpers import rome_graphs, write_cnf, T
from encoders import encode_graceful_labeling, decode_graceful_labeling, is_valid_graceful_labeling

def solve(cnf):
    with Solver(name='Maplesat', bootstrap_with=cnf) as solver:
        result = solver.solve()
        model = solver.get_model() if result else None
        return (result, model)

cnf_dir = Path(__file__).resolve().parent.parent / 'cnf'

def generate_cnfs(max_nodes):
    for G in rome_graphs():
        N = G.number_of_nodes()
        
        if N > max_nodes:
            continue
        
        T.start(G.name)
        cnf = encode_graceful_labeling(G)
        write_cnf(cnf, cnf_dir / 'rome_GL_SAT1' / f'gl_{G.name}.cnf')
        T.stop(G.name)
        print('-' * 30)

def test_encoding(nodes, max_cases):
    i = 1

    for G in rome_graphs():
        N = G.number_of_nodes()
        
        if N != nodes:
            continue

        if i > max_cases:
            break

        i += 1

        print(G.name)
        
        T.start('encode')
        cnf = encode_graceful_labeling(G)
        T.stop('encode')
        
        T.start('solve')
        result, solution = solve(cnf)
        T.stop('solve')
        
        print('SAT:', result)
        node_labels = decode_graceful_labeling(G, solution)
        print('Node labels:', node_labels)

        print('Correct GL:', is_valid_graceful_labeling(G, node_labels))
        print('-' * 30)

# test_encoding(nodes=30, max_cases=3)

generate_cnfs(10)