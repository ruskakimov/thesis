from pysat.formula import CNF
from pysat.solvers import Solver
import networkx as nx
from dataset import rome_graphs

def encode_planarity_with_left(graph):
    """
    Encodes planarity testing based on left-orientation into a SAT problem.
    
    :param graph: A networkx graph.
    :return: CNF object representing the SAT problem.
    """
    cnf = CNF()
    V = len(graph.nodes)
    edges = [tuple(sorted((int(u), int(v)))) for u, v in graph.edges()]
    left_vars = {}

    # Create variables for left relationships Lx_uv
    var_count = 1
    for x in range(V):
        for u in range(V):
            for v in range(u+1, V):
                left_vars[(x, u, v)] = var_count
                var_count += 1
    
    L = lambda x, y, z: left_vars[(x, y, z)] if y <= z else -left_vars[(x, z, y)]

    # No edge crossings
    # not (L(cba) and L(dab) and L(dac) and L(dcb))
    # and
    # not (L(cab) and L(dba) and L(dca) and L(dbc))
    for (a, b) in edges:
        for (c, d) in edges:
            if len(set([a, b, c, d])) == 4:
                cnf.append([-L(c,b,a), -L(d,a,b), -L(d,a,c), -L(d,c,b)])
                cnf.append([-L(c,a,b), -L(d,b,a), -L(d,c,a), -L(d,b,c)])

    return cnf

def verify_sat(graph):
    # Perform networkx planarity test
    is_true_planar, _ = nx.check_planarity(graph)

    # Encode the problem as a SAT formula
    cnf = encode_planarity_with_left(graph)

    # Use a SAT solver to check satisfiability
    solver = Solver()
    solver.append_formula(cnf)
    is_sat_planar = solver.solve()
    solver.delete()

    return is_sat_planar, is_true_planar

true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0

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