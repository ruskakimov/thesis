import networkx as nx
from math import ceil
from pysat.solvers import Solver
from helpers import rome_graphs, write_cnf
from encoders import planarity_cnf, graceful_labeling_cnf, book_embedding_cnf, decode_book_embedding

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
        graph = nx.Graph()
        graph.add_edges_from(edges)

        cnf = graceful_labeling_cnf(graph)

        with Solver(bootstrap_with=cnf) as solver:
            sat_result = solver.solve()
            print(f"Test {i + 1}: {'🟢' if sat_result == expected else '🔴'} {'SAT' if sat_result else 'UNSAT'}")

def test_book_embedding():
    print('Testing book embedding SAT encoding.')

    test_cases = []

    # Test path graphs, which are always embeddable in 1 page
    for n in range(2, 11):
        for p in [1, 2]:
            test_cases.append((
                nx.path_graph(n).edges(),
                p,
                True,
                f'P{n}'
            ))

    # Test complete graphs, for which the exact book thickness is known: ceil(N / 2)
    for n in range(4, 21):
        min_p = ceil(n / 2)

        for p in range(1, min_p + 1):
            test_cases.append((
                list(nx.complete_graph(n).edges()),
                p,
                p >= min_p,
                f'K{n}'
            ))
    
    for i, (edges, pages, expected, graph_name) in enumerate(test_cases):
        graph = nx.Graph()
        graph.add_edges_from(edges)

        cnf = book_embedding_cnf(graph, pages)

        with Solver(bootstrap_with=cnf) as solver:
            sat_result = solver.solve()
            
            actual_result = 'SAT' if sat_result else 'UNSAT'
            expected_result = 'SAT' if expected else 'UNSAT'

            print(f"{'🟢' if sat_result == expected else '🔴'} graph: {graph_name}, pages: {pages}, actual: {actual_result}, expected: {expected_result}")

# test_book_embedding()

K5 = nx.complete_graph(5)
cnf = book_embedding_cnf(K5, 2)
write_cnf(cnf.nv, cnf.clauses, 'K5_2page')


# decode_book_embedding(K5, 2, '-1 -2 -3 4 -5 6 -7 -8 -9 10 11 12 13 -14 15 -16 17 18 19 -20 21 -22 -23 24 -25')