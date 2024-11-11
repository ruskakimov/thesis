#!/bin/bash

# Print the table header
echo "n | Processing Time"
echo "-----------------------------------------"

# Loop through the range [2, 20]
for n in {2..20}
do
  printf "Running for n = %d\n" "$n"
  
  time ./solvers/kissat-4.0.1-apple-amd64 "./cnf/grid_dag_${n}x${n}.cnf" > /dev/null

  echo "-----------------------------------------"
done
