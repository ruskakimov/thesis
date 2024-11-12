from pysat.formula import CNF

def get_variables(N):
    variable_count = 0
    
    is_left_to = {}
    for i in range(N):
        for j in range(i+1, N):
            variable_count += 1
            is_left_to[(i, j)] = variable_count
    
    # Variable: Whether vertex i is to the left of vertex j along the book spine
    L = lambda i, j: is_left_to[(i, j)] if i < j else -is_left_to[(j, i)]
    
    # Variable: Whether edge with index i is on top page
    TOP = lambda i: variable_count + i + 1

    return (L, TOP)

def encode_2UBE(digraph):
    cnf = CNF()
    nodes = list(digraph.nodes)
    edges = list(digraph.edges())
    N = len(digraph.nodes)
    M = len(edges)

    node_index = {nodes[i]: i for i in range(N)}

    L, TOP = get_variables(N)

    # Rule: Transitivity rule must hold
    # Lij and Ljk -> Lik
    # CNF form: Lik | ~Lij | ~Ljk
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for k in range(N):
                if i != k and j != k:
                    cnf.append([-L(i,j), -L(j,k), L(i,k)])
    

    # Rule: Nodes are topologically ordered
    for u, v in edges:
        i = node_index[u]
        j = node_index[v]
        cnf.append([L(i, j)])
    
    # Rule: Planarity rule for edges on the same page
    for a in range(M):
        for b in range(a+1, M):
            i, j = map(lambda x: node_index[x], edges[a])
            k, l = map(lambda x: node_index[x], edges[b])
            
            if len(set([i, j, k, l])) == 4: # pairwise different
                # Crossing on top page
                cnf.append([-TOP(a), -TOP(b), -L(i, k), -L(k, j), -L(j, l)]) # i, k, j, l
                cnf.append([-TOP(a), -TOP(b), -L(k, i), -L(i, l), -L(l, j)]) # k, i, l, j

                # Crossing on bottom page
                cnf.append([TOP(a), TOP(b), -L(i, k), -L(k, j), -L(j, l)]) # i, k, j, l
                cnf.append([TOP(a), TOP(b), -L(k, i), -L(i, l), -L(l, j)]) # k, i, l, j
    
    return cnf
