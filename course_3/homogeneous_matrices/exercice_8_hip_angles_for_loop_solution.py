"""
KIN6838 - Cours 3

Homogenous transformation exercise
"""
import numpy as np
import matplotlib.pyplot as plt
from pyomeca import Markers
from biorbd import Rotation
import xarray as xr


def repere_ISB_pelvis(rasis, lasis, rpsis, lpsis):
    """
    Calcule le repère du pelvis en accord avec l'ISB recommendations
    Origine milieu psis & lpsis.

    Parameters
    ---------
    rasis : np.ndarray
        position of RASIS RIGHT ANTERIOR SUPERIOR ILIAC SPINE (3)
    lasis : np.ndarray
            position of LASIS LEFT ANTERIOR SUPERIOR ILIAC SPINE (3)
    rpsis : np.ndarray
            position of RPSIS RIGHT POSTERIOR SUPERIOR ILIAC SPINE (3)
    lpsis : np.ndarray
            position of LPSIS LEFT POSTERIOR SUPERIOR ILIAC SPINE (3)

    Returns
    -------
    tuple x, y, z, origin
    
    """

    MPSIS = (rpsis + lpsis) / 2
    origin = MPSIS

    Z_axis = (rasis - lasis) / np.linalg.norm(rasis - lasis)
    Y_axis = np.cross((rasis - MPSIS), (lasis - MPSIS))
    Y_axis = Y_axis / np.linalg.norm(Y_axis)
    X_axis = np.cross(Y_axis, Z_axis)

    return X_axis, Y_axis, Z_axis.to_numpy(), origin.to_numpy()

def repere_ISB_cuisse_prox(cond_g, cond_d, hjc):
    """
    Computes the thigh reference frame in accordance with the ISB recommendations,
    with the origin at the femoral head.

    Parameters
    ----------
    cond_g : np.ndarray
        Position of the Cond_G point (3 coordinates).
    cond_d : np.ndarray
        Position of the Cond_D point (3 coordinates).
    hjc : np.ndarray
        Position of the hip joint center, HJC (3 coordinates).

    Returns
    -------
    tuple x, y, z, origin
    """

    # Calculate Y_axis
    Y_axis = (hjc - (cond_g + cond_d) / 2) / np.linalg.norm(hjc - (cond_g + cond_d) / 2)

    # Calculate X_axis
    X_axis = np.cross((cond_d - hjc), (cond_g - hjc))
    X_axis = X_axis / np.linalg.norm(X_axis)

    # Calculate Z_axis
    Z_axis = np.cross(X_axis, Y_axis)

    origin = hjc

    return X_axis, Y_axis.to_numpy(), Z_axis, origin.to_numpy()


def harrington2007(rasis: np.ndarray, lasis: np.ndarray, rpsis: np.ndarray, lpsis: np.ndarray) -> tuple:
    """
    This function computes the hip joint center from the RASIS, LASIS, RPSIS and LPSIS markers
    RASIS: RASIS marker

    Parameters
    ----------
    RASIS: np.ndarray
        RASIS marker location in meters
    LASIS: np.ndarray
        LASIS marker location in meters
    RPSIS: np.ndarray
        RPSIS marker location in meters
    LPSIS: np.ndarray
        LPSIS marker location in meters

    Returns
    -------
    tuple(np.ndarray, np.ndarray)
        The right and left hip joint center in global coordinates system in meters
        
    Source
    ------
    Harrington, M. E., Zavatsky, A. B., Lawson, S. E. M., Yuan, Z., 
    & Theologis, T. N. (2007). Prediction of the hip joint centre in adults, 
    children, and patients with cerebral palsy based on magnetic resonance imaging.
    Journal of biomechanics, 40(3), 595-602.
    
    """
    # convert inputs in millimeters
    rasis = rasis.to_numpy()[:3, np.newaxis] * 1000
    lasis = lasis.to_numpy()[:3, np.newaxis] * 1000
    rpsis = rpsis.to_numpy()[:3, np.newaxis] * 1000
    lpsis = lpsis.to_numpy()[:3, np.newaxis] * 1000

    # Right-handed Pelvis reference system definition
    Sacrum = (rpsis + lpsis) / 2
    # Global Pelvis center position
    OP = (rasis + lasis) / 2

    rhjc_global = np.zeros((4, rasis.shape[1]))
    lhjc_global = np.zeros((4, rasis.shape[1]))

    for i in range(rasis.shape[1]):
        provv = (rasis[:3, i] - Sacrum[:3, i]) / np.linalg.norm(rasis[:3, i] - Sacrum[:3, i])
        ib = (rasis[:3, i] - lasis[:3, i]) / np.linalg.norm(rasis[:3, i] - lasis[:3, i])

        kb = np.cross(ib, provv) / np.linalg.norm(np.cross(ib, provv))
        jb = np.cross(kb, ib) / np.linalg.norm(np.cross(kb, ib))

        OB = OP[:3, i]
        # Rotation + translation in homogenous matrix
        Pelvis = np.array(
            [[ib[0], jb[0], kb[0], OB[0]], [ib[1], jb[1], kb[1], OB[1]], [ib[2], jb[2], kb[2], OB[2]], [0, 0, 0, 1]]
        )

        # Transformation from global to pelvis reference system
        OPB = np.linalg.inv(Pelvis) @ np.hstack((OB, 1))

        PW = np.linalg.norm(rasis[:3, i] - lasis[:3, i])  # PW: width of pelvis (distance among ASIS)
        PD = np.linalg.norm(
            Sacrum[:3, i] - OP[:3, i]
        )  # PD: pelvis depth = distance between mid points joining PSIS and ASIS

        # Harrington formula in mm
        diff_ap = -0.24 * PD - 9.9
        diff_v = -0.3 * PW - 10.9
        diff_ml = 0.33 * PW + 7.3

        # vector that must be subtract to OP to obtain hjc in pelvis CS
        vett_diff_pelvis_sx = np.array([-diff_ml, diff_ap, diff_v, 1])
        vett_diff_pelvis_dx = np.array([diff_ml, diff_ap, diff_v, 1])

        # hjc in pelvis CS (4x4)
        rhjc_pelvis = OPB[:3] + vett_diff_pelvis_dx[:3]
        lhjc_pelvis = OPB[:3] + vett_diff_pelvis_sx[:3]

        # transformation from pelvis to global CS
        rhjc_global[:3, i] = Pelvis[:3, :3] @ rhjc_pelvis + OB
        lhjc_global[:3, i] = Pelvis[:3, :3] @ lhjc_pelvis + OB

    rhjc_global[:3, :] /= 1000
    lhjc_global[:3, :] /= 1000
    rhjc_global[-1, :] = 1
    lhjc_global[-1, :] = 1

    return rhjc_global, lhjc_global

def display_frames_and_points(markers, pelvis_tuple, femur_tuple):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    for m in markers.T:
        ax.scatter(*m[:3], marker='o', s=100, label=str(m.channel.coords["channel"].values))
    
    # Display the frame based on the axes x, y, z
    ax.quiver(*pelvis_tuple[-1], *pelvis_tuple[0], color='r', length=1, normalize=True, label="X-axis")
    ax.quiver(*pelvis_tuple[-1], *pelvis_tuple[1], color='g', length=1, normalize=True, label="Y-axis")
    ax.quiver(*pelvis_tuple[-1], *pelvis_tuple[2], color='b', length=1, normalize=True, label="Z-axis")
    
    # Display the frame based on the axes x, y, z
    ax.quiver(*femur_tuple[-1], *femur_tuple[0], color='r', length=1, normalize=True, label="X-axis")
    ax.quiver(*femur_tuple[-1], *femur_tuple[1], color='g', length=1, normalize=True, label="Y-axis")
    ax.quiver(*femur_tuple[-1], *femur_tuple[2], color='b', length=1, normalize=True, label="Z-axis")
    
    ax.set_xlim([0, max(markers[0,:]) + 1])
    ax.set_ylim([0, max(markers[1,:]) + 1])
    ax.set_zlim([0, max(markers[2,:]) + 1])
    
    # Set aspect ratio to be equal
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for x, y, and z axes
    
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    
    plt.title("3D Frame and Points Visualization")
    plt.show()

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

##########################################################################
# On commence là
c3d_filename = "2014001_C1_01.c3d"

# on charge les marqueurs du bassin seulement
all_markers = Markers.from_c3d(c3d_filename,usecols=["R_IAS","L_IAS","R_IPS","L_IPS","R_FME","R_FLE"])
all_markers = all_markers/1000
all_markers.attrs["units"] = 'm'

angles = np.zeros((3, 1, all_markers.shape[2]))

for i in range(all_markers.shape[2]):
    # Charger la frame du .c3d.
    markers = all_markers[:, :, i]


    pelvis_x_axis, pelvis_y_axis, pelvis_z_axis, pelvis_origin = repere_ISB_pelvis(
        rasis=markers[:3, 0],
        lasis=markers[:3, 1],
        rpsis=markers[:3, 2],
        lpsis=markers[:3, 3])
    
    right_hip_joint_center, left_hip_joint_center = harrington2007(
        rasis=markers[:3, 0],
        lasis=markers[:3, 1],
        rpsis=markers[:3, 2],
        lpsis=markers[:3, 3])
    
    hips = xr.DataArray(
        np.concatenate((right_hip_joint_center, left_hip_joint_center),axis=1),
        coords={"axis": ["x", "y", "z", "ones"], "channel": ["R_HIP", "L_HIP"]},
        dims=["axis", "channel"]
        )
    combined_markers = xr.concat([markers, hips], dim="channel")
    
    femur_x_axis, femur_y_axis, femur_z_axis, femur_origin = repere_ISB_cuisse_prox(
       cond_g=combined_markers[:3, 4],
       cond_d=combined_markers[:3, 5],
       hjc=combined_markers[:3, 6],
        )

    # CALCULER LA TRANSFORMATION HOMOGENE du repère global vers le repère pelvis
    T01 = np.concatenate(
        (pelvis_x_axis[:,np.newaxis],
         pelvis_y_axis[:,np.newaxis],
         pelvis_z_axis[:,np.newaxis],
         pelvis_origin[:,np.newaxis],
         ), axis=1)
    T01 = np.concatenate((T01, np.array([[0,0,0,1]])), axis=0)
    
    # CALCULER LA TRANSFORMATION HOMOGENE du repère global vers le repère femur
    T02 = np.concatenate(
        (femur_x_axis[:,np.newaxis],
         femur_y_axis[:,np.newaxis],
         femur_z_axis[:,np.newaxis],
         femur_origin[:,np.newaxis],
         ), axis=1)
    T02 = np.concatenate((T02, np.array([[0,0,0,1]])), axis=0)
    
    # CALCULER LA TRANSFORMATION HOMOGENE du repère pelvis vers le repère femur
    T12 = np.linalg.inv(T01) @ T02  # T10 @ T02
    
    
    # CALCULER LES ANGLES ARTICULAIRES, sequence ZXY (ISB)
    R12 = T12[:3,:3]  # selectionner la matrice de rotation
    
    angles[:, 0, i] = rotation_matrix_to_euler_angles(R12, "zxy") 
    print("Euler Angles:", angles[:,0,i] * 180 / np.pi, "in degrees")
    

# Display joint angles in subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 10))

# Time vector for x-axis
time = all_markers

# Plot alpha (rotation around Z)
axs[0].plot(all_markers["time"], angles[0, 0, :] * 180 / np.pi, '-o')
axs[0].set_title('Alpha (Rotation around Z-axis) \n Flexion (+)/ Extension(-)')
axs[0].set_ylabel('Degrees')
axs[0].grid(True)

# Plot beta (rotation around X)
axs[1].plot(all_markers["time"], angles[1, 0, :] * 180 / np.pi, '-o')
axs[1].set_title('Beta (Rotation around X-axis \n Adduction(+)/ Abduction(-)')
axs[1].set_ylabel('Degrees')
axs[1].grid(True)

# Plot gamma (rotation around Y)
axs[2].plot(all_markers["time"], angles[2, 0, :] * 180 / np.pi, '-o')
axs[2].set_title('Gamma (Rotation around Y-axis \n Rot Int(+)/ Ext(-)')
axs[2].set_xlabel('Time (s)')
axs[2].set_ylabel('Degrees')
axs[2].grid(True)

# Adjust layout
plt.tight_layout()
plt.show()




