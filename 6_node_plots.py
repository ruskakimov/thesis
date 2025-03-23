from pathlib import Path
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv(Path("./PT/bench/n10_10000_dags.csv"))
# df_n6_k2 = pd.read_csv(Path("./PT/bench/n6_k2___lingeling_10_runs.csv"))

# df_n5_k1 = pd.read_csv(Path("./PT/bench/n5_k1___lingeling_10_runs.csv"))
# df_n5_k2 = pd.read_csv(Path("./PT/bench/n5_k2___lingeling_10_runs.csv"))

# df_n4_k1 = pd.read_csv(Path("./PT/bench/n4_k1___lingeling_10_runs.csv"))

# Compute m/n ratio
# df["m/n"] = df["m"] / df["n"]
# df2["m/n"] = df2["m"] / df2["n"]
# # df["m/n"] = df["m/n"].round(4)

# # Scatter plot: Time vs m/n
# def plot_scatter(df):
#     plt.figure(figsize=(8, 5))
#     plt.scatter(df["m/n"], df["time(s)"], alpha=0.01, color='red')
#     plt.xlabel("m/n")
#     plt.ylabel("Time (s)")
#     plt.title("Scatter Plot: Time vs m/n")
#     plt.grid()
#     plt.show()

# plot_scatter(df)

# print(sorted(df["m/n"].unique()))

# by_mn = defaultdict(list)

# for index, row in df.iterrows():
#     mn = row["m"] / row["n"]
#     by_mn[mn].append(row["time(s)"])

# mns = list(by_mn.keys())
# mns.sort()
# means = []

# print(mns)

# for mn in mns:
#     mean = sum(by_mn[mn]) / len(by_mn[mn])
#     means.append(mean)

# print(means)

# plt.plot(mns, means)
# plt.show()

# man_mn = [0.0, 0.16666666666666666, 0.3333333333333333, 0.5, 0.6666666666666666, 0.8333333333333334, 1.0, 1.1666666666666667, 1.3333333333333333, 1.5, 1.6666666666666667, 1.8333333333333333, 2.0, 2.1666666666666665, 2.3333333333333335, 2.5]
# man_mean_time = [7.702e-05, 5.8549999999999987e-05, 6.029247619047618e-05, 6.554456111111111e-05, 6.900819047619047e-05, 7.25125181055836e-05, 7.749815535595505e-05, 8.215522022227527e-05, 8.931039951518962e-05, 0.00010511568484602627, 9.807410616190943e-05, 0.00010305658126682349, 0.00010795364248442969, 0.0001152129607614593, 0.000121728837777778, 0.00013142188888888898]











plt.rcParams.update({'font.size': 14})


# 1) time vs m/n
# grouped_mean = df.groupby("m/n")["time(s)"].mean()
# grouped_mean2 = df2.groupby("m/n")["time(s)"].mean()
# # grouped_median = df.groupby("m/n")["time(s)"].median()

# plt.figure(figsize=(8, 5))

# # Scatter plot of original data
# # plt.scatter(df["m/n"], df["time(s)"], alpha=0.5, color="red", label="Original Data")

# # Scatter plot of mean points
# plt.plot(grouped_mean.index, grouped_mean.values, color='red', marker='o', linestyle='-', linewidth=3, label="Mean")
# plt.plot(grouped_mean2.index, grouped_mean2.values, color='blue', marker='o', linestyle='-', linewidth=3, label="Mean")

# # Scatter plot of median points
# # plt.plot(grouped_median.index, grouped_median.values, color="green", marker="D", linestyle='-', linewidth=3, label="Median")

# plt.xlabel("m/n")
# plt.ylabel("time (seconds)")
# # plt.title("mean time vs m/n")
# # plt.legend()
# plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
# plt.grid(True)
# plt.tight_layout()
# # plt.savefig("PT_plots/all_5_node_sat1___mean_time_vs_mn.pdf")
# plt.show()






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

k1_col = k_colours[0]
k2_col = k_colours[1]

# 2) percentage vs m
# Group by 'm' and calculate the SAT percentage
# n6_k1 = df_n6_k1.groupby('m')['sat'].mean() * 100  # Mean gives the proportion of True values
# n6_k2 = df_n6_k2.groupby('m')['sat'].mean() * 100

# n5_k1 = df_n5_k1.groupby('m')['sat'].mean() * 100
# n5_k2 = df_n5_k2.groupby('m')['sat'].mean() * 100

# n4_k1 = df_n4_k1.groupby('m')['sat'].mean() * 100
# # m_counts2 = df2.groupby('m')['sat'].mean() * 100

# # Plotting
# plt.figure(figsize=(8, 3))
# plt.plot(n6_k1.index, n6_k1.values, color=k1_col, marker='o', linestyle='-', linewidth=1, label='n=6, k=1')
# plt.plot(n6_k2.index, n6_k2.values, color=k2_col, marker='o', linestyle='-', linewidth=1, label='n=6, k=2')

# plt.plot(n5_k1.index, n5_k1.values, color=k1_col, marker='x', linestyle='--', linewidth=1, label='n=5, k=1')
# plt.plot(n5_k2.index, n5_k2.values, color=k2_col, marker='x', linestyle='--', linewidth=1, label='n=5, k=2')

# plt.plot(n4_k1.index, n4_k1.values, color=k1_col, marker='^', linestyle=':', linewidth=1, label='n=4, k=1')
# # plt.plot(m_counts2.index, m_counts2.values, color=k_colours[1], marker='o', linestyle='-', linewidth=3, label='2UBE')
# plt.xlabel('m')
# plt.ylabel('satisfiable (%)')
# # plt.title('Satisfiability for 6-node DAGs')
# # plt.ylim(0, 100)
# plt.xticks(n6_k1.index)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.legend()
# plt.tight_layout()
# plt.savefig("PT/plots/sat_curves_n4-6.pdf")
# plt.show()






# 3) graph distribution vs m
m_counts = df.groupby('m')['sat'].size()
plt.figure(figsize=(8, 5))
plt.bar(m_counts.index, m_counts.values, color='royalblue')
plt.xlabel('m')
plt.ylabel('dag count')
plt.title('Distribution of DAGs with 6 nodes')
plt.xticks(m_counts.index)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()