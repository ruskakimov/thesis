import time
import networkx as nx
from math import ceil
from pysat.solvers import Solver
from helpers import rome_graphs, write_cnf
from encoders import encode_planarity, encode_graceful_labeling, encode_book_embedding, decode_book_embedding

def test_planarity():
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for graph in rome_graphs():
        cnf = encode_planarity(graph)
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

        cnf = encode_graceful_labeling(graph)

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
    for n in range(4, 11):
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

        cnf = encode_book_embedding(graph, pages)
        
        number_of_clauses = len(cnf.clauses)
        number_of_vars = cnf.nv

        print(f"{graph_name} in {pages} pages")
        print(f"p cnf {number_of_vars} {number_of_clauses}")

        # TODO: Maplesat vs Cadical195
        with Solver(name='Maplesat', bootstrap_with=cnf) as solver:
            start_time = time.time()
            sat_result = solver.solve()
            end_time = time.time()
            
            actual_result = 'SAT' if sat_result else 'UNSAT'
            expected_result = 'SAT' if expected else 'UNSAT'

            print(f"{'🟢' if sat_result == expected else '🔴'} actual: {actual_result}, expected: {expected_result}")

            time_taken = end_time - start_time
            print(f"Time taken: {time_taken:.8f} seconds")
            print()

# test_book_embedding()

K5 = nx.complete_graph(5)
P = 3
cnf = encode_book_embedding(K5, P)
# write_cnf(cnf, 'K9_5page')

with Solver(bootstrap_with=cnf) as solver:
    sat_result = solver.solve()
    print(sat_result)
    print()

    solution = solver.get_model()
    decode_book_embedding(K5, P, solution)
