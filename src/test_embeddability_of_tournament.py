from pysat.solvers import Solver
from graph_generators import generate_tournament_dag
from encoders import encode_upward_book_embedding

def find_upward_book_thickness(graph, max_pages):
    for p in range(1, max_pages + 1):
        cnf = encode_upward_book_embedding(graph, p)
        
        with Solver(name='Maplesat', bootstrap_with=cnf) as solver:
            sat_result = solver.solve()
            if sat_result:
                return p
    return None

print('n, min_pages')

for n in range(20, 100, 10):
    G = generate_tournament_dag(n)

    t = find_upward_book_thickness(G, n//2 + 1)

    print(f'{n}, {t}')
