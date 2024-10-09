import itertools
from pysat.formula import CNF
from pysat.solvers import Solver
import networkx as nx
from dataset import rome_graphs

def encode_kuratowski_planarity(vertices, edges):
    """
    Encodes the Kuratowski-based planarity testing problem into a SAT formula.
    
    :param graph: A networkx graph.
    :return: CNF object representing the SAT problem.
    """
    cnf = CNF()

    # Create a dictionary for edge variables
    edge_vars = {e: i + 1 for i, e in enumerate(edges)}

    # Generate clauses to detect forbidden K5 or K3,3 subgraphs
    for subset in itertools.combinations(vertices, 5):
        # Check if the subset can form a K5 structure
        k5_edges = itertools.combinations(subset, 2)
        clause = [-edge_vars[(u, v)] if (u, v) in edge_vars else -edge_vars[(v, u)]
                  for u, v in k5_edges if (u, v) in edge_vars or (v, u) in edge_vars]
        if clause:
            cnf.append(clause)

    for subset in itertools.combinations(vertices, 6):
        # Check if the subset can form a K3,3 structure
        for partition in itertools.combinations(subset, 3):
            part1 = set(partition)
            part2 = set(subset) - part1
            k33_edges = itertools.product(part1, part2)
            clause = [-edge_vars[(u, v)] if (u, v) in edge_vars else -edge_vars[(v, u)]
                      for u, v in k33_edges if (u, v) in edge_vars or (v, u) in edge_vars]
            if clause:
                cnf.append(clause)

    return cnf

def verify_sat(graph):
    """
    Compares the planarity result of a SAT-based method with networkx's method.
    
    :param graph: A networkx graph.
    :param filename: The name of the GML file for reporting.
    """
    # Get the vertices and edges of the graph
    vertices = list(graph.nodes)
    edges = list(graph.edges)

    # Perform networkx planarity test
    is_true_planar, _ = nx.check_planarity(graph)

    # Encode the problem as a SAT formula
    cnf = encode_kuratowski_planarity(vertices, edges)

    # Use a SAT solver to check satisfiability
    solver = Solver()
    solver.append_formula(cnf)
    is_sat_planar = solver.solve()
    solver.delete()

    return is_sat_planar == is_true_planar

correct = 0
wrong = 0

for graph in rome_graphs():
    if verify_sat(graph):
        correct += 1
    else:
        wrong += 1

    print(f"\rCorrect: {correct}, Wrong: {wrong}", end="")

print()