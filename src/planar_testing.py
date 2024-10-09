from pysat.formula import CNF
from pysat.solvers import Solver
import networkx as nx
from dataset import rome_graphs

def encode_schnyder_planarity(vertices, edges):
    """
    Encodes Schnyder realizer-based planarity checking into a SAT problem.
    
    :param graph: A triangulated networkx graph.
    :return: CNF object representing the SAT problem.
    """
    cnf = CNF()
    
    # Create variables for edge directions
    edge_vars = {(u, v): [cnf.nv + 1, cnf.nv + 2, cnf.nv + 3] for u, v in edges}
    
    for u, v in edges:
        d1, d2, d3 = edge_vars[(u, v)]
        
        # Ensure each edge (u, v) is assigned to exactly one direction
        cnf.append([d1, d2, d3])  # At least one direction
        cnf.append([-d1, -d2])    # Not both d1 and d2
        cnf.append([-d1, -d3])    # Not both d1 and d3
        cnf.append([-d2, -d3])    # Not both d2 and d3

    # Constraints to ensure each vertex has exactly one outgoing edge per direction
    for v in vertices:
        out_edges = [edge_vars[(v, u)][k] for u in graph.neighbors(v) for k in range(3) if (v, u) in edge_vars]
        for k in range(3):
            # For direction k, ensure exactly one outgoing edge from each vertex
            cnf.append(out_edges)  # At least one outgoing edge in direction k
            # Further constraints to ensure that there is no more than one can be added with cardinality constraints

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
    cnf = encode_schnyder_planarity(vertices, edges)

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