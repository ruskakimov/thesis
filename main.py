from utils.read_graph import read_all_graphs
from solvers.google_cp_sat import solve_graph

graphs = read_all_graphs()

for graph in graphs:
    print(graph.name)
    solve_graph(graph.num_nodes, graph.edges)
    print()