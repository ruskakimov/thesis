import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- Paths ---
script_dir = Path(__file__).resolve().parent
data_dir = script_dir.parent / "bench"         # ../bench
output_path = Path("sat_curves.pdf")           # ./sat_curves.pdf

# --- Configurable Parameters ---
n_values = [5,6,7,8,9,10,11,12,13,14,15]
k_values = [7]

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
def get_filename(n, k):
    runs = 1 if (n == 6 and k == 1) else 10
    return f"n{n}_k{k}___{runs}_run{'s' if runs > 1 else ''}.csv"

def load_and_process_csv(n, k):
    filepath = data_dir / get_filename(n, k)
    df = pd.read_csv(filepath)
    return df.groupby("m")["sat"].mean() * 100  # Convert to percentage

# --- Plotting ---
plt.figure(figsize=(8, 3))

for idx_n, n in enumerate(n_values):
    for k in k_values:
        try:
            color = k_colours[k - 1]
            style = ['-', '--', ':'][idx_n % 3]
            marker = ['o', 'x', '^'][idx_n % 3]
            curve = load_and_process_csv(n, k)
            label = f"n={n}, k={k}"
            plt.plot(curve.index, curve.values, color=color, marker=marker,
                     linestyle=style, linewidth=1, label=label)
        except FileNotFoundError:
            print(f"Missing data for n={n}, k={k} ({get_filename(n, k)})")

plt.xlabel('m')
plt.ylabel('satisfiable (%)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig(output_path)
plt.show()
