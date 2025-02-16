#!/bin/bash

f1=grid_sat1_vars_clauses.csv
f2=grid_sat2_vars_clauses.csv

echo "n,vars,clauses" > $f1
echo "n,vars,clauses" > $f2

for n in {2..28}
do
  file1="./cnf/grid_dag_${n}x${n}.cnf"
  file2="./cnf/grid_dag_v2_${n}x${n}.cnf"

  read -r first_line_sat1 < "$file1"
  read -r first_line_sat2 < "$file2"

  read -r _ _ cnf_v1 cnf_c1 <<< "$first_line_sat1"
  read -r _ _ cnf_v2 cnf_c2 <<< "$first_line_sat2"

  echo "$n, $cnf_v1, $cnf_c1" >> "$f1"
  echo "$n, $cnf_v2, $cnf_c2" >> "$f2"
done
