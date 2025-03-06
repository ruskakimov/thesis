import math
from pysat.formula import CNF

def AMO_pairwise(cnf, vars, var_count):
    n = len(vars)
    for i in range(n):
        for j in range(i+1, n):
            cnf.append([-vars[i], -vars[j]])
    return var_count

# At-most-one clauses
# Bimander encoding (Van-Hau Nguyen et. al.)
def AMO(cnf, vars, var_count, group_size=2):
    n = len(vars)

    # pairwise
    # for i in range(n):
    #     for j in range(i+1, n):
    #         clause = [-vars[i], -vars[j]]
    #         cnf.append(clause)

    m = math.ceil(n / group_size)
    log_m = math.ceil(math.log(m) / math.log(2))

    # Group `i`
    def G(i): # 0-indexed
        start = i * group_size
        return [vars[i] for i in range(start, min(start + group_size, n))]
    
    # Aux variables (commander, bin representation)
    def B(j): # 0-indexed
        return var_count + 1 + j

    def phi(i, j):
        if i & (1 << j):
            return B(j)
        else:
            return -B(j)
    
    # 1) pairwise AMO
    for i in range(m):
        g = G(i)
        if len(g) < 2:
            continue
        for h1 in range(len(g)):
            for h2 in range(h1+1, len(g)):
                clause = [-g[h1], -g[h2]]
                # print('pairwise', clause)
                cnf.append(clause)
    
    # 2) commander variables constraints
    for i in range(m):
        g = G(i)
        for h in range(len(g)):
            for j in range(log_m):
                x_i_h = g[h]
                clause = [-x_i_h, phi(i, j)]
                # print(f'{clause[0]} \/ {"-" if clause[1] < 0 else ""}b{abs(clause[1]) - 8}')
                cnf.append(clause)

    return var_count + log_m

test_cnf = []
AMO(test_cnf, list(range(1,9)), 8, group_size=3)
assert(test_cnf == [[-1, -2], [-1, -3], [-2, -3], [-4, -5], [-4, -6], [-5, -6], [-7, -8], [-1, -9], [-1, -10], [-2, -9], [-2, -10], [-3, -9], [-3, -10], [-4, 9], [-4, -10], [-5, 9], [-5, -10], [-6, 9], [-6, -10], [-7, -9], [-7, 10], [-8, -9], [-8, 10]])

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