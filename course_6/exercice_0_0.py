import numpy as np


def homogeneous_matrix(q, L):
    """
    Compute the homogeneous transformation matrix for one segment.
 
    Parameters:
        - q (float): Joint angle in radians.
        - L (float): Link length.
 
    Returns:
        - numpy.ndarray: 4x4 homogeneous transformation matrix.
    """
    
    # matrix = ...
    
    return matrix

def forward_kinematics_homogeneous(q1, q2, L1, L2):
    """
    Compute the forward kinematics using homogeneous matrices.
    
    Returns:
    - numpy.ndarray: 4x1 array of the marker's position [x, y, z, 1].
    
    """
    T01 = homogeneous_matrix(q1, 0)
    T12 = homogeneous_matrix(q2, L1)
    
    # Multiply the matrices to get the combined transformation
    # T02 = ....
    
    # marker location in 2
    marker_in_2 = np.array([L2, 0, 0])
    
    # Compute the location in 0 
    # (don't forget to had a 1 to transform it as an homogenous coordinate)
    # marker_in_0 = ...
    
    return marker_in_0

print(forward_kinematics_homogeneous(np.pi/4, np.pi/4, 0.30, 0.29))
print(forward_kinematics_homogeneous(np.pi/3, np.pi/4, 0.30, 0.29))
    