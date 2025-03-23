library(unifDAG)

generate_dags_per_m <- function(n, per_m = 50, max_attempts = 1e6) {
  max_edges <- n * (n - 1) / 2
  output_file <- sprintf("n%d_balanced_dags.txt", n)
  file_conn <- file(output_file, open = "w")

  cat(sprintf("Generating %d DAGs per m for n = %d → %s\n", per_m, n, output_file))

  m_counts <- integer(max_edges + 1)
  attempts <- 0

  while (any(m_counts < per_m) && attempts < max_attempts) {
    dag <- unifDAG(n)
    amat <- as(dag, "matrix")
    edges <- which(amat != 0, arr.ind = TRUE)
    m <- nrow(edges)
    attempts <- attempts + 1

    if (m_counts[m + 1] >= per_m) next

    edge_list <- apply(edges, 1, function(row) {
      sprintf("(%d, %d)", row[1] - 1, row[2] - 1)
    })
    line <- paste0("[", paste(edge_list, collapse = ", "), "]")
    writeLines(line, file_conn)

    m_counts[m + 1] <- m_counts[m + 1] + 1

    # --- Custom compact progress ---
    symbols <- sapply(m_counts, function(count) {
      if (count == 0) "0"
      else if (count >= per_m) "✓"
      else as.character(min(9, floor(10 * count / per_m)))
    })
    cat("\r[", paste(symbols, collapse = ""), "]")
    flush.console()
  }

  cat("\n✅ Finished n =", n, "| Total DAGs written:", sum(m_counts), "\n\n")
  close(file_conn)
}


# Run for a range of n values
n_values <- 7:10
for (n in n_values) {
  generate_dags_per_m(n, per_m = 50)
}
