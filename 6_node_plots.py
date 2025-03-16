import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_time_vs_ratio(file_path):
    # Read CSV file
    df = pd.read_csv(file_path)
    print("Columns in the CSV:", df.columns)

    # Compute m/n ratio
    df["m/n"] = df["m"] / df["n"]

    # Scatter plot: Time vs m/n
    plt.figure(figsize=(8, 5))
    plt.scatter(df["m/n"], df["time(s)"], alpha=0.5)
    plt.xlabel("m/n")
    plt.ylabel("Time (s)")
    plt.title("Scatter Plot: Time vs m/n")
    plt.grid()
    plt.show()

# Example usage
plot_time_vs_ratio("all_dags_5_bench.csv")
