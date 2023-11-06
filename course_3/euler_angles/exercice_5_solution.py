"""
KIN6838 - Cours 3

Matrice de rotation avec une séquence d'angles d'euler prédéfinies
"""
import sympy as sp

alpha = sp.symbols("alpha")
beta = sp.symbols("beta")
gamma = sp.symbols("gamma")

# Rotation matrix around X-axis
R_x = sp.Matrix([
    [1, 0, 0],
    [0, sp.cos(alpha), -sp.sin(alpha)],
    [0, sp.sin(alpha), sp.cos(alpha)]
])


# Rotation matrix around Y-axis
R_y = sp.Matrix([
    [sp.cos(beta), 0, sp.sin(beta)],
    [0, 1, 0],
    [-sp.sin(beta), 0, sp.cos(beta)]
])

# Rotation matrix around Z-axis
R_z = sp.Matrix([
    [sp.cos(gamma), -sp.sin(gamma), 0],
    [sp.sin(gamma), sp.cos(gamma), 0],
    [0, 0, 1]
])

R_xyz = R_x @ R_y @ R_z

sp.pprint(R_xyz, use_unicode=True)