import networkx as nx
from pysat.solvers import Solver
from helpers import rome_graphs
from encoders import planarity_cnf

def verify_sat(graph):
    is_true_planar, _ = nx.check_planarity(graph)

    cnf = planarity_cnf(graph)

    solver = Solver()
    solver.append_formula(cnf)
    is_sat_planar = solver.solve()
    solver.delete()

    return is_sat_planar, is_true_planar

true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0

G = nx.complete_graph(5)

for graph in rome_graphs():
    actual, correct = verify_sat(graph)
    if actual == correct:
        if actual:
            true_positive += 1
        else:
            true_negative += 1
    else:
        if actual:
            false_positive += 1
        else:
            false_negative += 1

    print(f"\rTP: {true_positive}, TN: {true_negative}, FP: {false_positive}, FN: {false_negative}", end="")

print()