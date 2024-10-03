def read_graph(file_path):
    n = None
    edges = []

    with file_path.open('r') as file:
        n = int(file.readline().strip())
        
        for line in file:
            u, v = map(int, line.strip().split())
            edges.append((u, v))
    
    return (n, edges)