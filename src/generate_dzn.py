import numpy as np
from helpers import rome_graphs

def generate_dzn(G, s, t, k, filename="graph_instance.dzn"):
    nodes = list(G.nodes())
    edges = list(G.edges())
    n = len(nodes)

    # Create adjacency matrix
    adj_matrix = np.zeros((n, n), dtype=bool)
    for u, v in edges:
        adj_matrix[nodes.index(u)][nodes.index(v)] = True  # Assuming nodes are 1-indexed

    # Create cover matrix (randomly initialized as False)
    cover_matrix = np.random.choice([True, False], size=(n, k), p=[0.3, 0.7])

    # Convert matrices to Minizinc format
    adj_flat = ", ".join(map(str, adj_matrix.flatten().tolist())).lower()
    cover_flat = ", ".join(map(str, cover_matrix.flatten().tolist())).lower()

    # Generate the .dzn file
    with open(filename, "w") as f:
        f.write(f"n = {n};\n")
        f.write(f"s = {s};\n")
        f.write(f"t = {t};\n")
        f.write(f"k = {k};\n")
        f.write(f"adj = array2d(1..{n}, 1..{n}, [{adj_flat}]);\n")
        f.write(f"cover = array2d(1..{n}, 1..{k}, [{cover_flat}]);\n")

    print(f"DZN file saved as {filename}")

for G in rome_graphs():
    if G.name == 'grafo263.11.gml':
        n = G.number_of_nodes()
        generate_dzn(G, s=1, t=n, k=5, filename=f'{G.name}.dzn')
        break