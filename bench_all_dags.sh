#!/bin/bash

# Output CSV file
output="bench_rome_gl_sat1_results.csv"

# Write CSV header
echo "name,time_seconds,result" > "$output"

# Loop through all CNF files in ./cnf/rome_GL_SAT1
for file in ./cnf/rome_GL_SAT1/*.cnf; do
    echo "Processing file: $file"

    # Record start time in seconds with nanosecond precision
    start=$(date +%s.%N)
    
    # Run kissat and capture its output
    solver_output=$(./solvers/kissat-4.0.1-apple-amd64 -q "$file")
    
    # Record end time
    end=$(date +%s.%N)
    
    # Compute elapsed time using bc for floating point arithmetic
    elapsed=$(echo "$end - $start" | bc)
    
    # Determine result from solver output
    if echo "$solver_output" | grep -q "UNSATISFIABLE"; then
        result="UNSAT"
    elif echo "$solver_output" | grep -q "SATISFIABLE"; then
        result="SAT"
    else
        result="UNKNOWN"
    fi

    # Append file name (basename), time, and result to the CSV
    echo "$(basename "$file"),$elapsed,$result" >> "$output"
done
