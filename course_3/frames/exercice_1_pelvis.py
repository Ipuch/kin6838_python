"""
KIN6838 - Cours 3

Frame exercice.
"""
import numpy as np
import matplotlib.pyplot as plt
from pyomeca import Markers
            
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
    
    
    Regarder la publication, disponible dans le dossier du cours :
        
    Wu, G., Siegler, S., Allard, P., Kirtley, C., Leardini, A., Rosenbaum, 
    D., ... & Stokes, I. (2002). 
    ISB recommendation on definitions of joint coordinate system of various 
    joints for the reporting of human joint motion—part I: ankle, hip, and spine. 
    Journal of biomechanics, 35(4), 543-548.

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

    MPSIS = ...
    origin = MPSIS

    Z_axis = ...
    Y_axis = ...
    Y_axis = ...
    X_axis = ...

    return X_axis, Y_axis, Z_axis, origin


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


repere_pelvis = repere_ISB_pelvis(
    rasis=markers[:3, 0],
    lasis=markers[:3, 1],
    rpsis=markers[:3, 2],
    lpsis=markers[:3, 3])

print(repere_pelvis)

# Displaying the frames and points using matplotlib
display_frames_and_points(markers, repere_pelvis)

