import networkx as nx

# Diamond and manta ray graphs (named by me)
# Source: https://link.springer.com/article/10.1007/BF00563521
diamond_graph = nx.DiGraph()
diamond_graph.add_edges_from([
    (0, 1), (0, 3), (0, 5),
    (2, 1), (2, 3),
    (4, 3), (4, 5),
    (1, 8), (1, 6),
    (3, 6), (3, 7), (3, 8),
    (5, 7), (5, 8),
])

manta_ray_graph = nx.DiGraph()
manta_ray_graph.add_edges_from([
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
    (1, 10),
    (2, 10),
    (3, 7), (3, 8),
    (4, 8), (4, 9),
    (5, 11),
    (6, 11),
    (7, 10),
    (8, 10), (8, 11),
    (9, 11),
    (10, 12),
    (11, 12)
])