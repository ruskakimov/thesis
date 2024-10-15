from sympy import symbols, Implies, And
from sympy.logic.boolalg import to_cnf

# abc
# Lxab, Lxbc, Lxca, Lxba, Lxcb, Lxac = symbols('Lxab Lxbc Lxca -Lxab -Lxbc -Lxca')
# formula = (Lxab & Lxbc & Lxca) | (Lxba | Lxcb | Lxac)

# abcd
# Lij, Ljk, Lik = symbols('Lij Ljk Lik')
# formula = Implies(And(Lij, Ljk), Lik)

# Convert to CNF
# cnf_formula = to_cnf(formula)
# print(cnf_formula)

# For abc
# (-Lxab | -Lxbc | -Lxca | Lxab) &
# (-Lxab | -Lxbc | -Lxca | Lxbc) &
# (-Lxab | -Lxbc | -Lxca | Lxca)

# for abcd
# (-Lxab | -Lxbc | -Lxcd | -Lxda | Lxab) &
# (-Lxab | -Lxbc | -Lxcd | -Lxda | Lxbc) &
# (-Lxab | -Lxbc | -Lxcd | -Lxda | Lxcd) &
# (-Lxab | -Lxbc | -Lxcd | -Lxda | Lxda)


# a, b, c, d, e, f, x = symbols('a, b, c, d, e, f, x')
# formula = Implies((a & b) | (c & d) | (e & f), x)

# cnf_formula = to_cnf(formula)
# print(cnf_formula) # (x | ~a | ~b) & (x | ~c | ~d) & (x | ~e | ~f)


Xijkl, Lij, Lji, Lkl, Llk, Lik, Lki, Lil, Lli, Ljk, Lkj, Ljl, Llj = symbols('Xijkl, Lij, Lji, Lkl, Llk, Lik, Lki, Lil, Lli, Ljk, Lkj, Ljl, Llj')
# i k j l
# i l j k
# j k i l
# j l i k
# k i l j
# k j l i
# l i k j
# l j k i
formula = Implies(
    Xijkl,
    ~(Lik & Lkj & Ljl) &
    ~(Lil & Llj & Ljk)
)

cnf_formula = to_cnf(formula)
print(cnf_formula)
