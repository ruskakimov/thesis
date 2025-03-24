import time
import sys
import ast
import math
import os
from pathlib import Path
import networkx as nx
from pysat.solvers import Solver
from helpers import T
from encoders import encode_2UBE, encode_book_embedding, encode_upward_book_embedding

def dags(n):
    filepath = f'./PT/dags/n{n}_100_per_m.txt'
    if not os.path.exists(filepath):
        print(f"Warning: File {filepath} not found.", file=sys.stderr)
        return []
    
    with open(filepath, 'r') as file:
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
        return elapsed_time, result

RUNS = 1

def run_benchmarks():
    output_dir = Path("./PT/bench/")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for n in range(7, 21):  # n = 7 to 20
        for k in range(1, math.ceil(n / 2)):  # k = 1 to ceil(n/2)-1
            print(f"Working on n={n}, k={k}", file=sys.stderr)

            output_file = output_dir / f"n{n}_k{k}___{RUNS}_run_eq_m_bins.csv"
            
            with open(output_file, 'w') as f:
                f.write('n,m,time(s),sat,median_time(s)\n')
                
                i = 0
                for G in dags(n):
                    i += 1
                    
                    cnf = encode_upward_book_embedding(G, k)
                    
                    times = []
                    _, result = solve(cnf)
                    
                    for _ in range(RUNS):
                        t, result = solve(cnf)
                        times.append(t)
                    
                    mean_solve_time = sum(times) / len(times)
                    times.sort()
                    median_solve_time = times[len(times) // 2]
                    
                    n_nodes = G.number_of_nodes()
                    m_edges = G.number_of_edges()
                    
                    f.write(f'{n_nodes},{m_edges},{mean_solve_time:.9f},{result},{median_solve_time:.9f}\n')

if __name__ == "__main__":
    run_benchmarks()
