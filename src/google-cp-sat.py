import sys
from ortools.sat.python import cp_model
from helpers import T, north_graphs, random_dag_graphs
from encoders import verify_2UBE
from graph_generators import generate_path_dag, generate_directed_cycle_graph, generate_complete_binary_arborescence, generate_tournament_dag, random_dag_with_density, generate_grid_dag

def solve(n, edges):
    # Create the model
    model = cp_model.CpModel()

    m = len(edges)

    # Variables
    pos_of_node = [model.NewIntVar(0, n - 1, f'pos_{i}') for i in range(n)]
    page_of_edge = [model.NewBoolVar(f'edge_page_{i}') for i in range(m)]

    # All-Different constraint for positions
    model.AddAllDifferent(pos_of_node)

    # Constraints for directed edges
    for u, v in edges:
        model.Add(pos_of_node[u] < pos_of_node[v])

    # Non-overlapping edges on the same page
    for i, (u, v) in enumerate(edges):
        for j, (w, x) in enumerate(edges):
            if i != j and len(set([u, v, w, x])) == 4: # pairwise different
                # pi = page_of_edge[i]
                # pj = page_of_edge[j]

                # overlap1 = pos_of_node[u] < pos_of_node[w] < pos_of_node[v] < pos_of_node[x]
                # overlap2 = pos_of_node[w] < pos_of_node[u] < pos_of_node[x] < pos_of_node[v]

                # model.AddBoolAnd(not overlap1, not overlap2).OnlyEnforceIf(pi == pj)

                # Create auxiliary Boolean variables for overlap conditions
                overlap1 = model.NewBoolVar(f'overlap1_{u}_{v}_{w}_{x}')
                overlap2 = model.NewBoolVar(f'overlap2_{u}_{v}_{w}_{x}')

                # Create Boolean variables for individual comparisons
                u_lt_w = model.NewBoolVar(f'u_lt_w_{u}_{w}')
                w_lt_v = model.NewBoolVar(f'w_lt_v_{w}_{v}')
                v_lt_x = model.NewBoolVar(f'v_lt_x_{v}_{x}')
                
                w_lt_u = model.NewBoolVar(f'w_lt_u_{w}_{u}')
                u_lt_x = model.NewBoolVar(f'u_lt_x_{u}_{x}')
                x_lt_v = model.NewBoolVar(f'x_lt_v_{x}_{v}')

                # Define conditions for overlap1: pos[u] < pos[w] < pos[v] < pos[x]
                model.Add(pos_of_node[u] < pos_of_node[w]).OnlyEnforceIf(u_lt_w)
                model.Add(pos_of_node[u] >= pos_of_node[w]).OnlyEnforceIf(u_lt_w.Not())

                model.Add(pos_of_node[w] < pos_of_node[v]).OnlyEnforceIf(w_lt_v)
                model.Add(pos_of_node[w] >= pos_of_node[v]).OnlyEnforceIf(w_lt_v.Not())

                model.Add(pos_of_node[v] < pos_of_node[x]).OnlyEnforceIf(v_lt_x)
                model.Add(pos_of_node[v] >= pos_of_node[x]).OnlyEnforceIf(v_lt_x.Not())

                # Define overlap1 as a conjunction of the above conditions
                model.AddBoolAnd([u_lt_w, w_lt_v, v_lt_x]).OnlyEnforceIf(overlap1)
                model.AddBoolOr([u_lt_w.Not(), w_lt_v.Not(), v_lt_x.Not()]).OnlyEnforceIf(overlap1.Not())

                # Define conditions for overlap2: pos[w] < pos[u] < pos[x] < pos[v]
                model.Add(pos_of_node[w] < pos_of_node[u]).OnlyEnforceIf(w_lt_u)
                model.Add(pos_of_node[w] >= pos_of_node[u]).OnlyEnforceIf(w_lt_u.Not())

                model.Add(pos_of_node[u] < pos_of_node[x]).OnlyEnforceIf(u_lt_x)
                model.Add(pos_of_node[u] >= pos_of_node[x]).OnlyEnforceIf(u_lt_x.Not())

                model.Add(pos_of_node[x] < pos_of_node[v]).OnlyEnforceIf(x_lt_v)
                model.Add(pos_of_node[x] >= pos_of_node[v]).OnlyEnforceIf(x_lt_v.Not())

                # Define overlap2 as a conjunction of the above conditions
                model.AddBoolAnd([w_lt_u, u_lt_x, x_lt_v]).OnlyEnforceIf(overlap2)
                model.AddBoolOr([w_lt_u.Not(), u_lt_x.Not(), x_lt_v.Not()]).OnlyEnforceIf(overlap2.Not())

                # Non-overlap condition: If on the same page, no overlap
                same_page = model.NewBoolVar(f'same_page_{i}_{j}')
                model.Add(page_of_edge[i] == page_of_edge[j]).OnlyEnforceIf(same_page)
                model.Add(page_of_edge[i] != page_of_edge[j]).OnlyEnforceIf(same_page.Not())

                model.AddImplication(same_page, overlap1.Not())
                model.AddImplication(same_page, overlap2.Not())

    # Solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output results
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution found:")
        # Retrieve and sort nodes by position
        node_positions = [(i, solver.Value(pos_of_node[i])) for i in range(n)]
        node_positions.sort(key=lambda x: x[1])  # Sort by position value
        order = [node for node, pos in node_positions]
        # print(" ".join(map(str, order)))
        return (order, [solver.Value(page) for page in page_of_edge])
    else:
        print("No solution found.")

# # # Example usage
G = generate_grid_dag(10, 10)
edges = list(G.edges())
print(edges)
# n = G.number_of_nodes()

# T.start('Solve')
# node_order, edge_assignment = solve(n, edges)
# T.stop('Solve')

# print(node_order)
# print(edge_assignment)

# # p1_edges = [edges[i] for i, page in enumerate(edge_assignment) if page == 0]
# # p2_edges = [edges[i] for i, page in enumerate(edge_assignment) if page == 1]

# # print(" ".join(map(lambda x: f"{x[0]}-{x[1]}", p1_edges)))
# # print(" ".join(map(lambda x: f"{x[0]}-{x[1]}", p2_edges)))

# print('Correct:', verify_2UBE(G, node_order, edge_assignment))

# # cp1: 30 seconds for 8x8

# for n in range(20, 29):
#     G = generate_grid_dag(n, n)
#     edges = list(G.edges())
#     node_count = G.number_of_nodes()

#     print('Solving for', n)

#     T.start('Solve')
#     node_order, edge_assignment = solve(node_count, edges)
#     T.stop('Solve')

#     print('Correct:', verify_2UBE(G, node_order, edge_assignment))
#     print('='*50)


# i = 0

# for G in random_dag_graphs():
#     i += 1

#     print(f"Working on graph {i}", file=sys.stderr)

#     edges = [(int(u[1:]), int(v[1:])) for u, v in G.edges()]
#     node_count = G.number_of_nodes()

#     T.start(G.name)
#     solution = solve(node_count, edges)
#     T.stop(G.name)

#     if solution:
#         node_order, edge_assignment = solution
#         print('Correct:', verify_2UBE(G, node_order, edge_assignment))
    
#     print('---')
