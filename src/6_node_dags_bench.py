import sys
import ast
from pathlib import Path
import networkx as nx
from pysat.solvers import Solver
from helpers import T
from encoders import encode_2UBE

def all_dags(n):
    with open(f'./src/all_dags_with_{n}_nodes.txt', 'r') as file:
        for line in file:
            edges = ast.literal_eval(line.strip())
            
            G = nx.Graph()
            G.add_nodes_from(range(n))
            G.add_edges_from(edges)
            
            yield G


def solve(cnf):
    with Solver(name='Cadical103', bootstrap_with=cnf) as solver:
        result = solver.solve()
        model = solver.get_model() if result else None
        return (result, model)

RUNS = 1

print('n,m,time(s),sat')

i = 0
for G in all_dags(5):
    i += 1
    print(f"Working on graph {i}", file=sys.stderr)
    
    cnf = encode_2UBE(G)

    times = []
    result, _ = solve(cnf)

    for j in range(RUNS):
        T.start('solve')
        solve(cnf)
        times.append(T.stop('solve'))
    
    mean_solve_time = sum(times) / len(times)

    n = G.number_of_nodes()
    m = G.number_of_edges()

    print(f'{n},{m},{mean_solve_time:.9f},{result}')
