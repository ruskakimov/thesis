from pysat.formula import CNF
from pysat.solvers import Solver
import networkx as nx

def encode_planarity(vertices, edges):
    """
    Encodes the planarity testing problem for a given graph into a SAT problem.
    
    :param vertices: List of vertices in the graph.
    :param edges: List of edges (tuples of vertices).
    :return: CNF object representing the SAT problem.
    """
    cnf = CNF()
    edge_vars = {}
    ordering_vars = {}

    # Generate crossing variables for each pair of edges
    var_count = 1
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            e1 = edges[i]
            e2 = edges[j]

            # Skip pairs of edges that share a vertex (they cannot cross)
            if len(set(e1).intersection(e2)) > 0:
                continue

            # Variable representing whether e1 and e2 cross
            var_name = f'c_{e1}_{e2}'
            edge_vars[(e1, e2)] = var_count
            cnf.append([-var_count])  # We want to find an embedding where all crossings are false
            var_count += 1

    # Generate ordering variables for edges around each vertex
    for vertex in vertices:
        adjacent_edges = [e for e in edges if vertex in e]

        for i in range(len(adjacent_edges)):
            for j in range(i + 1, len(adjacent_edges)):
                e1 = adjacent_edges[i]
                e2 = adjacent_edges[j]

                # Variable representing whether e1 comes before e2 in clockwise order around the vertex
                var_name = f'o_{e1}_{e2}_at_{vertex}'
                ordering_vars[(e1, e2, vertex)] = var_count
                var_count += 1

    # Encode that if edges have a certain order, they cannot cross
    for (e1, e2, vertex) in ordering_vars:
        ordering_var = ordering_vars[(e1, e2, vertex)]
        crossing_var = edge_vars.get((e1, e2)) or edge_vars.get((e2, e1))

        if crossing_var:
            # If the order is set, then the crossing variable must be false
            cnf.append([-ordering_var, -crossing_var])

    # Transitivity of ordering: if o(e1, e2) and o(e2, e3), then o(e1, e3)
    for vertex in vertices:
        adjacent_edges = [e for e in edges if vertex in e]

        for i in range(len(adjacent_edges)):
            for j in range(i + 1, len(adjacent_edges)):
                for k in range(j + 1, len(adjacent_edges)):
                    e1 = adjacent_edges[i]
                    e2 = adjacent_edges[j]
                    e3 = adjacent_edges[k]

                    var1 = ordering_vars.get((e1, e2, vertex))
                    var2 = ordering_vars.get((e2, e3, vertex))
                    var3 = ordering_vars.get((e1, e3, vertex))

                    if var1 and var2 and var3:
                        # If (e1 before e2) and (e2 before e3), then (e1 before e3)
                        cnf.append([-var1, -var2, var3])

    return cnf

# Example usage:
vertices = ['A', 'B', 'C', 'D']
edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D')]

G = nx.Graph()
G.add_edges_from(edges)
is_true_planar, embedding = nx.check_planarity(G)

cnf = encode_planarity(vertices, edges)

# Now, use a SAT solver to check satisfiability
solver = Solver()
solver.append_formula(cnf)

is_sat_planar = solver.solve()

if is_sat_planar != is_true_planar:
    print('Oops! Wrong answer by SAT!')
else:
    print('SAT was correct!')
    print('Solution:', solver.get_model())

solver.delete()
