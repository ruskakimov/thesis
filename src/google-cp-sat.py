from ortools.sat.python import cp_model


def encode_graph_constraints(n, edges):
    # Create the model
    model = cp_model.CpModel()

    m = len(edges)

    # Variables
    pos = [model.NewIntVar(0, n - 1, f'pos_{i}') for i in range(n)]  # Node positions
    page = [model.NewBoolVar(f'edge_page_{i}') for i in range(m)]    # Page assignments

    # All-Different constraint for positions
    model.AddAllDifferent(pos)

    # Constraints for directed edges
    for u, v in edges:
        # Enforce directionality: pos[u] < pos[v]
        model.Add(pos[u] < pos[v])

    # Non-overlapping edges on the same page
    for i, (u, v) in enumerate(edges):
        for j, (w, x) in enumerate(edges):
            if i != j:
                # Overlap condition
                overlap1 = pos[u] < pos[w] < pos[v] < pos[x]
                overlap2 = pos[w] < pos[u] < pos[x] < pos[v]

                model.AddImplication(page[i] == page[j], not overlap1 and not overlap2)

    # Solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output results
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution found:")
        for i in range(n):
            print(f'Node {i}: pos={solver.Value(pos[i])}, page={solver.Value(page[i])}')
    else:
        print("No solution found.")

# Example usage
n = 4  # Number of nodes
edges = [(0, 1), (1, 2), (2, 3), (0, 2)]  # Directed edges
encode_graph_constraints(n, edges)
