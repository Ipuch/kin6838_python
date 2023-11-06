"""
KIN6838 - Cours 3

Matrice de rotation avec une séquence d'angles d'euler prédéfinies
"""
import numpy as np

R_01 = np.array([
    [0.940, -0.339, 0.030],
    [0.339, 0.925, -0.171],
    [0.030, 0.171, 0.985]
])

def identifier_xyz_angles(rotation_matrix):
    
    
    # on préfère utiliser arctan2 qui est plus robuste que 
    # np.arctan
    # np.arctan2(denomiteur, numerateur)
    alpha = - np.arctan2(rotation_matrix[1,2], rotation_matrix[2,2])
    
    beta = np.arcsin(rotation_matrix[0,2])
    
    gamma = - np.arctan2(rotation_matrix[0,1], rotation_matrix[0,0])
    
    return alpha, beta, gamma


# on aime bien vérifier que le determinant d'une matrice de rotation
# est de 1.
print(np.linalg.det(R_01))

xyz = identifier_xyz_angles(R_01)

print("alpha, rotation X: ", xyz[0] * 180 / np.pi, " deg")
print("beta, rotation Y: ", xyz[1] * 180 / np.pi, " deg")
print("gamma, rotation Z: ", xyz[2] * 180 / np.pi, " deg")