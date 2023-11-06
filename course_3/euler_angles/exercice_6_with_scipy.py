"""
KIN6838 - Cours 3

Matrice de rotation avec une séquence d'angles d'euler prédéfinies
"""

from scipy.spatial.transform import Rotation as R
import numpy as np

r = R.from_matrix([[0.940, -0.339, 0.030],
    [0.339, 0.925, -0.171],
    [0.030, 0.171, 0.985]]
                  )

print(r.as_matrix())
# attention les conventions de scipy sont inversées
# convention for angles sequence are opposed in scipy
# xyz -> scipy -> zyx
angles = r.as_euler("zyx", degrees=True)

print("alpha, rotation X: ", angles[2], " deg")
print("beta, rotation Y: ", angles[1], " deg")
print("gamma, rotation Z: ", angles[0], " deg")


