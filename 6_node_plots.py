import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Scatter plot: Time vs m/n
def plot_scatter(df):
    plt.figure(figsize=(8, 5))
    plt.scatter(df["m/n"], df["time(s)"], alpha=0.5)
    plt.xlabel("m/n")
    plt.ylabel("Time (s)")
    plt.title("Scatter Plot: Time vs m/n")
    plt.grid()
    plt.show()

df = pd.read_csv("all_dags_5_bench.csv")

# Compute m/n ratio
df["m/n"] = df["m"] / df["n"]

# Example usage
plot_scatter(df)

mn_res_time = [(entry['m'] / entry['n'], entry['result'], entry['sat2']) for entry in data.values()]

mn_bucket_mid = []
runtimes = []

r = 1
step = 0.1
while r < 2.5 + step:
    bucket = [time for mn, sat, time in mn_res_time if (r - step) < mn <= r]
    if len(bucket) == 0:
        r += step
        continue

    bucket_mid = r - step/2
    mean_runtime = sum(bucket) / len(bucket)
    
    mn_bucket_mid.append(bucket_mid)
    runtimes.append(mean_runtime)

    print(f'({r-step:.1f}, {r:.1f}]', f'{mean_runtime:.3f}')
    r += step

plt.plot(mn_bucket_mid, runtimes, color='red', marker='o', linestyle='-', linewidth=3)
plt.xlabel("m/n")
plt.ylabel("time (seconds)")
# plt.ylim(0, 1)
# plt.title(f'bucket size: {step}')
plt.tight_layout()
plt.show()