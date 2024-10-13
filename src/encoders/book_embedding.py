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
            is_left_to[(i, j)] = variable_count
            variable_count += 1

    # Whether vertex i is to the left of vertex j along the book spine
    L = lambda i, j: is_left_to[(i, j)] if i < j else -is_left_to[(j, i)]

    # Encode transitivity of L
    

    return CNF
