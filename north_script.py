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
            'time': elapsed_time,
            'result': result
        }
    
    return results

def plot_scatter(data):
    sat_times = [(entry['nodes'], entry['time']) for entry in data.values() if entry['result'] == 'SAT']
    unsat_times = [(entry['nodes'], entry['time']) for entry in data.values() if entry['result'] == 'UNSAT']
    
    if sat_times:
        plt.scatter(*zip(*sat_times), color='blue', label='SAT', alpha=0.7)
    if unsat_times:
        plt.scatter(*zip(*unsat_times), color='red', label='UNSAT', alpha=0.7)
    
    plt.xlabel("Number of Nodes")
    plt.ylabel("Elapsed Time (seconds)")
    plt.title("Scatter Plot of Elapsed Time vs. Number of Nodes")
    plt.legend()
    plt.show()

# Example usage
file_path = "north__cp_result.txt"  # Change this to the actual file path
data = process_gml_log(file_path)
plot_scatter(data)
