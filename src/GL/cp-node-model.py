from ortools.sat.python import cp_model

def solve_graceful_labeling(n, edges):
    """
    Solve the graceful labeling problem for a graph with n nodes and given edges.
    Each node is assigned a label from 0 to q (q = number of edges) such that:
      - All node labels are different.
      - For each edge (i, j), the absolute difference |x_i - x_j| is computed,
        and these differences (edge labels) are all different and take values 1..q.
    
    Args:
      n (int): Number of nodes.
      edges (List[Tuple[int, int]]): List of edges as (i, j) tuples.
    """
    q = len(edges)  # q is the number of edges
    model = cp_model.CpModel()
    
    # Create node variables: each x[i] has domain [0, q]
    x = [model.NewIntVar(0, q, f'x[{i}]') for i in range(n)]
    
    # Enforce that all node labels are distinct.
    model.AddAllDifferent(x)
    
    # Create an auxiliary variable for the absolute difference (edge label)
    # for each edge. Its domain is [1, q] (cannot be 0 because x[i] are all different).
    diffs = []
    for k, (i, j) in enumerate(edges):
        diff = model.NewIntVar(1, q, f'diff[{k}]')
        # Add constraint: diff = |x[i] - x[j]|
        model.AddAbsEquality(diff, x[i] - x[j])
        diffs.append(diff)
    
    # Enforce that all edge differences are distinct.
    model.AddAllDifferent(diffs)
    
    # Create the solver and solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print('Graceful labeling found:')
        for i in range(n):
            print(f'  Node {i}: label = {solver.Value(x[i])}')
        print('Edge differences:')
        for k, (i, j) in enumerate(edges):
            print(f'  Edge ({i}, {j}): |{solver.Value(x[i])} - {solver.Value(x[j])}| = {solver.Value(diffs[k])}')
    else:
        print('No graceful labeling exists for this graph.')

# Example: a path graph with 4 nodes and 3 edges.
n = 4
edges = [(0, 1), (1, 2), (2, 3)]
solve_graceful_labeling(n, edges)
