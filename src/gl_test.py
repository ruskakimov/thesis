from pysat.solvers import Solver
from helpers import rome_graphs
from encoders import encode_graceful_labeling, decode_graceful_labeling, is_valid_graceful_labeling

def solve(cnf):
    with Solver(name='Maplesat', bootstrap_with=cnf) as solver:
        result = solver.solve()
        model = solver.get_model() if result else None
        return (result, model)
    
for G in rome_graphs():
    N = G.number_of_nodes()
    if N > 10:
        continue
    cnf = encode_graceful_labeling(G)
    result, solution = solve(cnf)
    
    node_labels = decode_graceful_labeling(G, solution)
    print(node_labels)

    print('Correct GL:', is_valid_graceful_labeling(G, node_labels))

    break