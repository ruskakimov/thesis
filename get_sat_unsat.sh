#!/bin/bash

output_filename="random_dag_sat_unsat.txt"
echo "" > $output_filename

# Loop through all CNF files in ./cnf/north_SAT1
for file1 in ./cnf/random_dag_SAT1/*.cnf
do
  # Extract just the filename (without path)
  filename=$(basename "$file1")

  # Define the corresponding file in ./cnf/north_SAT2
  file2="./cnf/random_dag_SAT2/$filename"

  # Check if the corresponding file exists
  if [[ -f "$file2" ]]; then
    printf "Running for file: %s\n" "$filename"

    v1="./solvers/kissat-4.0.1-apple-amd64 $file1"
    v2="./solvers/kissat-4.0.1-apple-amd64 $file2"

    echo $filename >> $output_filename
    ./solvers/kissat-4.0.1-apple-amd64 $file2 --quiet >> $output_filename
    echo '-' >> $output_filename
  else
    echo "Skipping $filename (no matching file in north_SAT2)"
  fi

done
