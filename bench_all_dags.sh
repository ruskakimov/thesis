#!/bin/bash

n=5
output=all_dags_$n\_bench_hyperfine.csv

echo "command,mean,stddev,median,user,system,min,max" > $output

# Loop through all CNF files in ./cnf/north_SAT1
for file in ./cnf/all_dags_$n/*.cnf
do
    printf "Running for file: %s\n" "$file"

    hyperfine --warmup 1 -i --time-unit second --runs 10 --export-csv temp.csv "./solvers/kissat-4.0.1-apple-amd64 -q $file"

    tail -n +2 temp.csv >> $output  # Append results without header

    echo "-----------------------------------------"

# Cleanup
rm temp.csv

done
