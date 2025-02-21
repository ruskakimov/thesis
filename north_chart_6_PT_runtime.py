import csv
import os
import re
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from scipy.stats import levene, mannwhitneyu, ttest_ind
import seaborn as sns

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


plt.rcParams.update({'font.size': 18})

# 1. Sat-1 Runtimes vs CNF clause count
# runtimes = [(entry['sat2_cv_ratio'], entry['sat2']) for entry in data.values()]
# plt.scatter(*zip(*runtimes), color='cyan', alpha=0.3, s=60)
# plt.xlabel("sat-2 clauses-to-variables ratio")
# plt.ylabel("sat-2 time (seconds)")
# plt.tight_layout()
# plt.show()
# plt.savefig("north_5_clause_count_scatter.pdf"


# 2. Plot mean/median per ratio bins
# B = 30  # Change this as needed
# method = 'sat2'
# # Extract data
# runtimes = [(entry['m'] / entry['n'], entry[f'{method}']) for entry in data.values()]
# ratios, times = zip(*runtimes)
# # Define bins with equal width
# min_ratio, max_ratio = min(ratios), max(ratios)
# bin_edges = np.linspace(min_ratio, max_ratio, B + 1)  # B bins → B+1 edges
# # Compute mean/median for each bin
# binned_ratios = []
# binned_mean_values = []
# binned_median_values = []
# for i in range(B):
#     bin_start, bin_end = bin_edges[i], bin_edges[i + 1]
#     bin_mask = (np.array(ratios) >= bin_start) & (np.array(ratios) < bin_end)
#     bin_times = np.array(times)[bin_mask]
#     if len(bin_times) > 0:
#         binned_ratios.append((bin_start + bin_end) / 2)  # Middle of the bin
#         binned_mean_values.append(np.mean(bin_times))  # Replace with np.median(bin_times) if needed
#         binned_median_values.append(np.median(bin_times))
# # plt.scatter(ratios, times, color='gray', alpha=0.3, s=60, label="raw data")
# plt.plot(binned_ratios, binned_mean_values, color='red', marker='o', linestyle='-', linewidth=3, label="mean")
# # plt.plot(binned_ratios, binned_median_values, color='blue', marker='s', linestyle='-', linewidth=3, label="median")
# plt.axvline(1.5)
# plt.xlabel("m/n")
# plt.ylabel("time (seconds)")
# plt.legend()
# plt.title(f'{method}, {B} buckets')
# plt.tight_layout()
# plt.show()


# B = 30  # Number of bins
# method = 'sat1'

# # Extract data
mn_res_time = [(entry['m'] / entry['n'], entry['result'], entry['sat2']) for entry in data.values()]
# ratios, results = zip(*runtimes)

# # Define bins with equal width
# min_ratio, max_ratio = min(ratios), max(ratios)
# bin_edges = np.linspace(min_ratio, max_ratio, B + 1)  # B bins → B+1 edges

# # Compute SAT ratio for each bin
# binned_ratios = []
# sat_ratios = []

# total_sat = 0

# for i in range(B):
#     bin_start, bin_end = bin_edges[i], bin_edges[i + 1]
#     bin_mask = (np.array(ratios) >= bin_start) & (np.array(ratios) < bin_end)
    
#     bin_results = np.array(results)[bin_mask]
#     sat_count = np.sum(bin_results == 'SAT')
#     total_count = len(bin_results)
#     total_sat += sat_count

#     print(bin_end, ': ', sat_count, '/', total_count)

#     if total_count > 0:
#         binned_ratios.append((bin_start + bin_end) / 2)  # Midpoint of the bin
#         sat_ratios.append(sat_count / total_count)  # SAT / (SAT + UNSAT)

# print('total SAT:', total_sat)

# # Plot SAT ratio per bucket
# plt.plot(binned_ratios, sat_ratios, color='blue', marker='o', linestyle='-', linewidth=3, markersize=9)

# # Formatting
# plt.xlabel("m/n")
# plt.ylabel("sat probability")
# plt.ylim(0, 1)  # Ensure y-axis is in range [0, 1]
# # plt.legend()
# # plt.title('')
# plt.tight_layout()
# plt.show()

print('Total SAT:', len([mn for mn, sat, time in mn_res_time if sat == 'SAT']))
print('Total UNSAT', len([mn for mn, sat, time in mn_res_time if sat == 'UNSAT']))

mn_bucket_mid = []
runtimes = []

r = 1
step = 0.1
while r < 2 + step:
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
plt.title(f'bucket size: {step}')
plt.tight_layout()
plt.show()