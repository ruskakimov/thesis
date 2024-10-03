from pathlib import Path

graphs_dir = Path(__file__).resolve().parent.parent / 'graphs'

def snake_edges(n):
    return [(i, i + 1) for i in range(1, n)]

# Generate snakes
for i in range(10):
    n = 2 ** (i+1)
    edges = snake_edges(n)

    with open(graphs_dir / f'snake_{n}.graph', 'w') as file:
        file.write(f'{n}\n')

        for u, v in edges:
            file.write(f'{u} {v}\n')
