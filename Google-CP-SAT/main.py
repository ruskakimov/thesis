from ortools.sat.python import cp_model

def solve_graph(n, edges):
    m = len(edges)
    model = cp_model.CpModel()
    labels = [None] * n

    for i in range(n):
        # Label for node i
        labels[i] = model.new_int_var(0, m, f"label_{i}")
    
    # Labels must be unique
    for i in range(n):
        for j in range(i+1, n):
            model.add(labels[i] != labels[j])

    edge_weights = [None] * m

    for i in range(m):
        a, b = edges[i]
        edge_weights[i] = model.new_int_var(1, m, f"edge_{a}_{b}")
        model.AddAbsEquality(edge_weights[i], labels[a] - labels[b])
    
    # Edges must be unique
    for i in range(m):
        for j in range(i+1, m):
            model.add(edge_weights[i] != edge_weights[j])
    
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Time taken: {solver.WallTime()} seconds')
        for i in range(n):
            print(f"label for node {i} is {solver.value(labels[i])}")
    else:
        print("No solution found.")

def path_edges(n):
    return [(i, i + 1) for i in range(n - 1)]

# 3 path graph (0.005s)
# solve_graph(3, path_edges(3))

# 100 path graph (1s)
# solve_graph(100, path_edges(100))

# 1000 path graph (426s)
# solve_graph(1000, path_edges(1000))