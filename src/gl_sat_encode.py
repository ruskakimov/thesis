from pathlib import Path
from src.dataset import read_all_graphs

cnf_dir = Path(__file__).resolve().parent.parent / 'cnf'

def naive_sat_encode_graph(graph):
    """
    Encodes graceful labeling of a given graph into CNF.
    Based on "Vertex-edge encoding" (Kraayenbrink 2011).

    Variables - n*(m+1) + m^2                            ~ 2(m^2)
    Clauses - n*(m+1) + m^2 + n^2*m + m^3 + m^3          ~ 2(m^2) + 3(m^3)

    Legend:
        n - number of nodes
        m - number of edges
        i - node label. Range is [0, m].
        j - calculated edge label. Range is [1, m].

    CNF variables:
        X_v_i - node `v` has label `i`. Range is [1, n*(m+1)].
        Y_vw_j - edge `v,w` has label `j`. Range is [n*(m+1)+1, n*(m+1)+m*m].
    
    Returns:
        int: number of variables
        List[List[int]]: list of disjunctive clauses
    """

    n = graph.num_nodes
    m = len(graph.edges)
    num_vars = n*(m+1) + m*m
    clauses = []

    # Note: all variables start from `0` here.
    X = lambda v, i: 1 + v*(m+1) + i
    Y = lambda vw, j: X(n-1, m) + 1 + vw*m + j

    # Constraint: Node `v` has at least one label
    for v in range(n):
        clause = [X(v, i) for i in range(m+1)]
        clauses.append(clause)
    
    # Constraint: Edge `v,w` has at least one label
    for vw in range(m):
        clause = [Y(vw, j) for j in range(m)]
        clauses.append(clause)

    # Constraint: At most one node has label `i`
    for v in range(n):
        for w in range(v+1, n):
            for i in range(m+1):
                clause = [-X(v, i), -X(w, i)]
                clauses.append(clause)

    # Constraint: At most one edge has label `j`
    for vw1 in range(m):
        for vw2 in range(vw1+1, m):
            for j in range(m):
                clause = [-Y(vw1, j), -Y(vw2, j)]
                clauses.append(clause)

    # Constraint: If vertex `v` has label `i` and vertex `w` has label `j` then edge `v,w` has label `abs(i-j)`
    for vw, (v, w) in enumerate(graph.edges):
        for i in range(m+1):
            for j in range(m+1):
                if i != j:
                    clause = [-X(v, i), -X(w, j), Y(vw, abs(i-j)-1)]
                    clauses.append(clause)
    
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
