import random
from pathlib import Path

def random_dag(n, m):
    """Generate a random DAG with n nodes and exactly m edges using a random topological order."""
    assert 0 <= m <= n * (n - 1) // 2

    order = list(range(n))
    random.shuffle(order)

    # All forward edges (acyclic in topological order)
    all_edges = [(order[i], order[j]) for i in range(n) for j in range(i + 1, n)]
    chosen_edges = random.sample(all_edges, m)
    return sorted(chosen_edges)

def generate_dags(n, per_m=100, output_dir="PT/dags"):
    max_edges = n * (n - 1) // 2
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file = output_path / f"n{n}_{per_m}_per_m.txt"

    with open(file, "w") as f:
        print(f"\nGenerating {per_m} DAGs per m for n={n} → {file}")
        for m in range(max_edges + 1):
            for _ in range(per_m):
                edges = random_dag(n, m)
                line = "[" + ", ".join(f"({u}, {v})" for u, v in edges) + "]"
                f.write(line + "\n")
            print(f"  ✓ m={m:3d}: {per_m} DAGs")

# Generate DAGs for n in 7 to 20
for n in [20]:
    generate_dags(n, per_m=50)
