from pysat.formula import CNF
from pysat.solvers import Solver
from functools import cmp_to_key

def get_variables(N, M, P):
    variable_count = 0
    
    is_left_to = {}
    for i in range(N):
        for j in range(i+1, N):
            variable_count += 1
            is_left_to[(i, j)] = variable_count
    
    # Variable: Whether vertex i is to the left of vertex j along the book spine
    L = lambda i, j: is_left_to[(i, j)] if i < j else -is_left_to[(j, i)]

    edge_to_page = {}
    for i in range(M):
        for p in range(P):
            variable_count += 1
            edge_to_page[(i, p)] = variable_count
    
    # Variable: Whether edge with index i is assigned to page p
    EP = lambda i, p: edge_to_page[(i, p)]

    edges_on_same_page = {}
    for i in range(M):
        for j in range(i+1, M):
            variable_count += 1
            edges_on_same_page[(i, j)] = variable_count

    # Intermediate variable: Whether two edges belong to the same page
    X = lambda i, j: edges_on_same_page[(i, j)] if i < j else edges_on_same_page[(j, i)]

    return (L, EP, X)

def encode_book_embedding(graph, P):
    """
    SAT encodes book embedding for P pages.
    Based on Bekos encoding (2015).

    Number of variables = n^2 + m^2 + pm
    Number of clauses = n^3 + m^2
    """

    cnf = CNF()
    nodes = list(graph.nodes)
    edges = list(graph.edges())
    N = len(graph.nodes)
    M = len(edges)

    node_index = {nodes[i]: i for i in range(N)}

    L, EP, X = get_variables(N, M, P)

    # TODO: See if enforcing order for edges (u < w) reduces encoding for forbidden orders below

    # Rule: Transitivity rule must hold
    # Lij and Ljk -> Lik
    # CNF form: Lik | ~Lij | ~Ljk
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if i != j and i != k and j != k:
                    cnf.append([-L(i,j), -L(j,k), L(i,k)])

    # Space reduction: set V0 as first vertex on the spine
    for i in range(1, N):
        cnf.append([L(0,i)])
    
    # Space reduction: assume V1 is left of V2
    if N >= 3:
        cnf.append([L(1, 2)])

    # Rule: Every edge is assigned to at least 1 page
    for i in range(M):
        clause = [EP(i, p) for p in range(P)]
        cnf.append(clause)
    
    # TODO: Test if improves perf
    # 1 edge to only 1 page
    for i in range(M):
        for p1 in range(P):
            for p2 in range(p1+1, P):
                cnf.append([-EP(i, p1), -EP(i, p2)])

    # Space reduction: set edge 0 to page 0
    # cnf.append([EP(0, 0)])
    # for p in range(1, P):
    #     cnf.append([-EP(0, p)])

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
            i, j = map(lambda x: node_index[x], edges[a])
            k, l = map(lambda x: node_index[x], edges[b])
            
            if len(set([i, j, k, l])) == 4: # pairwise different
                cnf.append([-X(a, b), -L(i, k), -L(k, j), -L(j, l)]) # i, k, j, l
                cnf.append([-X(a, b), -L(j, k), -L(k, i), -L(i, l)]) # j, k, i, l
                cnf.append([-X(a, b), -L(i, l), -L(l, j), -L(j, k)]) # i, l, j, k
                cnf.append([-X(a, b), -L(j, l), -L(l, i), -L(i, k)]) # j, l, i, k

                cnf.append([-X(a, b), -L(k, i), -L(i, l), -L(l, j)]) # k, i, l, j
                cnf.append([-X(a, b), -L(l, i), -L(i, k), -L(k, j)]) # l, i, k, j
                cnf.append([-X(a, b), -L(k, j), -L(j, l), -L(l, i)]) # k, j, l, i
                cnf.append([-X(a, b), -L(l, j), -L(j, k), -L(k, i)]) # l, j, k, i
    
    return cnf

def encode_upward_book_embedding(digraph, P):
    """
    SAT encodes Upward Book Embedding for P pages.
    """

    cnf = CNF()
    nodes = list(digraph.nodes)
    edges = list(digraph.edges())
    N = len(digraph.nodes)
    M = len(edges)

    node_index = {nodes[i]: i for i in range(N)}

    L, EP, X = get_variables(N, M, P)

    # Rule: Transitivity rule must hold
    # Lij and Ljk -> Lik
    # CNF form: Lik | ~Lij | ~Ljk
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if i != j and i != k and j != k:
                    cnf.append([-L(i,j), -L(j,k), L(i,k)])
    
    # Rule: Nodes are topologically ordered
    for u, v in edges:
        i = node_index[u]
        j = node_index[v]
        cnf.append([L(i, j)])

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

    # Space reduction: set edge 0 to page 0
    # cnf.append([EP(0, 0)])
    # for p in range(1, P):
    #     cnf.append([-EP(0, p)])

    # Rule: Enforce correct values for X (only true if both edges are assigned to the same page)
    for i in range(M):
        for j in range(i+1, M):
            for p in range(P):
                cnf.append([X(i, j), -EP(i, p), -EP(j, p)])

    # Rule: Planarity rule for edges on the same page
    for a in range(M):
        for b in range(a+1, M):
            i, j = map(lambda x: node_index[x], edges[a])
            k, l = map(lambda x: node_index[x], edges[b])
            
            if len(set([i, j, k, l])) == 4: # pairwise different
                cnf.append([-X(a, b), -L(i, k), -L(k, j), -L(j, l)]) # i, k, j, l
                cnf.append([-X(a, b), -L(j, k), -L(k, i), -L(i, l)]) # j, k, i, l
                cnf.append([-X(a, b), -L(i, l), -L(l, j), -L(j, k)]) # i, l, j, k
                cnf.append([-X(a, b), -L(j, l), -L(l, i), -L(i, k)]) # j, l, i, k

                cnf.append([-X(a, b), -L(k, i), -L(i, l), -L(l, j)]) # k, i, l, j
                cnf.append([-X(a, b), -L(l, i), -L(i, k), -L(k, j)]) # l, i, k, j
                cnf.append([-X(a, b), -L(k, j), -L(j, l), -L(l, i)]) # k, j, l, i
                cnf.append([-X(a, b), -L(l, j), -L(j, k), -L(k, i)]) # l, j, k, i
    
    return cnf

def decode_book_embedding(graph, P, solution):
    if not solution:
        return
    
    vertices = list(graph.nodes)
    edges = list(graph.edges)
    N = len(vertices)
    M = len(edges)

    # var_count = N*(N-1)/2 + M*P + M*(M-1)/2
    # assert len(solution) == var_count

    L, EP, X = get_variables(N, M, P)

    value_of = {}
    for var in solution:
        value_of[abs(var)] = var > 0
        value_of[-abs(var)] = var < 0
    
    # print('Vertex is to the left of:')
    # for i in range(N):
    #     right_vertices = [f'v{j}' for j in range(N) if i != j and value_of[L(i, j)]]
    #     right_vertices_str = ', '.join(right_vertices)
    #     print(f'v{i} - {right_vertices_str}')
    # print()
    
    print('Book spine vertex order:')
    vertices.sort(key=cmp_to_key(lambda i, j: -1 if value_of[L(i, j)] else 1))
    vertices_str = ', '.join(f'v{i}' for i in vertices)
    print(vertices_str)
    print()
    
    print('Edge to page assignment:')
    by_pages = [[] for _ in range(P)]
    for i in range(M):
        pages = [f'p{p}' for p in range(P) if value_of[EP(i, p)]]
        pages_str = ', '.join(pages)
        u, v = edges[i]
        print(f'e{i} (v{u}, v{v}) - {pages_str}')
        by_pages[int(pages_str[1:])].append((u,v))
    # print()

    return (vertices, by_pages)
    
    # print('Edge is on the same page with:')
    # for i in range(M):
    #     pages = [f'e{j}' for j in range(M) if i != j and value_of[X(i,j)]]
    #     pages_str = ', '.join(pages)
    #     print(f'e{i} - {pages_str}')
    # print()

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

def solve_kUBE_SAT(digraph, k):
    cnf = encode_upward_book_embedding(digraph, k)
    with Solver('Maplesat', bootstrap_with=cnf) as solver:
        sat_result = solver.solve()
        if not sat_result:
            return None, None
        else:
            model = solver.get_model()
            N = len(digraph.nodes)
            M = len(digraph.edges())
            L, EP, X = get_variables(N, M, k)

            value_of = {}
            for var in model:
                value_of[abs(var)] = var > 0
                value_of[-abs(var)] = var < 0

            node_order = list(digraph.nodes)
            node_order.sort(key=cmp_to_key(lambda i, j: -1 if value_of[L(i, j)] else 1))

            edge_assignment = [0] * M
            for i in range(M):
                for p in range(k):
                    if value_of[EP(i, p)]:
                        edge_assignment[i] = p
                        break

            return node_order, edge_assignment
        