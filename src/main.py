import sys
from pathlib import Path
import matplotlib.pyplot as plt
import time
import networkx as nx
from math import ceil
from pysat.solvers import Solver
from helpers import rome_graphs, north_graphs,  write_cnf, random_dag_graphs, T
from encoders import encode_planarity, encode_graceful_labeling, encode_book_embedding, decode_book_embedding, encode_upward_book_embedding, encode_2UBE, solve_2UBE_SAT, verify_2UBE, solve_kUBE_SAT
from graph_generators import generate_path_dag, generate_directed_cycle_graph, generate_complete_binary_arborescence, generate_tournament_dag, random_dag_with_density, generate_grid_dag, diamond_graph, manta_ray_graph, generate_cube_dag, generate_4d_grid_dag

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

def test_upward_book_embedding():
    print('Testing Upward Book Embedding (kUBE) SAT encoding.')

    test_cases = []

    # Test directed path graphs, which are always embeddable in 1 page
    for n in range(2, 11):
        for p in [1, 2]:
            test_cases.append((
                generate_path_dag(n),
                p,
                True,
                f'P{n}'
            ))
    
    # Test directed cycle graphs, which are never topologically embeddable
    for n in [3, 4, 5]:
        for p in range(1, 4):
            test_cases.append((
                generate_directed_cycle_graph(n),
                p,
                False,
                f'C{n}'
            ))
    
    # Test complete binary arborescence graphs, which are always embeddable in 1 page
    for levels in [2, 3, 4, 5]:
        for p in [1, 2]:
            test_cases.append((
                generate_complete_binary_arborescence(levels),
                p,
                True,
                f'BA{n}'
            ))
    
    # Test complete directed graphs (tournament), for which the exact book thickness is known: ceil(N / 2)
    for n in [30]:
        min_p = ceil(n / 2)

        for p in [15, 12, 13, 14]:
            test_cases.append((
                generate_tournament_dag(n),
                p,
                p >= min_p,
                f'T{n}'
            ))
    
    for digraph, pages, expected, graph_name in test_cases:
        cnf = encode_upward_book_embedding(digraph, pages)
        
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

def find_upward_book_thickness(graph, max_pages):
    for p in range(1, max_pages + 1):
        cnf = encode_upward_book_embedding(graph, p)
        
        with Solver(name='Maplesat', bootstrap_with=cnf) as solver:
            sat_result = solver.solve()
            if sat_result:
                return p
    return None

# print('Diamond graph book thickness:', find_upward_book_thickness(diamond_graph, 10))
# print('Manta ray graph book thickness:', find_upward_book_thickness(manta_ray_graph, 10))

# G = generate_grid_dag(3, 3)
# edges = list(G.edges())
# n = G.number_of_nodes()

# T.start('Solve')
# node_order, edge_assignment = solve_2UBE_SAT(G)
# # node_order, edge_assignment = solve_kUBE_SAT(G, 2)
# print(node_order)
# print(edge_assignment)
# T.stop('Solve')

# print([i+1 for i in node_order])
# for i, p in enumerate(edge_assignment):
#     u, v = edges[i]
#     print(u+1, '->', v+1, ':', p)

# # CP-1: 30 seconds for 8x8
# # Solution: 0 1 8 16 9 2 3 10 17 24 32 25 18 11 4 5 12 19 26 33 40 48 41 34 27 20 13 6 7 14 21 28 35 42 49 56 57 50 43 36 29 22 15 23 30 37 44 51 58 59 52 45 38 31 39 46 53 60 61 54 47 55 62 63

# print('Correct:', verify_2UBE(G, node_order, edge_assignment))

cnf_dir = Path(__file__).resolve().parent.parent / 'cnf'
# print(cnf_dir)

i = 0

for G in random_dag_graphs():
    i += 1
    print(i)
    print(f"Working on graph {i}", file=sys.stderr)

    T.start(G.name)

    cnf1 = encode_upward_book_embedding(G, 2)
    write_cnf(cnf1, cnf_dir / 'random_dag_SAT1' / f'{G.name}.cnf')
    
    cnf2 = encode_2UBE(G)
    write_cnf(cnf2, cnf_dir / 'random_dag_SAT2' / f'{G.name}.cnf')
    
    T.stop(G.name)
    print('---')

    # print(G.name, G.number_of_nodes(), G.number_of_edges())
