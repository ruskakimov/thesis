# v1 kUBE encoding
# =================
# O(n^2 + m^2)
def v1_vars(n, m, k):
    return n*(n-1)/2 + m*k + m*(m-1)/2

# O(n^3 + m^2)
def v1_clauses(n, m, k):
    return n*(n-1)*(n-2) + m + m + m*k*(k-1)/2 + m*(m-1)/2*k + m*(m-1)/2*8

for n in range(2, 29):
    # Number of edges in a grid graph
    m = 2*n*(n-1)

    print(n, v1_vars(n*n, m, 2), v1_clauses(n*n, m, 2))

# =================