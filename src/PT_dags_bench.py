import time
import sys
import ast
import os
from pathlib import Path
import networkx as nx
from pysat.solvers import Solver
from helpers import T
from encoders import encode_upward_book_embedding

PER_M = 100
TIMEOUT_PER_DAG_SEC = 60 * 5
RUNS = 10

N_VALS = [10]
K_VALS = [1]

def dags(n):
    filepath = f'./PT/dags/n{n}_{PER_M}_per_m.txt'
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
        elapsed = time.perf_counter() - start
        return (elapsed, result)

def print_progress_bar(current, total, start_time, bar_length=40):
    percent = current / total
    filled = int(bar_length * percent)
    bar = '=' * filled + '-' * (bar_length - filled)
    elapsed = time.time() - start_time
    rate = current / elapsed if elapsed else 0
    remaining = (total - current) / rate if rate else 0
    sys.stderr.write(f'\r[{bar}] {current}/{total} ({percent:.1%}) ETA: {remaining:.1f}s')
    sys.stderr.flush()

def run_benchmarks():
    output_dir = Path("./PT/bench/")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for n in N_VALS:
        for k in K_VALS:
            print(f"\n\nWorking on n={n}, k={k}", file=sys.stderr)
            output_file = output_dir / f"n{n}_k{k}___{RUNS}_run_eq_m_bins.csv"
            print(f"Writing to {output_file}")
            start_time = time.time()

            max_m = n*(n-1)//2
            total_dags = (1+max_m)*PER_M
            
            with open(output_file, 'w') as f:
                f.write('n,m,time(s),sat,median_time(s)\n')
                
                i = 0
                for G in dags(n):
                    i += 1
                    print_progress_bar(i, total_dags, start_time)
                    
                    cnf = encode_upward_book_embedding(G, k)
                    
                    times = []
                    first_time, result = solve(cnf)
                    times.append(first_time)
                    
                    for _ in range(RUNS-1):
                        t, _ = solve(cnf)
                        times.append(t)
                    
                    mean_solve_time = sum(times) / len(times)
                    times.sort()
                    median_solve_time = times[len(times) // 2]
                    
                    n_nodes = G.number_of_nodes()
                    m_edges = G.number_of_edges()
                    
                    f.write(f'{n_nodes},{m_edges},{mean_solve_time:.9f},{result},{median_solve_time:.9f}\n')

if __name__ == "__main__":
    run_benchmarks()
