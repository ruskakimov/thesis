from sympy import symbols
from sympy.logic.boolalg import to_cnf

# abc
# Lxab, Lxbc, Lxca, Lxba, Lxcb, Lxac = symbols('Lxab Lxbc Lxca -Lxab -Lxbc -Lxca')
# formula = (Lxab & Lxbc & Lxca) | (Lxba | Lxcb | Lxac)

# abcd
Lxab, Lxbc, Lxcd, Lxda, Lxba, Lxcb, Lxdc, Lxad = symbols('Lxab Lxbc Lxcd Lxda -Lxab -Lxbc -Lxcd -Lxda')
formula = (Lxab & Lxbc & Lxcd & Lxda) | (Lxba | Lxcb | Lxdc | Lxad)

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