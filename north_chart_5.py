import csv
import os
import re
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from scipy.stats import levene, mannwhitneyu, ttest_ind

def process_cp_result(file_path):
    results = {}
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Regex to match filename, solution status, and elapsed time
    pattern = re.compile(r"'(?P<filename>g\.(?P<nodes>\d+)\.\d+\.gml)' started\.\n(?P<status>Solution found:|No solution found\.)?\n'\1' stopped\. Elapsed time: (?P<time>\d+\.\d+) seconds")
    
    for match in pattern.finditer(content):
        filename = match.group('filename')
        nodes = int(match.group('nodes'))
        elapsed_time = float(match.group('time'))
        status = match.group('status')
        
        result = 'SAT' if status and 'Solution found' in status else 'UNSAT'
        
        results[filename] = {
            'nodes': nodes,
            'cp': elapsed_time,
            'result': result
        }
    
    return results


def parse_stat_file(file_path):
    data = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                name, n, m = parts
                data[name] = {
                    'n': int(n),
                    'm': int(m)
                }
    
    return data

plt.rcParams.update({'font.size': 18})

def plot_scatter(data):

    # hard_times = [(entry['sat1_cnf_c'] / 1e5 / entry['sat1'], entry['sat1'] / entry['sat2']) for entry in data.values() if entry['sat1_cnf_c'] / 1e5 / entry['sat1'] < 6]
    # easy_times = [(entry['sat1_cnf_c'] / 1e5 / entry['sat1'], entry['sat1'] / entry['sat2']) for entry in data.values() if entry['sat1_cnf_c'] / 1e5 / entry['sat1'] > 6]

    # if hard_times:
    #     plt.scatter(*zip(*hard_times), color='blue', label='hard', alpha=0.2, s=60)
    # if easy_times:
    #     plt.scatter(*zip(*easy_times), color='blue', label='easy', alpha=0.2, s=60)
    # plt.xlabel("sat-1 tractability")
    # plt.ylabel("speedup")

    # Sat-1 Runtimes vs CNF clause count
    runtimes = [(entry['sat1_cnf_c'], entry['sat1']) for entry in data.values()]
    plt.scatter(*zip(*runtimes), color='blue', alpha=0.2, s=60)
    plt.xlabel("number of sat-1 clauses")
    plt.ylabel("time (seconds)")
    plt.tight_layout()
    plt.savefig("north_5_clause_count_scatter.pdf")
    
    
    # plt.title(title)
    # plt.tight_layout()
    # plt.legend()
    # plt.show()
    # plt.savefig("north_chart.pdf")
    # plt.close('all')

# Read CP data
cp_file_path = "north__cp_result.txt"
data = process_cp_result(cp_file_path)




# Add graph details (n, m, n+m)
graph_stats = parse_stat_file("north_graph_stats.txt")
for filename, stats in graph_stats.items():
    n = stats['n']
    m = stats['m']

    if filename not in data:
        print('graph not found', filename)
    elif data[filename]['nodes'] != n:
        print('number of nodes mismatch', filename)
    else:
        data[filename]['n'] = n
        data[filename]['m'] = m
        data[filename]['n+m'] = n + m



with open('bench_north.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        command = row['command']
        mean = float(row["mean"])
        median = float(row["median"])

        # The command field looks like:
        # "./solvers/kissat-4.0.1-apple-amd64 ./cnf/north_SAT1/g.10.0.gml.cnf"
        # We assume the second part is the file path.
        file_path = command.split()[1]
        
        # Extract the file name, e.g. "g.10.0.gml.cnf"
        base = os.path.basename(file_path)
        # Remove the .cnf extension to get "g.10.0.gml"
        filename, _ = os.path.splitext(base)

        
        if 'north_SAT1' in file_path:
            data[filename]['sat1'] = mean
        elif 'north_SAT2' in file_path:
            data[filename]['sat2'] = mean
        else:
            print('failed to match sat1 or sat2')


for sat in ['sat1', 'sat2']:
    with open(f'north_{sat}_vars_clauses.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            graph = row['graph'][:-4]
            var_count = int(row["vars"])
            clause_count = int(row["clauses"])

            data[graph][f'{sat}_cnf_v'] = var_count
            data[graph][f'{sat}_cnf_c'] = clause_count
            data[graph][f'{sat}_cv_ratio'] = clause_count / var_count

# print(data['g.10.0.gml'])

# plot_scatter(data)


# speedups = []
# threshold = 5 / 1000 # below this time will be more random

# for filename, vals in data.items():
#     if not 'sat1' in vals or not 'sat2' in vals:
#         print('not found!', filename)
#         continue

#     cp = vals['cp']
#     s1 = vals['sat1']
#     s2 = vals['sat2']
#     n = vals['n']
#     m = vals['m']
#     sat_result = vals['result']

#     if s1 < threshold or s2 < threshold:
#         continue

#     # if sat_result == 'SAT':
#     speedup = s1 / s2
#     speedups.append(speedup)

threshold = 6 * 1e5

# [(clauses, runtime), ...]
below_group = [(entry['sat1_cnf_c'], entry['sat1']) for entry in data.values() if entry['sat1_cnf_c'] / entry['sat1'] < threshold]
above_group = [(entry['sat1_cnf_c'], entry['sat1']) for entry in data.values() if entry['sat1_cnf_c'] / entry['sat1'] >= threshold]

# Convert to DataFrames
df1 = pd.DataFrame(below_group, columns=['X', 'Y'])
df2 = pd.DataFrame(above_group, columns=['X', 'Y'])

# Compute the ratio R = X / Y
df1['Ratio'] = df1['X'] / df1['Y']
df2['Ratio'] = df2['X'] / df2['Y']

# Compute summary statistics
stats = {
    'Group': ['Below Threshold (R < T)', 'Above Threshold (R ≥ T)'],
    'Mean': [df1['Ratio'].mean(), df2['Ratio'].mean()],
    'Median': [df1['Ratio'].median(), df2['Ratio'].median()],
    'Variance': [df1['Ratio'].var(), df2['Ratio'].var()]
}

summary_df = pd.DataFrame(stats)
print(summary_df)

# Variance test (Levene’s test)
levene_stat, levene_p = levene(df1['Ratio'], df2['Ratio'])

# Non-parametric test for median difference
mann_stat, mann_p = mannwhitneyu(df1['Ratio'], df2['Ratio'], alternative='two-sided')

# Parametric test for mean difference
t_stat, t_p = ttest_ind(df1['Ratio'], df2['Ratio'])

# Display test results
test_results = pd.DataFrame({
    'Test': ['Levene’s Test (Variance)', 'Mann-Whitney U Test (Median)', 'T-Test (Mean)'],
    'Statistic': [levene_stat, mann_stat, t_stat],
    'p-value': [levene_p, mann_p, t_p]
})
print(test_results)

# 1. Sat-1 Runtimes vs CNF clause count
# runtimes = [(entry['sat1_cnf_c'], entry['sat1']) for entry in data.values()]
# plt.scatter(*zip(*runtimes), color='blue', alpha=0.3, s=60)
# plt.xlabel("number of sat-1 clauses")
# plt.ylabel("time (seconds)")
# plt.tight_layout()
# plt.savefig("north_5_clause_count_scatter.pdf")

# 2. Color groups
# hard_runtimes = [(entry['sat1_cnf_c'], entry['sat1']) for entry in data.values() if entry['sat1_cnf_c'] / entry['sat1'] < threshold]
# easy_runtimes = [(entry['sat1_cnf_c'], entry['sat1']) for entry in data.values() if entry['sat1_cnf_c'] / entry['sat1'] >= threshold]
# plt.scatter(*zip(*hard_runtimes), color='crimson', alpha=0.6, s=60, label='hard')
# plt.scatter(*zip(*easy_runtimes), color='teal', alpha=0.6, s=60, label='easy')
# plt.xlabel("number of sat-1 clauses")
# plt.ylabel("time (seconds)")
# plt.tight_layout()
# plt.legend()
# # plt.show()
# plt.savefig("north_5_clause_count_scatter_separated.pdf")

# 3. Speedup for groups
hard_runtimes = [(entry['sat1_cnf_c'] / entry['sat1'], entry['sat1'] / entry['sat2']) for entry in data.values() if entry['sat1_cnf_c'] / entry['sat1'] < threshold]
easy_runtimes = [(entry['sat1_cnf_c'] / entry['sat1'], entry['sat1'] / entry['sat2']) for entry in data.values() if entry['sat1_cnf_c'] / entry['sat1'] >= threshold]
plt.scatter(*zip(*hard_runtimes), color='crimson', alpha=0.1, s=60, label='hard')
plt.scatter(*zip(*easy_runtimes), color='teal', alpha=0.1, s=60, label='easy')
plt.axhline(1, color="black", linestyle="--", linewidth=1)
plt.xlabel("sat-1 clause-to-time ratio")
plt.ylabel("sat-2 speedup")
plt.tight_layout()
hard_patch = mpatches.Patch(color="crimson", label="hard")
easy_patch = mpatches.Patch(color="teal", label="easy")
plt.legend(handles=[hard_patch, easy_patch], loc="upper right")
# plt.show()
plt.savefig("north_5_speedup_groups.pdf")