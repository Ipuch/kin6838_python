"""
KIN6838 - Cours 3

Matrice de rotation avec une séquence d'angles d'euler prédéfinies
"""

from biorbd import Rotation  # conda install -c conda-forge biorbd
import numpy as np

def rotation_matrix_from_numpy_to_biorbd(R: np.ndarray) -> Rotation:
    """ This function returns the rotation matrix in biorbd formalism """

    return Rotation(
        R[0, 0],
        R[0, 1],
        R[0, 2],
        R[1, 0],
        R[1, 1],
        R[1, 2],
        R[2, 0],
        R[2, 1],
        R[2, 2],
    )


def rotation_matrix_to_euler_angles(rotation_matrix: np.ndarray, seq: str = "xyz") -> np.ndarray:
    """
    This function returns the rotation matrix in euler angles vector

    Parameters
    ---------
    rotation_matrix : np.ndarray
        Rotation matrix (3x3)
    seq: str = "xyz"
        order of the coordinates in the returned vector
    Returns
    ---------
    Rotation.toEulerAngles(rotation_matrix_biorbd, seq).to_array()
        The Euler vector in radiant as an array
    """

    rotation_matrix_biorbd = rotation_matrix_from_numpy_to_biorbd(rotation_matrix)
    return Rotation.toEulerAngles(rotation_matrix_biorbd, seq).to_array()

R_01 = np.array([
    [0.940, -0.339, 0.030],
    [0.339, 0.925, -0.171],
    [0.030, 0.171, 0.985]
])

euler_angles = rotation_matrix_to_euler_angles(R_01, "xyz")

print("alpha, rotation X: ", euler_angles[0] * 180 / np.pi, " deg")
print("beta, rotation Y: ", euler_angles[1] * 180 / np.pi, " deg")
print("gamma, rotation Z: ", euler_angles[2] * 180 / np.pi, " deg")