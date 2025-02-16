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

data = {}

# Table data
table_data = [
    (2, 0.0016, 0.0030, 0.0109),
    (3, 0.0053, 0.0033, 0.1007),
    (4, 0.0290, 0.0071, 0.6595),
    (5, 0.0503, 0.0116, 3.2400),
    (6, 0.1006, 0.0274, 7.8882),
    (7, 0.2406, 0.1536, 15.0825),
    (8, 0.5470, 0.3536, 28.3582),
    (9, 1.209, 0.7173, 46.2965),
    (10, 2.565, 1.266, 74.8024),
    (11, 4.601, 2.225, 108.6383),
    (12, 5.478, 4.491, 148.0552),
    (13, 7.062, 6.676, 183.4610),
    (14, 8.929, 8.370, 334.5505),
    (15, 11.362, 10.457, 538.5593),
    (16, 15.145, 13.859, 798.9257),
    (17, 19.617, 18.148, 1039.6657),
    (18, 25.703, 23.611, 1355.6614),
    (19, 34.164, 31.033, 2293.8375),
    (20, 44.323, 41.848, "TO"),
    (21, 77.498, 35.553, "TO"),
    (22, 111.974, 54.986, "TO"),
    (23, 152.683, 97.159, "TO"),
    (24, 237.621, 143.109, "TO"),
    (25, 377.786, 241.390, "TO"),
    (26, 570.635, 363.598, "TO"),
    (27, 1314.026, 978.565, "TO"),
    (28, 2874.723, 1649.362, "TO"),
]

# Populate the dictionary
for size, sat1, sat2, cp in table_data:
    key = f"{size}x{size}"  # Convert size to grid format (e.g., "28x28")
    data[key] = {
        "n": size,
        "sat1": sat1,
        "sat2": sat2,
        "cp": cp
    }

for sat in ['sat1', 'sat2']:
    with open(f'grid_{sat}_vars_clauses.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            n = int(row['n'])
            key = f'{n}x{n}'
            var_count = int(row["vars"])
            clause_count = int(row["clauses"])

            data[key][f'{sat}_cnf_v'] = var_count
            data[key][f'{sat}_cnf_c'] = clause_count
            data[key][f'{sat}_cv_ratio'] = clause_count / var_count

print(data)

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

# plt.rcParams.update({'font.size': 18})

# 1. Sat-1 Runtimes vs CNF clause count
runtimes = [(entry['sat1_cnf_c'], entry['sat1']) for entry in data.values()]
plt.scatter(*zip(*runtimes), color='blue', alpha=0.3, s=60)
plt.xlabel("number of sat-1 clauses")
plt.ylabel("time (seconds)")
plt.axline((0, 0), slope=1 / threshold, linestyle=":", color="black", linewidth=2)
plt.tight_layout()
plt.show()
# plt.savefig("north_5_clause_count_scatter.pdf")

# 2. Color groups
# hard_runtimes = [(entry['sat1_cnf_c'], entry['sat1']) for entry in data.values() if entry['sat1_cnf_c'] / entry['sat1'] < threshold]
# easy_runtimes = [(entry['sat1_cnf_c'], entry['sat1']) for entry in data.values() if entry['sat1_cnf_c'] / entry['sat1'] >= threshold]
# plt.scatter(*zip(*hard_runtimes), color='crimson', alpha=0.3, s=60, label='hard')
# plt.scatter(*zip(*easy_runtimes), color='teal', alpha=0.3, s=60, label='easy')
# plt.xlabel("number of sat-1 clauses")
# plt.ylabel("time (seconds)")
# plt.tight_layout()
# hard_patch = mpatches.Patch(color="crimson", label="hard")
# easy_patch = mpatches.Patch(color="teal", label="easy")
# plt.legend(handles=[hard_patch, easy_patch])
# # plt.axhline(1, color="black", linestyle="--", linewidth=1)
# plt.axline((0, 0), slope=1 / threshold, linestyle=":", color="black", linewidth=2)
# # plt.plot([0, threshold], [0, 8], linestyle="--", color="black", linewidth=1)
# plt.show()
# # plt.savefig("north_5_clause_count_scatter_separated.pdf")