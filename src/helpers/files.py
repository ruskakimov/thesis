from pathlib import Path
import networkx as nx

dataset_dir = Path(__file__).resolve().parent.parent.parent / 'dataset'
cnf_dir = Path(__file__).resolve().parent.parent.parent / 'cnf'

def write_cnf(cnf, name):
    with open(cnf_dir / f'{name}.cnf', 'w') as file:
        file.write(f'p cnf {cnf.nv} {len(cnf.clauses)}\n')
        for clause in cnf.clauses:
            file.write(' '.join(map(str, clause)) + " 0\n")

def rome_graphs():
    """
    Generator that reads all GML files from the 'rome' subdirectory in the dataset 
    and yields them as networkx graphs.
    
    :yield: A networkx graph loaded from a GML file in the 'rome' subdirectory.
    """
    rome_dir = dataset_dir / 'rome' / 'data'
    
    for gml_file in rome_dir.glob('*.gml'):
        try:
            G = nx.read_gml(gml_file)
            G.name = gml_file.name
            yield G
        except Exception as e:
            print(f"Failed to read {gml_file.name}: {e}")

def north_graphs():
    """
    Generator that reads all GML files from the 'north' subdirectory in the dataset 
    and yields them as networkx graphs.
    
    :yield: A networkx graph loaded from a GML file in the 'north' subdirectory.
    """
    north_dir = dataset_dir / 'north' / 'data'
    
    for gml_file in north_dir.glob('*.gml'):
        try:
            G = nx.read_gml(gml_file)
            G.name = gml_file.name
            yield G
        except Exception as e:
            print(f"Failed to read {gml_file.name}: {e}")
