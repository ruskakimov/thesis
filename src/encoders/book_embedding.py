from pysat.formula import CNF

def book_embedding_cnf(graph, P):
    """
    SAT encodes book embedding for P pages.
    Based on Bekos encoding (2015).

    Number of variables = n^2 + m^2 + pm
    Number of clauses = n^3 + m^2
    """

    cnf = CNF()
    N = len(graph.nodes)
    M = len(graph.edges())

    variable_count = 0
    is_left_to = {}

    for i in range(N):
        for j in range(i+1, N):
            variable_count += 1
            is_left_to[(i, j)] = variable_count

    # Whether vertex i is to the left of vertex j along the book spine
    L = lambda i, j: is_left_to[(i, j)] if i < j else -is_left_to[(j, i)]

    # Encode transitivity of L
    # Implies(And(Lij, Ljk), Lik)
    # Lik | ~Lij | ~Ljk
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if i != j and i != k and j != k:
                    cnf.append([L(i,k), -L(i,j), -L(j,k)])
    
    # TODO: The search space of possible satisfying assignments can be reduced by choosing a particular vertex as the first vertex along the spine

    # Every edge to only 1 page

    # TODO: We can again reduce the search space by the fixed page assignment rule, that fixes a single edge on a particular page

    # Intermediate variable X - whether two edges belong to the same page

    # Planarity rule for edges on the same page

    return cnf
