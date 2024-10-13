import networkx as nx
from pysat.solvers import Solver
from helpers import rome_graphs
from encoders import graceful_labeling_cnf, planarity_cnf

def test_planarity():
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for graph in rome_graphs():
        cnf = planarity_cnf(graph)
        solver = Solver()
        solver.append_formula(cnf)
        
        actual = solver.solve()
        correct, _ = nx.check_planarity(graph)

        solver.delete()

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

test_planarity()