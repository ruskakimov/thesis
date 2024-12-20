from pysat.formula import CNF

def encode_graceful_labeling(graph):
    """
    SAT encodes graceful labeling.
    Based on "Vertex-edge encoding" (Kraayenbrink, 2011).

    Number of variables = n*(m+1) + m^2                      ~ 2(m^2)
    Number of clauses = n*(m+1) + m^2 + n^2*m + m^3 + m^3    ~ 2(m^2) + 3(m^3)
    """

    cnf = CNF()
    N = len(graph.nodes)
    M = len(graph.edges())

    # X_v_i - node `v` has label `i`. Range is [1, n*(m+1)].
    X = lambda v, i: 1 + v*(M+1) + i

    # Y_vw_j - edge `v,w` has label `j`. Range is [n*(m+1)+1, n*(m+1)+m*m].
    Y = lambda vw, j: X(N-1, M) + 1 + vw*M + j

    # Constraint: Node `v` has at least one label
    for v in range(N):
        clause = [X(v, i) for i in range(M+1)]
        cnf.append(clause)
    
    # Constraint: Edge `v,w` has at least one label
    for vw in range(M):
        clause = [Y(vw, j) for j in range(M)]
        cnf.append(clause)

    # Constraint: At most one node has label `i`
    for v in range(N):
        for w in range(v+1, N):
            for i in range(M+1):
                clause = [-X(v, i), -X(w, i)]
                cnf.append(clause)

    # Constraint: At most one edge has label `j`
    for vw1 in range(M):
        for vw2 in range(vw1+1, M):
            for j in range(M):
                clause = [-Y(vw1, j), -Y(vw2, j)]
                cnf.append(clause)

    # Constraint: If vertex `v` has label `i` and vertex `w` has label `j` then edge `v,w` has label `abs(i-j)`
    for vw, (v, w) in enumerate(graph.edges):
        for i in range(M+1):
            for j in range(M+1):
                if i != j:
                    clause = [-X(v, i), -X(w, j), Y(vw, abs(i-j)-1)]
                    cnf.append(clause)
    
    return cnf
