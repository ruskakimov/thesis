import networkx as nx
from encoders import encode_upward_book_embedding, decode_book_embedding
from pysat.solvers import Solver

def solve(cnf):
    with Solver(name='Lingeling', bootstrap_with=cnf) as solver:
        result = solver.solve()
        model = solver.get_model() if result else None
        return (result, model)

def test_valid_embedding(vertices, by_pages):
    for page_edges in by_pages:
        for u,v in page_edges:
            i = vertices.index(u)
            j = vertices.index(v)
            if not i < j:
                return False
        for a in page_edges:
            for b in page_edges:
                if a != b:
                    u0,v0 = a
                    u1,v1 = b
                    if vertices.index(u0) < vertices.index(u1) < vertices.index(v0) < vertices.index(v1):
                        return False
                    if vertices.index(u1) < vertices.index(u0) < vertices.index(v1) < vertices.index(v0):
                        return False
        return True


G = nx.DiGraph()

G.add_nodes_from(range(6))

G.add_edges_from([(u-1, v-1) for u,v in [
    (1,2), (1,3), (1,4), (1,5), (1,6),
    (2,3), (2,4), (2,5), (2,6),
    (3,4), (3,5), (3,6),
    (4,5), (4,6)
]])

cnf = encode_upward_book_embedding(G, 3)

result, model = solve(cnf)

vertices, by_pages = decode_book_embedding(G, 3, model)

print('=' * 30)
print('Is valid upwards embedding: ', test_valid_embedding(vertices, by_pages))
