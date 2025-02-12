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

plt.rcParams.update({'font.size': 18})

def plot_scatter(data, key, title):

    sat_times = [(entry['n+m'], entry[key]) for entry in data.values() if entry['result'] == 'SAT' and key in entry]
    unsat_times = [(entry['n+m'], entry[key]) for entry in data.values() if entry['result'] == 'UNSAT' and key in entry]
    
    if sat_times:
        plt.scatter(*zip(*sat_times), color='green', label='SAT', marker='o', alpha=0.7, s=60)
    if unsat_times:
        plt.scatter(*zip(*unsat_times), color='red', label='UNSAT', marker='x', alpha=0.7, s=60)
    
    plt.xlabel('n+m')
    plt.ylabel("time (seconds)")
    # plt.title(title)
    plt.legend(loc='upper left')
    # plt.show()
    plt.tight_layout()
    plt.savefig(f"{title}.pdf", dpi=300)
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


plot_scatter(data, 'cp', "north_1_cp_scatter")
plot_scatter(data, 'sat1', "north_1_sat_1_scatter")
plot_scatter(data, 'sat2', "north_1_sat_2_scatter")