from pathlib import Path
from utils.read_graph import read_graph
from solvers.google_cp_sat import solve_graph

graphs_dir = Path(__file__).resolve().parent / 'graphs'

graphs = []

for file_path in graphs_dir.iterdir():
    if file_path.is_file():
        graphs.append(read_graph(file_path))

graphs.sort(key=lambda g: (g.name.split('_')[0], int(g.name.split('_')[1])))

for graph in graphs:
    print(graph.name)
    solve_graph(graph.num_nodes, graph.edges)
    print()