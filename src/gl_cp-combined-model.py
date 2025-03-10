import networkx as nx
import sys
from ortools.sat.python import cp_model
from helpers import T, rome_graphs

def solve_graceful_labeling_combined(n, edges):
    """
    Solve the graceful labeling problem using the combined model.
    
    For a graph with n nodes and given edges, let q = number of edges.
    - Each node i gets a label x[i] in [0, q].
    - For each edge k = (i,j), define d[k] = |x[i] - x[j]|, with d[k] in [1, q].
    - Enforce AllDifferent(x) and AllDifferent(d).
    - Define d_prime[k] = d[k] - 1, so d_prime[k] in [0, q-1].
    - Create dual variables y[j] (j = 0,...,q-1) with domain [0, q-1].
    - Add the inverse constraint: model.AddInverse(d_prime, y)
      which enforces that for every j, d_prime[y[j]] = j.
    """
    q = len(edges)
    model = cp_model.CpModel()
    
    # 1. Node variables: x[i] in [0, q]
    x = [model.NewIntVar(0, q, f'x[{i}]') for i in range(n)]
    model.AddAllDifferent(x)
    
    # 2. Edge difference variables: d[k] in [1, q]
    d = []
    for k, (i, j) in enumerate(edges):
        diff = model.NewIntVar(1, q, f'd[{k}]')
        model.AddAbsEquality(diff, x[i] - x[j])
        d.append(diff)
    model.AddAllDifferent(d)
    
    # 3. Create auxiliary variables: d_prime[k] = d[k] - 1, so d_prime[k] in [0, q-1]
    d_prime = []
    for k in range(q):
        dp = model.NewIntVar(0, q - 1, f'd_prime[{k}]')
        model.Add(d[k] == dp + 1)
        d_prime.append(dp)
    
    # 4. Dual variables: y[j] in [0, q-1] for each j in 0..q-1
    y = [model.NewIntVar(0, q - 1, f'y[{j}]') for j in range(q)]
    
    # 5. Add inverse constraint: for each j, d_prime[y[j]] = j.
    model.AddInverse(d_prime, y)
    
    # Optional: You can set decision strategies if desired.
    # For example, prioritize node variables:
    # model.AddDecisionStrategy(x, cp_model.CHOOSE_FIRST, cp_model.SELECT_MIN_VALUE)
    
    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print("SAT")
        print([solver.Value(x[i]) for i in range(n)])
        # for i in range(n):
        #     print(f"  Node {i}: label = {solver.Value(x[i])}")
        # print("Edge differences:")
        # for k, (i, j) in enumerate(edges):
        #     print(f"  Edge ({i}, {j}): |{solver.Value(x[i])} - {solver.Value(x[j])}| = {solver.Value(d[k])}")
        # print("Dual variables (inverse mapping):")
        # for j in range(q):
        #     print(f"  y[{j}] = {solver.Value(y[j])}  ->  d_prime[{solver.Value(y[j])}] = {solver.Value(d_prime[solver.Value(y[j])])} (should equal {j})")
    else:
        print("UNSAT")

# # Example: a path graph with 4 nodes and 3 edges.
# n = 4
# edges = [(0, 1), (1, 2), (2, 3)]
# solve_graceful_labeling_combined(n, edges)

i = 1

for G in rome_graphs():
    n = G.number_of_nodes()
    if n <= 20:
        print(f"Working on graph {i}", file=sys.stderr)
        i += 1
        nodes = list(G.nodes())
        edges = [(nodes.index(u), nodes.index(v)) for u,v in G.edges()]
        T.start(G.name)
        solve_graceful_labeling_combined(n, edges)
        T.stop(G.name)
        print('-' * 30)
