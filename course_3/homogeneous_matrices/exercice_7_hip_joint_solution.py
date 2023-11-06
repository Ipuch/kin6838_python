"""
KIN6838 - Cours 3

Homogenous transformation exercise
"""
import numpy as np
import matplotlib.pyplot as plt
from pyomeca import Markers
import xarray as xr
            
c3d_filename = "2014001_ST.c3d"

# on charge les marqueurs du bassin seulement
markers = Markers.from_c3d(c3d_filename,usecols=["R_IAS","L_IAS","R_IPS","L_IPS"])
markers = markers/1000
markers.attrs["units"] = 'm'

# Charger la 1ère première frame du .c3d seulement.
markers = markers[:, :, 0]


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


def display_frames_and_points(markers, pelvis_tuple):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    for m in markers.T:
        ax.scatter(*m[:3], marker='o', s=100, label=str(m.channel.coords["channel"].values))
    
    # Display the frame based on the axes x, y, z
    ax.quiver(*pelvis_tuple[-1], *pelvis_tuple[0], color='r', length=1, normalize=True, label="X-axis")
    ax.quiver(*pelvis_tuple[-1], *pelvis_tuple[1], color='g', length=1, normalize=True, label="Y-axis")
    ax.quiver(*pelvis_tuple[-1], *pelvis_tuple[2], color='b', length=1, normalize=True, label="Z-axis")
    
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
    

x_axis, y_axis, z_axis, origin = repere_ISB_pelvis(
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

# Displaying the frames and points using matplotlib
display_frames_and_points(combined_markers, (x_axis, y_axis, z_axis, origin))


print("Pelvs Frame:",  (x_axis, y_axis, z_axis, origin))
print("Hip joint centers in global:", (right_hip_joint_center, left_hip_joint_center) )

# CALCULER LA TRANSFORMATION HOMOGENE du repère global vers le repère pelvis
T01 = np.concatenate(
    (x_axis[:,np.newaxis],
     y_axis[:,np.newaxis],
     z_axis[:,np.newaxis],
     origin[:,np.newaxis],
     ), axis=1)
T01 = np.concatenate((T01, np.array([[0,0,0,1]])), axis=0)
print(T01)


# CALCULER LA POSITION DE LA HANCHE DROITE DANS LE REPERE PELVIS
right_hip_in_pelvis = np.linalg.inv(T01) @ right_hip_joint_center
left_hip_in_pelvis =  np.linalg.inv(T01) @ left_hip_joint_center

print(right_hip_in_pelvis)
print(left_hip_in_pelvis)


