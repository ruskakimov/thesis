from pysat.formula import CNF
from pysat.solvers import Solver
from functools import cmp_to_key

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
    
    # Assign 1 edge to top page
    cnf.append([TOP(0)])
    
    return cnf


# Returns node order and edge assignment
def solve_2UBE_SAT(digraph):
    cnf = encode_2UBE(digraph)
    with Solver('Maplesat', bootstrap_with=cnf) as solver:
        sat_result = solver.solve()
        if not sat_result:
            return None, None
        else:
            model = solver.get_model()
            N = len(digraph.nodes)
            M = len(digraph.edges())
            L, TOP = get_variables(N)

            value_of = {}
            for var in model:
                value_of[abs(var)] = var > 0
                value_of[-abs(var)] = var < 0
            
            nodes = list(digraph.nodes)

            node_order = list(range(N))
            node_order.sort(key=cmp_to_key(lambda i, j: -1 if value_of[L(i, j)] else 1))

            node_order = [nodes[i] for i in node_order]

            edge_assignment = [+value_of[TOP(i)] for i in range(M)]

            return node_order, edge_assignment



def verify_2UBE(G, node_order, edge_assignment):
    edges = list(G.edges())
    p1_edges = [edges[i] for i, page in enumerate(edge_assignment) if page == 0]
    p2_edges = [edges[i] for i, page in enumerate(edge_assignment) if page == 1]

    pos_of_node = {node: i for i, node in enumerate(node_order)}

    assert len(p1_edges) + len(p2_edges) == len(edges)
    
    for page_edges in [p1_edges, p2_edges]:
        for i, (u, v) in enumerate(page_edges):
            for j, (w, x) in enumerate(page_edges):
                if i != j and len(set([u, v, w, x])) == 4:
                    overlap1 = pos_of_node[u] < pos_of_node[w] < pos_of_node[v] < pos_of_node[x]
                    overlap2 = pos_of_node[w] < pos_of_node[u] < pos_of_node[x] < pos_of_node[v]
                    if overlap1 or overlap2:
                        print(f"Overlap: {u}-{v} and {w}-{x}")
                        return False
    return True
