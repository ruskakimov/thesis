from pysat.formula import CNF

def book_embedding_cnf(graph, P):
    """
    SAT encodes book embedding for P pages.
    Based on "Vertex-edge encoding" (Kraayenbrink, 2011).

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

    cnf = CNF()
    N = len(graph.nodes)
    M = len(graph.edges())

    return CNF
