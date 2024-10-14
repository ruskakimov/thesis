from pysat.formula import CNF

def book_embedding_cnf(graph, P):
    """
    SAT encodes book embedding for P pages.
    Based on Bekos encoding (2015).

    Number of variables = n^2 + m^2 + pm
    Number of clauses = n^3 + m^2
    """

    cnf = CNF()
    edges = graph.edges()
    N = len(graph.nodes)
    M = len(edges)

    variable_count = 0
    
    is_left_to = {}
    for i in range(N):
        for j in range(i+1, N):
            variable_count += 1
            is_left_to[(i, j)] = variable_count

    # Variable: Whether vertex i is to the left of vertex j along the book spine
    L = lambda i, j: is_left_to[(i, j)] if i < j else -is_left_to[(j, i)]

    # Rule: Transitivity rule must hold
    # Lij and Ljk -> Lik
    # CNF form: Lik | ~Lij | ~Ljk
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if i != j and i != k and j != k:
                    cnf.append([L(i,k), -L(i,j), -L(j,k)])
    
    # TODO: The search space of possible satisfying assignments can be reduced by choosing a particular vertex as the first vertex along the spine

    # edge_index = {}
    # for i, u, v in enumerate(edges):
    #     edge_index[(u, v)] = i
    
    edge_to_page = {}
    for i in range(M):
        for p in range(P):
            variable_count += 1
            edge_to_page[(i, p)] = variable_count

    # Variable: Whether edge with index i is assigned to page p
    EP = lambda i, p: edge_to_page[(i, p)]

    # Rule: Every edge is assigned to at least 1 page (TODO: Test if adding restriction of only 1 page helps)
    for i in range(M):
        clause = [EP(i, p) for p in range(P)]
        cnf.append(clause)

    # TODO: We can again reduce the search space by the fixed page assignment rule, that fixes a single edge on a particular page

    # Intermediate variable X - whether two edges belong to the same page
    edges_cross = {}
    for i in range(M):
        for j in range(i+1, M):
            variable_count += 1
            edges_cross[(i, j)] = variable_count
    X = lambda i, j: edges_cross[(i, j)] if i < j else edges_cross[(j, i)]

    # Enforce correct values for X (only true if both edges are assigned to the same page)
    # (EPi1 and EPj1) or (EPi2 and EPj2) or ... or (EPip and EPjp) -> Xij

    # Planarity rule for edges on the same page

    return cnf
