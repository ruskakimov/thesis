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
import threading

PER_M = 100
TIMEOUT_PER_DAG_SEC = 60 * 5
RUNS = 1

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

from multiprocessing import Process, Pipe

def solve_worker(cnf, conn):
    with Solver(name='Lingeling', bootstrap_with=cnf) as solver:
        start = time.perf_counter()
        result = solver.solve()
        elapsed = time.perf_counter() - start
        conn.send((elapsed, result))
        conn.close()

def solve(cnf, timeout=TIMEOUT_PER_DAG_SEC):  # default: 20 minutes
    parent_conn, child_conn = Pipe()
    p = Process(target=solve_worker, args=(cnf, child_conn))
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        return timeout, None  # Timed out

    if parent_conn.poll():
        return parent_conn.recv()
    else:
        return timeout, None  # Unexpected failure

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
    
    for n in [15]:
        for k in [7]:
            print(f"Working on n={n}, k={k}", file=sys.stderr)
            output_file = output_dir / f"n{n}_k{k}___{RUNS}_run_eq_m_bins_2.csv"
            start_time = time.time()

            max_m = n*(n-1)//2
            total_dags = (1+max_m)*PER_M
            
            with open(output_file, 'w') as f:
                f.write('n,m,time(s),sat,median_time(s)\n')
                
                i = 0
                for G in dags(n):
                    i += 1
                    if i < 9457:
                        continue

                    # print(f"Working on n={n}, k={k}, dag={i}", file=sys.stderr)
                    print_progress_bar(i, total_dags, start_time)
                    
                    cnf = encode_upward_book_embedding(G, k)
                    
                    times = []
                    _, result = solve(cnf)
                    
                    for _ in range(RUNS):
                        t, result = solve(cnf)
                        times.append(t)
                    
                    mean_solve_time = sum(times) / len(times)
                    times.sort()
                    median_solve_time = times[len(times) // 2]

                    # print('Done, elapsed:', mean_solve_time)
                    
                    n_nodes = G.number_of_nodes()
                    m_edges = G.number_of_edges()
                    
                    f.write(f'{n_nodes},{m_edges},{mean_solve_time:.9f},{result},{median_solve_time:.9f}\n')
                    f.flush()

if __name__ == "__main__":
    run_benchmarks()
