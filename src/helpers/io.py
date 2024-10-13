from pathlib import Path

cnf_dir = Path(__file__).resolve().parent.parent / 'cnf'

def write_cnf_to_file(num_vars, clauses, name):
    with open(cnf_dir / f'{name}.cnf', 'w') as file:
        file.write(f'p cnf {num_vars} {len(clauses)}\n')
        for clause in clauses:
            file.write(' '.join(map(str, clause)) + " 0\n")
