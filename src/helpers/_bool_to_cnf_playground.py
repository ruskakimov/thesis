from sympy import symbols, Implies, And
from sympy.logic.boolalg import to_cnf

# abc
# Lxab, Lxbc, Lxca, Lxba, Lxcb, Lxac = symbols('Lxab Lxbc Lxca -Lxab -Lxbc -Lxca')
# formula = (Lxab & Lxbc & Lxca) | (Lxba | Lxcb | Lxac)

# abcd
Lij, Ljk, Lik = symbols('Lij Ljk Lik')
formula = Implies(And(Lij, Ljk), Lik)

# Convert to CNF
cnf_formula = to_cnf(formula)
print(cnf_formula)

# For abc
# (-Lxab | -Lxbc | -Lxca | Lxab) &
# (-Lxab | -Lxbc | -Lxca | Lxbc) &
# (-Lxab | -Lxbc | -Lxca | Lxca)

# for abcd
# (-Lxab | -Lxbc | -Lxcd | -Lxda | Lxab) &
# (-Lxab | -Lxbc | -Lxcd | -Lxda | Lxbc) &
# (-Lxab | -Lxbc | -Lxcd | -Lxda | Lxcd) &
# (-Lxab | -Lxbc | -Lxcd | -Lxda | Lxda)