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
    
    L = lambda x, a, b: left_vars[(x, a, b)] if a <= b else -left_vars[(x, b, a)]

    # cycles = nx.cycle_basis(graph)
    cycles = nx.simple_cycles(graph)

    # Vertex x is inside abc cycle:
    # Lxab and Lxbc and Lxca
    
    # Vertex x is outside abc cycle:
    # Lxba or Lxcb or Lxac

    # Vertex x is inside or outside of abc cycle:
    # (Lxab and Lxbc and Lxca) or (Lxba or Lxcb or Lxac)
    
    # Vertex must be inside or outside any given cycle.
    for x in range(V):
        for cycle in cycles:
            common = []
            for i in range(len(cycle)):
                u, v = int(cycle[i-1]), int(cycle[i])
                common.append(L(x, v, u))

            for i in range(len(cycle)):
                u, v = int(cycle[i-1]), int(cycle[i])
                cnf.append(common + [L(x, u, v)])

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