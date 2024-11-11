#!/bin/bash

# Print the table header
echo "n | Processing Time"
echo "-----------------------------------------"

for n in {2..28}
do
#   printf "Running for n = %d\n" "$n"
  
#   time ./solvers/kissat-4.0.1-apple-amd64 "./cnf/grid_dag_${n}x${n}.cnf" > /dev/null

  # stat -f%z "./cnf/grid_dag_${n}x${n}.cnf"
  head -n 1 "./cnf/grid_dag_${n}x${n}.cnf"

#   echo "-----------------------------------------"
done
