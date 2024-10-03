from pathlib import Path
from math import log, ceil
import networkx as nx
import matplotlib.pyplot as plt

graphs_dir = Path(__file__).resolve().parent.parent / 'graphs'

def write_graph_to_file(n, edges, prefix):
    with open(graphs_dir / f'{prefix}_{n}.graph', 'w') as file:
        file.write(f'{n}\n')
        for u, v in edges:
            file.write(f'{u} {v}\n')

def write_tree_img_to_file(n, tree):
    s = ceil(log(n) / log(2))
    plt.figure(figsize=(s * 4, s * 3))
    pos = nx.spring_layout(tree)
    nx.draw(tree, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, font_size=10)
    name = f'tree_{n}'
    plt.title(name)
    plt.savefig(graphs_dir / f'{name}.png')

# Generate snakes
for i in range(10):
    n = 2 ** (i+1)
    edges = [(i, i + 1) for i in range(1, n)]
    write_graph_to_file(n, edges, 'snake')

# Generate trees
for i in range(1, 10):
    n = 2 ** (i+1)
    tree = nx.random_tree(n)
    edges = list(tree.edges())
    write_graph_to_file(n, edges, 'tree')
    write_tree_img_to_file(n, tree)
