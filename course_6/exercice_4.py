import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L1 = 0.3
# L2 = 0.29  only one segment in this simulation.

# Colors for the links
color_1 = (1, 0.45, 0.1)

def forward_kinematics_model(q):
    """Compute the forward kinematics for a given joint configuration."""
    return np.array([
        # Ajouter le modèle de géométrie directe du marqueur situé à L1 selon x
        # composante en x,
        # composante en y,
    ])
    
def compute_jacobian(q):
    """Compute the Jacobian for a given joint configuration."""
    return np.array([
        # Ajouter la jacobienne du modèle de géométrie directe.
        # ...
        # ...
    ])

def compute_residual(q, m):
    """Compute the residual between the current position and target position."""
    return # Calculer le résidu entre les modèle de géométrie directe et les marqueurs xp
           # modele de geometrie - marqueurs
                    
def compute_pseudo_inverse(q):
    """Compute the pseudo-inverse of the Jacobian."""
    # J = ... calcule de la jacobienne
    # return - # Calcul de la pseudo-inverse


marker_location = np.array([
    # entrée une composante en x
    # entrée une composante en y
     ])
initial_guess = np.array([
    # q at the initialization of the optimization
    ])  
convergence_tolerance = 0.001

# Storage for animation
configurations = [initial_guess]

# Nonlinear Least-Square Gauss-Newton Optimization
delta_q = 10  # artificially superior to the tolerance criterion
current_q = initial_guess

while np.linalg.norm(delta_q) > 0.001:
    
    # delta_q = # calculer la variation de q
    # current_q = # calculer le nouveau q
    
    configurations.append(current_q.copy())


# Animation function
def animate(i):
    plt.gca().cla()  # Clear the current axis

    plt.plot(marker_location[0], marker_location[1], 'bo', label='Target Position' if i == 0 else "")
    plt.xlim([-0.5, 0.5])
    plt.ylim([-0.5, 0.5])
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.grid(True)
    plt.title('Progression of the Optimization')

    current_position = forward_kinematics_model(configurations[i])
    plt.plot([0, current_position[0,0]], [0, current_position[1,0]], '-', color=color_1, lw=6)
    plt.plot(current_position[0], current_position[1], 'ro')
    
fig = plt.figure()
ani = FuncAnimation(fig, animate, frames=len(configurations), repeat=False, interval=500)
plt.legend()
plt.show()
    
