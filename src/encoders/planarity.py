from pysat.formula import CNF
import networkx as nx

def planarity_cnf(graph):
    """
    Does not work.
    
    :param graph: A networkx graph.
    :return: CNF object representing the SAT problem.
    """
    cnf = CNF()
    V = len(graph.nodes)
    edges = [tuple(sorted((int(u), int(v)))) for u, v in graph.edges()]
    left_vars = {}

    # Create variables for left relationships Lx_uv
    var_count = 1
    for x in range(V):
        for u in range(V):
            for v in range(u+1, V):
                left_vars[(x, u, v)] = var_count
                var_count += 1
    
    L = lambda x, a, b: left_vars[(x, a, b)] if a <= b else -left_vars[(x, b, a)]

    # cycles = nx.cycle_basis(graph)
    cycles = nx.simple_cycles(graph)

    # Vertex x is inside abc cycle:
    # Lxab and Lxbc and Lxca
    
    # Vertex x is outside abc cycle:
    # Lxba or Lxcb or Lxac

    # Vertex x is inside or outside of abc cycle:
    # (Lxab and Lxbc and Lxca) or (Lxba or Lxcb or Lxac)
    
    # Vertex must be inside or outside any given cycle.
    for x in range(V):
        for cycle in cycles:
            common = []
            for i in range(len(cycle)):
                u, v = int(cycle[i-1]), int(cycle[i])
                common.append(L(x, v, u))

            for i in range(len(cycle)):
                u, v = int(cycle[i-1]), int(cycle[i])
                cnf.append(common + [L(x, u, v)])

    # No edge crossings
    # not (L(cba) and L(dab) and L(dac) and L(dcb))
    # and
    # not (L(cab) and L(dba) and L(dca) and L(dbc))
    for (a, b) in edges:
        for (c, d) in edges:
            if len(set([a, b, c, d])) == 4:
                cnf.append([-L(c,b,a), -L(d,a,b), -L(d,a,c), -L(d,c,b)])
                cnf.append([-L(c,a,b), -L(d,b,a), -L(d,c,a), -L(d,b,c)])

    return cnf
