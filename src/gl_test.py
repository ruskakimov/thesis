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
    
for G in rome_graphs():
    N = G.number_of_nodes()
    
    # if N > 10:
    #     continue

    # print(G.name)
    
    T.start(G.name)
    cnf = encode_graceful_labeling(G)
    write_cnf(cnf, cnf_dir / 'rome_GL' / f'gl_{G.name}.cnf')
    T.stop(G.name)
    
    # result, solution = solve(cnf)
    # print('SAT:', result)
    
    # node_labels = decode_graceful_labeling(G, solution)
    # print('Node labels:', node_labels)

    # print('Correct GL:', is_valid_graceful_labeling(G, node_labels))
    print('-' * 30)
