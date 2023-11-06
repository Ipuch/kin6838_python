"""
KIN6838 - Cours 3

Frame exercice.
"""
import numpy as np
import matplotlib.pyplot as plt


# Voici les coordonnées des points pour l'exerice
A = np.array([0.1,0.2,0.3])
B = np.array([0.2,0.4,0.5])
C = np.array([1,2,3])

# Determinier x,y,z axis avec la méthode présentée dans le cours.

def build_frame(a,b,c):
    
    # step 2
    x = (b - a)/ np.linalg.norm(b - a)
    
    # temporary axis - step 3
    t = (c - a)/ np.linalg.norm(c - a)
    
    # step 4 
    # np.cross() est utiliser pour faire le produit vectoriel (cross product)
    z = np.cross(x, t) / np.linalg.norm(np.cross(x, t))
    
    # step 5 - Soyez sur de construire un repère directe.
    y = np.cross(z, x) # pas besoin de normalisation car z et x sont déjà unitaires.
    
    return x, y, z


def display_frames_and_points(a, b, c, x, y, z):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the points A, B, and C
    ax.scatter(*a, c='k', marker='o', s=100, label='A')
    ax.scatter(*b, c='k', marker='o', s=100, label='B')
    ax.scatter(*c, c='k', marker='o', s=100, label='C')
    
    # Display the frame based on the axes x, y, z
    ax.quiver(*a, *x, color='r', length=1, normalize=True, label="X-axis")
    ax.quiver(*a, *y, color='g', length=1, normalize=True, label="Y-axis")
    ax.quiver(*a, *z, color='b', length=1, normalize=True, label="Z-axis")
    
    ax.set_xlim([0, max(a[0], b[0], c[0]) + 1])
    ax.set_ylim([0, max(a[1], b[1], c[1]) + 1])
    ax.set_zlim([0, max(a[2], b[2], c[2]) + 1])
    
    # Set aspect ratio to be equal
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for x, y, and z axes
    
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    
    plt.title("3D Frame and Points Visualization")
    plt.show()


print(build_frame(A, B, C))
# Displaying the frames and points using matplotlib
display_frames_and_points(A, B, C, *build_frame(A, B, C))

