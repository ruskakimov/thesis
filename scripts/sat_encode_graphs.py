from pathlib import Path
from utils.read_graph import read_all_graphs

cnf_dir = Path(__file__).resolve().parent.parent / 'graphs'

def naive_sat_encode_graph(graph):
    """
    Encodes graceful labeling of a given graph into CNF.
    Based on "Vertex-edge encoding" (Kraayenbrink 2011).

    Constants:
        n - number of nodes
        m - number of edges
    
    Variables:
        i - node label. Range is [0, m].
        j - edge label. Range is [1, m].

    CNF variables:
        X_v_i - node `v` has label `i`. Range is [1, n*(m+1)].
        Y_vw_j - edge `v,w` has label `j`. Range is [n*(m+1)+1, n*(m+1)+1 + m*m].
    
    Returns:
        int: number of variables
        List[List[int]]: list of disjunctive clauses
    """

    n = graph.num_nodes
    m = len(graph.edges)
    num_vars = n*(m+1)+1 + m*m
    clauses = []

    edge_index = {}
    for i, v, w in enumerate(graph.edges):
        edge_index[(min(v,w), max(v,w))] = i

    X = lambda v, i: 1 + v*(m+1) + i
    Y = lambda v, w, j: X(n-1, m) + 1 + edge_index[(min(v,w), max(v,w))]*m + j

    # Constraint: Node `v` has at least one label
    for v in range(n):
        clause = [X(v, i) for i in range(m+1)]
        clauses.append(clause)
    
    # Constraint: Edge `v,w` has at least one label
    for edge in graph.edges:
        v, w = edge
        clause = [Y(v, w, j) for j in range(m)]
        clauses.append(clause)

    # Constraint: At most one node has label `i`

    # Constraint: At most one edge has label `j`

    # Constraint: If vertex `v` has label `i` and vertex `w` has label `j` then edge `v,w` has label `abs(i-j)`
    
    return (num_vars, clauses)

def write_cnf_to_file(num_vars, clauses, name):
    with open(cnf_dir / f'{name}.cnf', 'w') as file:
        file.write(f'p cnf {num_vars} {len(clauses)}\n')
        for clause in clauses:
            file.write(' '.join(map(str, clause)) + " 0\n")

graphs = read_all_graphs()

for graph in graphs:
    num_vars, clauses = naive_sat_encode_graph(graph)
    write_cnf_to_file(num_vars, clauses, graph.name)
