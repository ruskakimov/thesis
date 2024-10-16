from pysat.formula import CNF
from itertools import combinations

def book_embedding_cnf(graph, P):
    cnf = CNF()

    # Number of vertices and edges
    vertices = list(graph.nodes)
    edges = list(graph.edges)
    n = len(vertices)
    m = len(edges)

    # Step 1: Asymmetric relative ordering of vertices on the spine
    # Variables σ(vi, vj) -> vi is before vj on the spine
    def sigma(i, j):
        return i * n + j + 1

    # Asymmetry: σ(vi, vj) <-> ¬σ(vj, vi)
    for i, j in combinations(range(n), 2):
        cnf.append([sigma(i, j), sigma(j, i)])  # Either σ(vi, vj) or σ(vj, vi)
        cnf.append([-sigma(i, j), -sigma(j, i)])  # Both can't be true

    # Step 2: Transitivity of σ
    # σ(vi, vj) ∧ σ(vj, vk) -> σ(vi, vk)
    for i, j, k in combinations(range(n), 3):
        cnf.append([-sigma(i, j), -sigma(j, k), sigma(i, k)])

    # Step 3: Page assignment for each edge
    # Variables φq(ei) -> edge ei is assigned to page q
    def phi(edge, page):
        idx = edges.index(edge)
        return m * page + idx + 1

    # Each edge should be assigned to exactly one page
    for edge in edges:
        cnf.append([phi(edge, p) for p in range(P)])

    # Step 4: No crossings on the same page
    for (vi, vj), (vk, vl) in combinations(edges, 2):
        for p in range(P):
            cnf.append([-phi((vi, vj), p), -phi((vk, vl), p), -sigma(min(vi, vk), max(vi, vk)), 
                        -sigma(min(vj, vl), max(vj, vl))])

    return cnf

def _book_embedding_cnf(graph, P):
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

    # TODO: See if enforcing order for edges (u < w) reduces encoding for forbidden orders below

    # Rule: Transitivity rule must hold
    # Lij and Ljk -> Lik
    # CNF form: Lik | ~Lij | ~Ljk
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if i != j and i != k and j != k:
                    cnf.append([-L(i,j), -L(j,k), L(i,k)])
    
    # TODO: The search space of possible satisfying assignments can be reduced by choosing a particular vertex as the first vertex along the spine
    
    edge_to_page = {}
    for i in range(M):
        for p in range(P):
            variable_count += 1
            edge_to_page[(i, p)] = variable_count

    # Variable: Whether edge with index i is assigned to page p
    EP = lambda i, p: edge_to_page[(i, p)]

    # Rule: Every edge is assigned to at least 1 page
    for i in range(M):
        clause = [EP(i, p) for p in range(P)]
        cnf.append(clause)
    
    # # TODO: Test if improves perf
    # # 1 edge to only 1 page
    # for i in range(M):
    #     for p1 in range(P):
    #         for p2 in range(p1+1, P):
    #             cnf.append([-EP(i, p1), -EP(i, p2)])

    # TODO: We can again reduce the search space by the fixed page assignment rule, that fixes a single edge on a particular page

    # Variable: Intermediate variable X - whether two edges belong to the same page
    edges_cross = {}
    for i in range(M):
        for j in range(i+1, M):
            variable_count += 1
            edges_cross[(i, j)] = variable_count
    X = lambda i, j: edges_cross[(i, j)] if i < j else edges_cross[(j, i)]

    # Rule: Enforce correct values for X (only true if both edges are assigned to the same page)
    # (EPi1 and EPj1) or (EPi2 and EPj2) or ... or (EPip and EPjp) -> Xij
    # EPi1 and EPj1 -> Xij
    # not (EPi1 and EPj1) or Xij
    # not EPi1 or not EPj1 or Xij
    # -EPi1, -EPj1, Xij
    for i in range(M):
        for j in range(i+1, M):
            for p in range(P):
                cnf.append([X(i, j), -EP(i, p), -EP(j, p)])

    # Rule: Planarity rule for edges on the same page
    #
    # for any 2 edges where i,j,k,l are pairwise different
    # forbidden orders (with crossing):
    # i k j l
    # i l j k
    # j k i l
    # j l i k
    # k i l j
    # k j l i
    # l i k j
    # l j k i
    #
    # Xijkl ->
    # not (Lik and Lkj and Ljl) and
    # ... same for all forbidden orders ijkl
    #
    # Xijkl -> not (Lik and Lkj and Ljl)
    # not Xijkl or not (Lik and Lkj and Ljl)
    # -Xijkl, -Lik, -Lkj, -Ljl
    for a in range(M):
        for b in range(i+1, M):
            i, j = edges[a]
            k, l = edges[b]

            cnf.append([[-X(i, j), -L(i, k), -L(k, j), -L(j, l)]]) # i, k, j, l
            cnf.append([[-X(i, j), -L(j, k), -L(k, i), -L(i, l)]]) # j, k, i, l
            cnf.append([[-X(i, j), -L(i, l), -L(l, j), -L(j, k)]]) # i, l, j, k
            cnf.append([[-X(i, j), -L(j, l), -L(l, i), -L(i, k)]]) # j, l, i, k

            cnf.append([[-X(i, j), -L(k, i), -L(i, l), -L(l, j)]]) # k, i, l, j
            cnf.append([[-X(i, j), -L(l, i), -L(i, k), -L(k, j)]]) # l, i, k, j
            cnf.append([[-X(i, j), -L(k, j), -L(j, l), -L(l, i)]]) # k, j, l, i
            cnf.append([[-X(i, j), -L(l, j), -L(j, k), -L(k, i)]]) # l, j, k, i
    
    return cnf

# Notes:
#
# Implication X -> Y is encoded like this in CNF
# not X or Y
#
# X Y X->Y
# 0 0  1
# 0 1  1
# 1 0  0
# 1 1  1
#
# Main it forbids the case where X is true and Y isn't
# if X is true, Y is true
# but if X is false, no restriction on Y