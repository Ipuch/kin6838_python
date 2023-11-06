import numpy as np
from scipy.spatial.transformation import Rotation


def homogeneous_matrix(q, L):
    """
    Compute the homogeneous transformation matrix for one segment.
 
    Parameters:
        - q (float): Joint angle in radians.
        - L (float): Link length.
 
    Returns:
        - numpy.ndarray: 4x4 homogeneous transformation matrix.
    """
    # Use scipy to generate a 2D rotation matrix
    rot_matrix = Rotation.from_euler('z', q).as_matrix()
    
    # Create the homogeneous matrix
    matrix = np.eye(4)
    matrix[:3, :3] = rot_matrix
    matrix[0, 3] = L
    
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
    T02 = T01 @ T12
    
    # marker location in 2
    marker_in_2 = np.array([L2, 0, 0])
    
    # Compute the location in 0
    marker_in_0 = T02 @ np.hstack((marker_in_2, 1))
    
    return marker_in_0

print(forward_kinematics_homogeneous(np.pi/4, np.pi/4, 0.30, 0.29))
print(forward_kinematics_homogeneous(np.pi/3, np.pi/4, 0.30, 0.29))
    