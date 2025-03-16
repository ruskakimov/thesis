import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("all_dags_4_bench.csv")

# Compute m/n ratio
df["m/n"] = df["m"] / df["n"]

# Scatter plot: Time vs m/n
def plot_scatter(df):
    plt.figure(figsize=(8, 5))
    plt.scatter(df["m/n"], df["time(s)"], alpha=0.1, color='red')
    plt.xlabel("m/n")
    plt.ylabel("Time (s)")
    plt.title("Scatter Plot: Time vs m/n")
    plt.grid()
    plt.show()

plot_scatter(df)





# Assuming df is your DataFrame
grouped_mean = df.groupby("m/n")["time(s)"].mean()
grouped_median = df.groupby("m/n")["time(s)"].median()

plt.figure(figsize=(8, 5))

# Scatter plot of original data
plt.scatter(df["m/n"], df["time(s)"], alpha=0.5, color="red", label="Original Data")

# Scatter plot of mean points
plt.scatter(grouped_mean.index, grouped_mean.values, color="blue", marker="o", s=80, label="Mean")

# Scatter plot of median points
# plt.scatter(grouped_median.index, grouped_median.values, color="green", marker="D", s=80, label="Median")

plt.xlabel("m/n")
plt.ylabel("Time (s)")
plt.title("Scatter Plot: Time vs m/n with Mean & Median")
plt.legend()
plt.grid(True)

plt.show()