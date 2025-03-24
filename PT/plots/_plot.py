import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re
import ast
from collections import Counter

# --- Paths ---
script_dir = Path(__file__).resolve().parent
data_dir = script_dir.parent / "bench"         # ../bench
dags_dir = script_dir.parent / "dags"          # ../dags
output_path = Path("sat_curves.pdf")           # ./sat_curves.pdf

# --- Configurable Parameters ---
default_n_values = [10]
default_k_values = list(range(20))

# --- Style Settings ---
plt.rcParams.update({'font.size': 14})
k_colours = [
    "#1f77b4",  # Muted Blue
    "#ff7f0e",  # Orange
    "#2ca02c",  # Green
    "#d62728",  # Red
    "#9467bd",  # Purple
    "#8c564b",  # Brown
    "#e377c2",  # Pink
    "#7f7f7f",  # Gray
    "#bcbd22",  # Yellow-Green
    "#17becf",  # Cyan
]

# --- Helper Functions ---
def get_filename(n, k, eq_bins=True):
    if eq_bins:
        return f"n{n}_k{k}___1_run_eq_m_bins.csv"
    runs = 1 if (n == 6 and k == 1) else 10
    return f"n{n}_k{k}___{runs}_runs.csv"

def load_and_process_csv(n, k):
    filepath = data_dir / get_filename(n, k)
    df = pd.read_csv(filepath)
    return df

# --- Plotting Functions ---

def plot_sat_curves(n_values=default_n_values, k_values=default_k_values, output_file=output_path):
    plt.figure(figsize=(8, 3))

    for idx_n, n in enumerate(n_values):
        for k in k_values:
            try:
                df = load_and_process_csv(n, k)
                grouped = df.groupby("m")["sat"].mean() * 100  # Convert to %
                color = k_colours[k - 1]
                style = ['-', '--', ':'][idx_n % 3]
                marker = ['o', 'x', '^'][idx_n % 3]
                label = f"n={n}, k={k}"
                plt.plot(grouped.index, grouped.values, color=color, marker=marker,
                         linestyle=style, linewidth=1, label=label)
            except FileNotFoundError:
                print(f"Missing data for n={n}, k={k} ({get_filename(n, k)})")

    plt.xlabel('m')
    plt.ylabel('satisfiable (%)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()


def plot_dag_count_per_m(filename):
    path = dags_dir / filename
    try:
        with open(path, "r") as f:
            dags = [ast.literal_eval(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {path}")
        return

    # Count how many DAGs have each number of edges (m)
    m_counts = Counter(len(edges) for edges in dags)
    ms = sorted(m_counts)
    counts = [m_counts[m] for m in ms]

    # Plot
    plt.figure(figsize=(8, 4))
    plt.bar(ms, counts, color="#1f77b4")
    plt.xlabel("m (number of edges)")
    plt.ylabel("count")
    plt.title(f"Number of DAGs per m from {filename}")
    plt.xticks(ms)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


# --- Example usage ---
if __name__ == "__main__":
    plot_sat_curves()
    # plot_dag_count_per_m("n7_1000_dags.txt")
