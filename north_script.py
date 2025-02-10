import csv
import os
import re
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

def plot_scatter(data, key, title):
    sat_times = [(entry['n+m'], entry[key]) for entry in data.values() if entry['result'] == 'SAT' and key in entry]
    unsat_times = [(entry['n+m'], entry[key]) for entry in data.values() if entry['result'] == 'UNSAT' and key in entry]
    
    if sat_times:
        plt.scatter(*zip(*sat_times), color='green', label='SAT', alpha=0.7)
    if unsat_times:
        plt.scatter(*zip(*unsat_times), color='red', label='UNSAT', alpha=0.7)
    
    plt.xlabel("n+m")
    plt.ylabel("time (seconds)")
    # plt.title(title)
    plt.legend()
    # plt.show()
    plt.savefig(f"{title}.pdf")
    plt.close('all')

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


# plot_scatter(data, 'cp', "cp_scatter")
# plot_scatter(data, 'sat1', "sat_1_scatter")
# plot_scatter(data, 'sat2', "sat_2_scatter")

speedups = []
threshold = 5 / 1000 # below this time will be more random

for filename, vals in data.items():
    if not 'sat1' in vals or not 'sat2' in vals:
        print('not found!', filename)
        continue

    cp = vals['cp']
    s1 = vals['sat1']
    s2 = vals['sat2']
    n = vals['n']
    m = vals['m']
    sat_result = vals['result']

    if s1 < threshold or s2 < threshold:
        continue

    # if sat_result == 'SAT':
    speedup = s1 / s2
    speedups.append(speedup)

print('total graphs:', len(speedups))

print('min speedup:', min(speedups))
print('max speedup:', max(speedups))

# print('above 1.5:', len([x for x in speedups if x > 1.5]))

average_speedup = sum(speedups) / len(speedups)
print('average speedup:', average_speedup)


bins = [0.8, 1.2, 1.6, 2, 4, 8, 16, 32]
fq = [0] * len(bins)

for x in speedups:
    for i, right in enumerate(bins):
        if x < right:
            fq[i] += 1
            break

labels = []

for i, r in enumerate(bins):
    if i == 0:
        labels.append(f'<{r}x')
    elif i == len(bins) - 1:
        l = bins[i-1]
        labels.append(f'>{l}x')
    else:
        l = bins[i-1]
        labels.append(f'{l}–{r}x')

assert(len(bins) == len(labels))

plt.bar(labels, fq, edgecolor='black', color=['red', 'gray', 'green','green','green','green','green','green'])

# plt.hist(speedups, bins=1000, edgecolor='black')  # 30 bins (one for each value)
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# # plt.title('Histogram of Values (0 to 30)')
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.xscale('log')

plt.xticks(rotation=45, ha="right", rotation_mode='anchor', fontsize=12)
plt.gcf().subplots_adjust(bottom=0.2)
plt.tight_layout()

legend_handles = [
    mpatches.Patch(color="red", label="Regression (<0.8x)"),
    mpatches.Patch(color="gray", label="Comparable (0.8x – 1.2x)"),
    mpatches.Patch(color="green", label="Improvement (1.2x+)")
]
plt.legend(handles=legend_handles, loc="upper right")

# Show plot
# plt.show()
plt.savefig("sat2_speedup_histogram.pdf")