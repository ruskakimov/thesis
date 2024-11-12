import time
import networkx as nx
from math import ceil
from pysat.solvers import Solver
from helpers import rome_graphs, write_cnf, T
from encoders import encode_planarity, encode_graceful_labeling, encode_book_embedding, decode_book_embedding, encode_upward_book_embedding, encode_2UBE
from graph_generators import generate_path_dag, generate_directed_cycle_graph, generate_complete_binary_arborescence, generate_tournament_dag, random_dag_with_density, generate_grid_dag

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

# test_upward_book_embedding()

for n in range(21, 29):
    G = generate_grid_dag(n, n)
    print(f"Grid DAG {n}x{n}")

    # cnf = encode_upward_book_embedding(G, 2)
    T.start("Encode")
    cnf = encode_2UBE(G)
    T.stop("Encode")

    T.start("Write")
    write_cnf(cnf, f'grid_dag_v2_{n}x{n}')
    T.stop("Write")



# for n in [2,3,4]:
#     G = generate_grid_dag(n, n)
#     print(f"Grid DAG {n}x{n}")

#     cnf = encode_2UBE(G)

#     T.start("Solve")
#     with Solver(name='Maplesat', bootstrap_with=cnf) as solver:
#         solver.solve()
#         T.stop("Solve")
#         decode_book_embedding(G, 2, solver.get_model())


# # Path graph
# for n in range(2, 1000+1):
#     cnf = encode_upward_book_embedding(generate_path_dag(n), 2)
#     with Solver(name='Maplesat', bootstrap_with=cnf) as solver:
#         start_time = time.time()
#         sat_result = solver.solve()
#         end_time = time.time()
        
#         result = 'SAT' if sat_result else 'UNSAT'
#         time_taken = end_time - start_time
        
#         print(", ".join([f"P{n}", result, f"{time_taken:.8f}s"]))

# for n in range(94, 100+1):
#     for density in range(10, 100+1, 10):
#         G = random_dag_with_density(n, density)
#         E = len(G.edges)

#         print()
#         print()
#         T.start(f"Encode")
#         cnf = encode_upward_book_embedding(G, 2)
#         T.stop(f"Encode")


#         T.start("Load")
#         with Solver(name='Maplesat', bootstrap_with=cnf) as solver:
#             T.stop("Load")

#             T.start("Solve")
#             sat_result = solver.solve()
#             time_taken = T.stop("Solve")
            
#             result = 'SAT' if sat_result else 'UNSAT'
            
#             print(", ".join([f"G{n}_{density}", str(E), result, f"{time_taken:.8f}s"]))

# T30 = generate_tournament_dag(30)
# for k in [12, 13, 14, 15]:
#     cnf = encode_upward_book_embedding(T30, k)
#     write_cnf(cnf, f'T30_{k}page')


# G = nx.read_gml('need4stacks275.gml')
# P = 4
# print(f'Number of nodes: {len(G.nodes)}')
# print(f'Number of edges: {len(G.edges)}')

# start_time = time.time()
# cnf = encode_book_embedding(G, P)
# end_time = time.time()

# print(f"Time taken: {end_time - start_time:.8f} seconds")

# print(f"p cnf {cnf.nv} {len(cnf.clauses)}")
# write_cnf(cnf, f'need4stacks275_{P}page')


# with Solver(name='Maplesat', bootstrap_with=cnf) as solver:
#     sat_result = solver.solve()
#     print(sat_result)
#     print()

#     # solution = solver.get_model()
#     # decode_book_embedding(K5, P, solution)
