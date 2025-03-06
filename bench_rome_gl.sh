#!/bin/bash

# Print the table header
echo "Filename | Processing Time"
echo "-----------------------------------------"

output=bench_rome_gl_sat1.csv

echo "command,mean,stddev,median,user,system,min,max" > $output

# Loop through all CNF files in ./cnf/north_SAT1
for file in ./cnf/rome_GL_SAT1/*.cnf
do
    printf "Running for file: %s\n" "$file"

    hyperfine --warmup 1 -i --time-unit second --export-csv temp.csv "./solvers/kissat-4.0.1-apple-amd64 -q $file"

    tail -n +2 temp.csv >> $output  # Append results without header

    echo "-----------------------------------------"

# Cleanup
rm temp.csv

done


