from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("all_dags_5_bench_lingeling_100_runs_2.csv")

# Compute m/n ratio
df["m/n"] = df["m"] / df["n"]
# df["m/n"] = df["m/n"].round(4)

# Scatter plot: Time vs m/n
def plot_scatter(df):
    plt.figure(figsize=(8, 5))
    plt.scatter(df["m/n"], df["time(s)"], alpha=0.01, color='red')
    plt.xlabel("m/n")
    plt.ylabel("Time (s)")
    plt.title("Scatter Plot: Time vs m/n")
    plt.grid()
    plt.show()

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

man_mn = [0.0, 0.16666666666666666, 0.3333333333333333, 0.5, 0.6666666666666666, 0.8333333333333334, 1.0, 1.1666666666666667, 1.3333333333333333, 1.5, 1.6666666666666667, 1.8333333333333333, 2.0, 2.1666666666666665, 2.3333333333333335, 2.5]
man_mean_time = [7.702e-05, 5.8549999999999987e-05, 6.029247619047618e-05, 6.554456111111111e-05, 6.900819047619047e-05, 7.25125181055836e-05, 7.749815535595505e-05, 8.215522022227527e-05, 8.931039951518962e-05, 0.00010511568484602627, 9.807410616190943e-05, 0.00010305658126682349, 0.00010795364248442969, 0.0001152129607614593, 0.000121728837777778, 0.00013142188888888898]














# 1) time vs m/n
grouped_mean = df.groupby("m/n")["time(s)"].mean()
grouped_median = df.groupby("m/n")["median_time(s)"].mean()

plt.figure(figsize=(8, 5))

# Scatter plot of original data
# plt.scatter(df["m/n"], df["time(s)"], alpha=0.5, color="red", label="Original Data")

# Scatter plot of mean points
plt.plot(grouped_mean.index, grouped_mean.values, color='red', marker='o', linestyle='-', linewidth=3, label="Mean")

# Scatter plot of median points
# plt.plot(grouped_median.index, grouped_median.values, color="green", marker="D", linestyle='-', linewidth=3, label="Median")

plt.xlabel("m/n")
plt.ylabel("mean time (s)")
plt.title("mean time vs m/n")
plt.legend()
plt.grid(True)

plt.show()










# 2) percentage vs m
# # Group by 'm' and calculate the SAT percentage
# m_counts = df.groupby('m')['sat'].mean() * 100  # Mean gives the proportion of True values

# # Plotting
# plt.figure(figsize=(8, 5))
# plt.plot(m_counts.index, m_counts.values, color='royalblue', marker='o', linestyle='-', linewidth=3)
# plt.xlabel('m')
# plt.ylabel('Percentage of SAT (%)')
# plt.title('Percentage of SAT per m')
# # plt.ylim(0, 100)
# plt.xticks(m_counts.index)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()






# 3) graph distribution vs m
# m_counts = df.groupby('m')['sat'].size()
# plt.figure(figsize=(8, 5))
# plt.bar(m_counts.index, m_counts.values, color='royalblue')
# plt.xlabel('m')
# plt.ylabel('dag count')
# plt.title('Distribution of DAGs with 6 nodes')
# plt.xticks(m_counts.index)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()