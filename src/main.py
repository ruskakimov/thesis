import networkx as nx
from pysat.solvers import Solver
from helpers import rome_graphs
from encoders import planarity_cnf, graceful_labeling_cnf, book_embedding_cnf

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

def test_graceful_labeling():
    print('Testing graceful labeling SAT encoding.')

    test_cases = [
        ([[0, 1]], True),  # Single edge graph
        ([[0, 1], [2, 3]], False),  # Disconnected graph
        ([[0, 1], [1, 2], [2, 3]], True),  # Path graph P4
        ([[0, 1], [0, 2], [0, 3], [0, 4]], True),  # Star graph S4
        ([[0, 1], [1, 2], [2, 0]], True),  # Triangle graph C3
        ([[0, 1], [1, 2], [2, 3], [0, 4], [4, 1]], True), # Wiki image graph
        ([[0, 1], [1, 2], [2, 3], [3, 0], [0, 2], [1, 3]], True), # K4
        ([[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]], False), # Pentagon
        (nx.complete_graph(5).edges(), False) # K5
    ]
    
    for i, (edges, expected) in enumerate(test_cases):
        # Create a NetworkX graph from the edge list
        graph = nx.Graph()
        graph.add_edges_from(edges)

        # Generate CNF from the graph
        cnf = graceful_labeling_cnf(graph)

        # Solve the CNF
        with Solver(bootstrap_with=cnf) as solver:
            sat_result = solver.solve()

            # Print and validate the result
            result = "SAT" if sat_result else "UNSAT"
            print(f"Test {i + 1}: {'🟢' if sat_result == expected else '🔴'} {result}")

def test_book_embedding():
    print('Testing book embedding SAT encoding.')

    test_cases = [
        # Single edge graph is embeddable in P >= 1.
        ([[0, 1]], 1, True),
        ([[0, 1]], 2, True),
        ([[0, 1]], 3, True),
    ]
    
    for i, (edges, pages, expected) in enumerate(test_cases):
        # Create a NetworkX graph from the edge list
        graph = nx.Graph()
        graph.add_edges_from(edges)

        # Generate CNF from the graph
        cnf = graceful_labeling_cnf(graph)

        # Solve the CNF
        with Solver(bootstrap_with=cnf) as solver:
            sat_result = solver.solve()

            # Print and validate the result
            result = "SAT" if sat_result else "UNSAT"
            print(f"Test {i + 1}: {'🟢' if sat_result == expected else '🔴'} {result}")

test_book_embedding()
