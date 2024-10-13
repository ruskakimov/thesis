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

    return CNF
