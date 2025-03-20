import time
import sys
import ast
from pathlib import Path
import networkx as nx
from pysat.solvers import Solver
from helpers import T
from encoders import encode_2UBE, encode_book_embedding, encode_upward_book_embedding

def all_dags(n):
    with open(f'./src/all_dags_with_{n}_nodes.txt', 'r') as file:
        for line in file:
            edges = ast.literal_eval(line.strip())
            
            G = nx.Graph()
            G.add_nodes_from(range(n))
            G.add_edges_from(edges)
            
            yield G


def solve(cnf):
    with Solver(name='Lingeling', bootstrap_with=cnf) as solver:
        start = time.perf_counter()
        result = solver.solve()
        elapsed_time = time.perf_counter() - start
        # model = solver.get_model() if result else None
        return (elapsed_time, result)

RUNS = 1

print('n,m,time(s),sat,median_time(s)')

i = 0
for G in all_dags(6):
    i += 1
    print(f"Working on graph {i}", file=sys.stderr)
    
    # cnf = encode_2UBE(G)
    cnf = encode_upward_book_embedding(G, 3)

    times = []
    _, result = solve(cnf)

    for j in range(RUNS):
        t, result = solve(cnf)
        times.append(t)
    
    mean_solve_time = sum(times) / len(times)
    times.sort()
    median_solve_time = times[len(times) // 2]

    n = G.number_of_nodes()
    m = G.number_of_edges()

    print(f'{n},{m},{mean_solve_time:.9f},{result},{median_solve_time:.9f}')
