from pysat.formula import CNF
from functools import cmp_to_key

def book_embedding_cnf(graph, P):
    """
    SAT encodes book embedding for P pages.
    Based on Bekos encoding (2015).

    Number of variables = n^2 + m^2 + pm
    Number of clauses = n^3 + m^2
    """

    cnf = CNF()
    edges = list(graph.edges())
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
    edges_on_same_page = {}
    for i in range(M):
        for j in range(i+1, M):
            variable_count += 1
            edges_on_same_page[(i, j)] = variable_count
    X = lambda i, j: edges_on_same_page[(i, j)] if i < j else edges_on_same_page[(j, i)]

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
        for b in range(a+1, M):
            i, j = edges[a]
            k, l = edges[b]
            # 1i 2j
            # 3k 4l
            # 3k 2j 4l 1i
            # k j l i
            
            if len(set([i, j, k, l])) == 4: # pairwise different
                cnf.append([-X(a, b), -L(i, k), -L(k, j), -L(j, l)]) # i, k, j, l
                cnf.append([-X(a, b), -L(j, k), -L(k, i), -L(i, l)]) # j, k, i, l
                cnf.append([-X(a, b), -L(i, l), -L(l, j), -L(j, k)]) # i, l, j, k
                cnf.append([-X(a, b), -L(j, l), -L(l, i), -L(i, k)]) # j, l, i, k

                cnf.append([-X(a, b), -L(k, i), -L(i, l), -L(l, j)]) # k, i, l, j
                cnf.append([-X(a, b), -L(l, i), -L(i, k), -L(k, j)]) # l, i, k, j
                cnf.append([-X(a, b), -L(k, j), -L(j, l), -L(l, i)]) # k, j, l, i

                # if i == 1 and j == 2 and k == 3 and l == 4:
                #     print(a, b, [-X(i, j), -L(k, j), -L(j, l), -L(l, i)])

                cnf.append([-X(a, b), -L(l, j), -L(j, k), -L(k, i)]) # l, j, k, i
    
    return cnf

def decode_book_embedding(graph, P, solution):
    if not solution:
        return
    
    vertices = list(graph.nodes)
    edges = list(graph.edges)
    N = len(vertices)
    M = len(edges)

    var_count = N*(N-1)/2 + M*P + M*(M-1)/2
    assert len(solution) == var_count

    values = {}
    for var in solution:
        values[abs(var)] = var > 0
        values[-abs(var)] = var < 0
    
    print([values[v] for v in [-40, 8, -9, 7]])

    variable_count = 0
    
    is_left_to = {}
    for i in range(N):
        for j in range(i+1, N):
            variable_count += 1
            is_left_to[(i, j)] = variable_count
            is_left_to[(j, i)] = -variable_count
    
    for i in range(N):
        print(f'V{i} is to the left of: ', end='')
        for j in range(N):
            if i == j:
                continue
            var_idx = is_left_to[(i, j)]
            if values[var_idx]:
                print(f'V{j} ', end='')
        print()
    
    print()
    
    vertices.sort(key=cmp_to_key(lambda i, j: -1 if values[is_left_to[(i, j)]] else 1))
    print('Book spine:', vertices)
    print()

    edge_to_page = {}
    for i in range(M):
        for p in range(P):
            variable_count += 1
            edge_to_page[(i, p)] = variable_count
    
    for i in range(M):
        pages = [str(p) for p in range(P) if values[edge_to_page[(i,p)]]]
        pages_str = ', '.join(pages)
        u, v = edges[i]
        print(f'E{i} (V{u}, V{v}) belongs to pages {pages_str}')

    print()

    same_page = []
    
    edges_on_same_page = {}
    for i in range(M):
        for j in range(i+1, M):
            variable_count += 1
            edges_on_same_page[(i, j)] = variable_count
    X = lambda i, j: edges_on_same_page[(i, j)] if i < j else edges_on_same_page[(j, i)]

    print(X(4,9), X(9,4))
    
    for i in range(M):
        pages = [f'E{j}' for j in range(M) if i != j and values[X(i,j)]]
        pages_str = ', '.join(pages)
        u, v = edges[i]
        print(f'E{i} is on the same page with {pages_str}')
    
    print('  '.join(same_page))

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