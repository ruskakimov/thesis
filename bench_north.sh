#!/bin/bash

# Print the table header
echo "Filename | Processing Time"
echo "-----------------------------------------"

echo "command,mean,stddev,median,user,system,min,max" > bench_north.csv

# Loop through all CNF files in ./cnf/north_SAT1
for file1 in ./cnf/north_SAT1/*.cnf
do
  # Extract just the filename (without path)
  filename=$(basename "$file1")

  # Define the corresponding file in ./cnf/north_SAT2
  file2="./cnf/north_SAT2/$filename"

  # Check if the corresponding file exists
  if [[ -f "$file2" ]]; then
    printf "Running for file: %s\n" "$filename"

    v1="./solvers/kissat-4.0.1-apple-amd64 $file1"
    v2="./solvers/kissat-4.0.1-apple-amd64 $file2"

    hyperfine --warmup 1 -i --time-unit second --export-csv temp.csv "$v1" "$v2"

    tail -n +2 temp.csv >> bench_north.csv  # Append results without header

    echo "-----------------------------------------"
  else
    echo "Skipping $filename (no matching file in north_SAT2)"
  fi

# Cleanup
rm temp.csv

done
