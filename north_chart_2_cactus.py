import csv
import os
import re
import re
import matplotlib.pyplot as plt

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



# ==== DATA INITIALIZED ====

graphs = list(data.keys())
graphs.sort()

time = {
    'cp': [],
    'sat1': [],
    'sat2': [],
}

for graph in graphs:
    for alg in ['cp', 'sat1', 'sat2']:
        last_time = time[alg][-1] if len(time[alg]) > 0 else 0
        t = data[graph][alg]
        time[alg].append(last_time + t)
    # print(time['sat1'][-1])

for alg in ['cp', 'sat1', 'sat2']:
    print(alg, time[alg][-1])

solved_instances = [i / 1277 * 100 for i in range(1, len(graphs) + 1)]

for i, t in enumerate(time['sat1']):
    if solved_instances[i] < 6:
        print(i, solved_instances[i], t)

plt.rcParams.update({'font.size': 18})

plt.plot(solved_instances, time['cp'], label="CP", linestyle="-", linewidth=3, color='orange')
plt.plot(solved_instances, time['sat1'], label="SAT-1", linestyle="-", linewidth=3, color='navy')
plt.plot(solved_instances, time['sat2'], label="SAT-2", linestyle="-", linewidth=3, color='cyan')

# Labels and title
plt.xlabel("solved instances (%)")
plt.ylabel("time (seconds)")
plt.legend()
plt.grid(True)
plt.yscale("log")

# Save the plot
plt.tight_layout()
plt.show()
# plt.savefig("north_2_cactus.pdf", format="pdf", dpi=300)

# def plot_scatter(data, key, title):

#     sat_times = [(entry['n+m'], entry[key]) for entry in data.values() if entry['result'] == 'SAT' and key in entry]
#     unsat_times = [(entry['n+m'], entry[key]) for entry in data.values() if entry['result'] == 'UNSAT' and key in entry]
    
#     if sat_times:
#         plt.scatter(*zip(*sat_times), color='green', label='SAT', marker='o', alpha=0.7, s=60)
#     if unsat_times:
#         plt.scatter(*zip(*unsat_times), color='red', label='UNSAT', marker='x', alpha=0.7, s=60)
    
#     plt.xlabel('n+m')
#     plt.ylabel("time (seconds)")
#     # plt.title(title)
#     plt.legend(loc='upper left')
#     # plt.show()
#     plt.tight_layout()
#     plt.savefig(f"{title}.pdf", dpi=300)
#     plt.close('all')