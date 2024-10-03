from pathlib import Path
from utils.read_graph import read_graph
from solvers.google_cp_sat import solve_graph

graphs_dir = Path(__file__).resolve().parent / 'graphs'

graphs = []

for file_path in graphs_dir.iterdir():
    if file_path.is_file():
        graphs.append(read_graph(file_path))

for graph in graphs:
    n, edges = graph
    # print(n, edges[:10])
    solve_graph(n, edges)