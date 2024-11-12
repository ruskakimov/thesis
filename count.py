# v1 kUBE encoding
# =================
# O(n^2 + m^2)
def v1_vars(n, m, k):
    return n*(n-1)/2 + m*k + m*(m-1)/2

# O(n^3 + m^2)
def v1_clauses(n, m, k):
    return n*(n-1)*(n-2) + m + m + m*k*(k-1)/2 + m*(m-1)/2*k + m*(m-1)/2*8


# v2 2UBE encoding
# =================
# O(n^2 + m)
def v2_vars(n, m):
    return n*(n-1)/2 + m

# O(n^3 + m^2)
def v2_clauses(n, m):
    return n*(n-1)*(n-2) + m + m*(m-1)/2*4


for n in range(2, 29):
    # Number of edges in a grid graph
    m = 2*n*(n-1)

    v1_v = v1_vars(n*n, m, 2)
    v1_c = v1_clauses(n*n, m, 2)

    v2_v = v2_vars(n*n, m)
    v2_c = v2_clauses(n*n, m)

    # percentage reduction of variables
    reduction_v = (v1_v - v2_v) / v1_v * 100

    # percentage reduction of clauses
    reduction_c = (v1_c - v2_c) / v1_c * 100

    print(n, reduction_v, reduction_c)