library(unifDAG)

# Range of n values
n_values <- 7:20
num_samples <- 10000

for (n in n_values) {
  output_file <- sprintf("uniform_n%d_%d_dags.txt", n, num_samples)
  file_conn <- file(output_file, open = "w")

  cat(sprintf("Generating %d DAGs for n = %d → %s\n", num_samples, n, output_file))

  for (i in 1:num_samples) {
    dag <- unifDAG(n)
    amat <- as(dag, "matrix")

    edges <- which(amat != 0, arr.ind = TRUE)
    edge_list <- apply(edges, 1, function(row) {
      sprintf("(%d, %d)", row[1] - 1, row[2] - 1)  # 0-based indexing
    })

    line <- paste0("[", paste(edge_list, collapse = ", "), "]")
    writeLines(line, file_conn)
  }

  close(file_conn)
}
