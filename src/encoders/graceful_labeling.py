import math
from pysat.formula import CNF

# At-most-one clauses
# Bimander encoding (Van-Hau Nguyen et. al.)
def AMO(cnf, vars, var_count):
    n = len(vars)

    # pairwise
    # for i in range(n):
    #     for j in range(i+1, n):
    #         clause = [-vars[i], -vars[j]]
    #         cnf.append(clause)

    group_size = 2 # most optimal is 2
    m = math.ceil(n / group_size)
    log_m = math.ceil(math.log(m) / math.log(2))

    def G(i): # 0-indexed
        a = i * group_size
        b = a + 1
        if b < n:
            return [a, b]
        else:
            return [a]
    
    # 1) pairwise AMO
    for i in range(m):
        g = G(i)
        if len(g) < 2:
            continue
        for a in range(len(g)):
            for b in range(a+1, len(g)):
                clause = [-g[a], -g[b]]
                cnf.append(clause)

    return var_count + log_m

def get_variables(N, M):
    # X_v_i - node `v` has label `i`. Range is [1, n*(m+1)].
    X = lambda v, i: 1 + v*(M+1) + i

    # Y_vw_j - edge `v,w` has label `j`. Range is [n*(m+1)+1, n*(m+1)+m*m].
    Y = lambda vw, j: X(N-1, M) + 1 + vw*M + j

    return (X, Y)

def encode_graceful_labeling(graph):
    """
    SAT encodes graceful labeling.
    Based on "Vertex-edge encoding" (Kraayenbrink, 2011).

    Number of variables = n*(m+1) + m^2                      ~ 2(m^2)
    Number of clauses = n*(m+1) + m^2 + n^2*m + m^3 + m^3    ~ 2(m^2) + 3(m^3)
    """

    cnf = CNF()
    nodes = list(graph.nodes())
    N = len(nodes)
    M = len(graph.edges())

    node_index = {nodes[i]: i for i in range(N)}

    X, Y = get_variables(N, M)

    node_labels = list(range(M+1)) # [0,M]
    edge_labels = list(range(M))   # [0,M-1] represents [1,M]

    var_count = Y(M-1, M-1)

    # Constraint: Node `v` has at least one label
    for v in range(N):
        clause = [X(v, i) for i in range(M+1)]
        cnf.append(clause)
    
    # Constraint: Edge `v,w` has at least one label
    for vw in range(M):
        clause = [Y(vw, j) for j in edge_labels]
        cnf.append(clause)

    # Constraint: At most one node has label `i`
    for i in node_labels:
        var_count = AMO(cnf, [X(v, i) for v in range(N)], var_count)

    # Constraint: At most one edge has label `j`
    for j in edge_labels:
        var_count = AMO(cnf, [Y(vw, j) for vw in range(M)], var_count)

    # Constraint: If vertex `v` has label `i` and vertex `w` has label `j` then edge `v,w` has label `abs(i-j)`
    for vw, (v, w) in enumerate(graph.edges):
        for i in node_labels: # node v label (i)
            for j in node_labels: # node w label (j)
                if i != j:
                    clause = [-X(node_index[v], i), -X(node_index[w], j), Y(vw, abs(i-j)-1)]
                    cnf.append(clause)
    
    return cnf

def decode_graceful_labeling(graph, solution):
    if not solution:
        return
    
    vertices = list(graph.nodes)
    edges = list(graph.edges)
    N = len(vertices)
    M = len(edges)

    X, Y = get_variables(N, M)

    value_of = {}
    for var in solution:
        value_of[abs(var)] = var > 0
        value_of[-abs(var)] = var < 0

    node_labels = [-1] * N

    for v in range(N):
        for i in range(M+1):
            if value_of[X(v, i)]:
                node_labels[v] = i
                break
    
    return node_labels

def is_valid_graceful_labeling(graph, node_labels):
    vertices = list(graph.nodes)
    edges = list(graph.edges)

    edge_labels = set()

    for u, v in edges:
        i = vertices.index(u)
        j = vertices.index(v)

        a = node_labels[i]
        b = node_labels[j]

        edge_label = abs(a-b)
        if edge_label in edge_labels:
            return False
        edge_labels.add(edge_label)
    
    return True