import networkx as nx
from encoders import encode_book_embedding, decode_book_embedding
from pysat.solvers import Solver

def solve(cnf):
    with Solver(name='Lingeling', bootstrap_with=cnf) as solver:
        result = solver.solve()
        model = solver.get_model() if result else None
        return (result, model)

G = nx.DiGraph()

G.add_nodes_from(range(6))

G.add_edges_from([(u-1, v-1) for u,v in [
    (1,2), (1,3), (1,4), (1,5), (1,6),
    (2,3), (2,4), (2,5), (2,6),
    (3,4), (3,5), (3,6),
    (4,5), (4,6)
]])

cnf = encode_book_embedding(G, 3)

result, model = solve(cnf)

print(result, model)

decode_book_embedding(G, 3, model)
