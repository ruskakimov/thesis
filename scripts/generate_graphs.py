from pathlib import Path

graphs_dir = Path(__file__).resolve().parent.parent / 'graphs'

def write_graph_to_file(n, edges, prefix):
    with open(graphs_dir / f'{prefix}_{n}.graph', 'w') as file:
        file.write(f'{n}\n')
        for u, v in edges:
            file.write(f'{u} {v}\n')

# Generate snakes
for i in range(10):
    n = 2 ** (i+1)
    edges = [(i, i + 1) for i in range(1, n)]
    write_graph_to_file(n, edges, 'snake')
