import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re
import ast
from collections import Counter
import matplotlib.ticker as ticker

# --- Paths ---
script_dir = Path(__file__).resolve().parent
data_dir = script_dir.parent / "bench"         # ../bench
dags_dir = script_dir.parent / "dags"          # ../dags
output_path = Path("sat_curves.pdf")           # ./sat_curves.pdf

# --- Configurable Parameters ---
default_n_values = [10]
default_k_values = [1,2,3,4]
dataset_runs = 1

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
k_markers = [
    'o',  # Circle
    'x',  # X
    '^',  # Triangle Up
    's',  # Square
    'D',  # Diamond
    '*',  # Star
    'P',  # Plus (filled)
    'X',  # X (filled)
    'v',  # Triangle Down
    'd',  # Thin diamond
]

# --- Helper Functions ---
def get_filename(n, k, eq_bins=True):
    if eq_bins:
        return f"n{n}_k{k}___{dataset_runs}_run_eq_m_bins.csv"
    return f"n{n}_k{k}___{dataset_runs}_runs.csv"

def load_and_process_csv(n, k, eq_bins=True):
    filepath = data_dir / get_filename(n, k, eq_bins)
    print('Loading', filepath)
    df = pd.read_csv(filepath)
    return df

# --- Plotting Functions ---

def plot_sat_curves(n_values=default_n_values, k_values=default_k_values, output_file=output_path):
    plt.figure(figsize=(10, 3))

    for n in n_values:
        for k in k_values:
            try:
                df = load_and_process_csv(n, k)
                grouped = df.groupby("m")["sat"].mean() * 100  # Convert to %
                color = k_colours[k - 1]
                marker = k_markers[k - 1]
                label = f"n={n}, k={k}"
                plt.plot(grouped.index, grouped.values, color=color, marker=marker,
                         linestyle='-', linewidth=1, label=label)
            except FileNotFoundError:
                print(f"Missing data for n={n}, k={k} ({get_filename(n, k)})")

    plt.xlabel('m')
    plt.ylabel('satisfiable (%)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()

def plot_mean_runtime_vs_mn_ratio(n_values=default_n_values, k_values=default_k_values):
    plt.figure(figsize=(10, 5))

    for n in n_values:
        for k in k_values:
            try:
                df = load_and_process_csv(n, k, True)
                # df = df.dropna(subset=["time(s)"]) # drop rows with missing time

                # df["m/n"] = df["m"] / n
                grouped = df.groupby("m")["time(s)"].mean()

                color = k_colours[k - 1]
                marker = k_markers[k - 1]
                # marker = None
                label = f"n={n}, k={k}"

                plt.plot(grouped.index, grouped.values, color=color, linestyle='-',
                         marker=marker, linewidth=1, label=label)
            except FileNotFoundError:
                print(f"Missing data for n={n}, k={k} ({get_filename(n, k)})")

    plt.xlabel("m")
    plt.ylabel("time (s)")
    # plt.ylim(0, 0.02)
    plt.yscale('log')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    # plt.savefig(output_file)
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

def plot_sat_and_time_shared_x(n_values, k_values, dataset_runs, data_dir, k_colours, k_markers, output_file="sat_time_shared_axis.pdf"):
    for n in n_values:
        for k in k_values:
            try:
                df = load_and_process_csv(n, k, True)
                
                # Group data
                m_vals = sorted(df["m"].unique())
                sat_percent = df.groupby("m")["sat"].mean() * 100
                avg_time = df.groupby("m")["time(s)"].mean()

                # Estimate PT at ~50% SAT
                pt_candidates = (sat_percent - 50).abs()
                pt_m = pt_candidates.idxmin()

                # Plot
                fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 5), height_ratios=(1, 1))

                # SAT%
                ax1.plot(m_vals, sat_percent, marker=k_markers[k - 1], color=k_colours[k - 1], label=f"n={n}, k={k}")
                ax1.set_ylabel("satisfiable (%)")
                ax1.set_ylim(-5, 105)
                ax1.grid(True)
                ax1.legend(loc="lower left")

                # Time (log scale)
                ax2.plot(m_vals, avg_time, marker=k_markers[k - 1], color=k_colours[k - 1], label=f"n={n}, k={k}")
                ax2.set_ylabel("time (s)")
                ax2.set_xlabel("m")
                ax2.set_yscale("log")
                ax2.yaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=[1.0], numticks=6))
                ax2.yaxis.set_minor_locator(ticker.NullLocator())
                ax2.grid(True, which='both')
                ax2.legend(loc="upper left")

                # Shared vertical line at PT
                for ax in [ax1, ax2]:
                    ax.axvline(x=pt_m, linestyle='--', color='gray', linewidth=1)

                fig.align_ylabels([ax1, ax2])
                plt.tight_layout()
                plt.savefig(f"sat_time_n{n}_k{k}.pdf")
                plt.show()

            except FileNotFoundError:
                print(f"Some error")


# --- Example usage ---
if __name__ == "__main__":
    # plot_sat_curves()
    # plot_mean_runtime_vs_mn_ratio()
    plot_sat_and_time_shared_x([10], [1, 2, 3, 4], 1, "../bench", k_colours, k_markers)
    # plot_dag_count_per_m("n7_1000_dags.txt")
