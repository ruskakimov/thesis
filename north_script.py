import re
import matplotlib.pyplot as plt

def process_gml_log(file_path):
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

def process_sat_benchmark(file_path, results):
    with open(file_path, 'r') as file:
        content = file.read()
    
    benchmark_pattern = re.compile(
        r"Running for file: (?P<filename>g\.\d+\.\d+\.gml)\.cnf"  # Match filename
        r".*?Benchmark 1:.*?\n.*?Time \(mean ± σ\):\s+(?P<sat1>\d+\.\d+) (ms|s)"  # SAT1 time
        r".*?Benchmark 2:.*?\n.*?Time \(mean ± σ\):\s+(?P<sat2>\d+\.\d+) (ms|s)",  # SAT2 time
        re.DOTALL
    )
    
    for match in benchmark_pattern.finditer(content):
        filename = match.group('filename').replace('.cnf', '')  # Remove .cnf extension
        sat1_time = float(match.group('sat1'))
        sat1_unit = match.group(2)  # ms or s
        sat2_time = float(match.group('sat2'))
        sat2_unit = match.group(4)  # ms or s
        
        # Convert to seconds if necessary
        if sat1_unit == 'ms':
            sat1_time /= 1000
        if sat2_unit == 'ms':
            sat2_time /= 1000
        
        if filename in results:
            results[filename]['sat1'] = sat1_time
            results[filename]['sat2'] = sat2_time
    
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
    plt.ylabel("Elapsed Time (seconds)")
    plt.title(title)
    plt.legend()
    plt.show()

# Example usage
cp_file_path = "north__cp_result.txt"  # Change this to the CP solver log file
sat_file_path = "north__v1_v2_compare.txt"  # Change this to the SAT benchmark file

data = process_gml_log(cp_file_path)
process_sat_benchmark(sat_file_path, data)

graph_stats = parse_stat_file("north_graph_stats.txt")

for name, stats in graph_stats.items():
    n = stats['n']
    m = stats['m']

    if name not in data:
        print('graph not found', name)
    elif data[name]['nodes'] != n:
        print('number of nodes mismatch', name)
    else:
        data[name]['n'] = n
        data[name]['m'] = m
        data[name]['n+m'] = n + m

# Plot each separately
plot_scatter(data, 'cp', "CP Runtime")
plot_scatter(data, 'sat1', "SAT-1 Runtime")
plot_scatter(data, 'sat2', "SAT-2 Runtime")
