#!/bin/bash

f1=north_sat1_vars_clauses.csv
f2=north_sat2_vars_clauses.csv

echo "graph,vars,clauses" > $f1
echo "graph,vars,clauses" > $f2

# Loop through all CNF files in ./cnf/north_SAT1
for file1 in ./cnf/north_SAT1/*.cnf
do
  # Extract just the filename (without path)
  filename=$(basename "$file1")

  # Define the corresponding file in ./cnf/north_SAT2
  file2="./cnf/north_SAT2/$filename"

  read -r first_line_sat1 < "$file1"
  read -r first_line_sat2 < "$file2"

  read -r _ _ cnf_v1 cnf_c1 <<< "$first_line_sat1"
  read -r _ _ cnf_v2 cnf_c2 <<< "$first_line_sat2"

  echo "$filename, $cnf_v1, $cnf_c1" >> "$f1"
  echo "$filename, $cnf_v2, $cnf_c2" >> "$f2"

done
