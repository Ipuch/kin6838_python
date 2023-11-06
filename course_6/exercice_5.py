import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L10 = 0.3
# Let's add another marker on the first segment
L11 = 0.25
# L2 = 0.29  only one segment in this simulation.

# Colors for the links
color_1 = (1, 0.45, 0.1)

def forward_kinematics_model(q):
    """Compute the forward kinematics for a given joint configuration."""
    return np.array([
        [L10 * np.cos(q[0,0])], 
        [L10 * np.sin(q[0,0])],
        # Ajouter un nouveau marqueur situé à L11 selon x
        # ...
        # ...
    ])
    
def compute_jacobian(q):
    """Compute the Jacobian for a given joint configuration."""
    return np.array([
        [-L10 * np.sin(q[0,0])],
        [L10 * np.cos(q[0,0])],
        # Calculer les termes de sa jacobienne
        # ...
        # ...
    ])

def compute_residual(q, m):
    """Compute the residual between the current position and target position."""
    return forward_kinematics_model(q) - m
                    
def compute_pseudo_inverse(q):
    """Compute the pseudo-inverse of the Jacobian."""
    J = compute_jacobian(q)
    return - np.linalg.inv(J.T @ J) @ J.T


marker_locations = np.array([
    [0.3],
    [0.1],
    # Ajouter un nouveau marqueur experimental
    # ...
    # ...
    ])

initial_guess = np.array([[2.54]])  # q at the initialization of the optimization
convergence_tolerance = 0.001

# Storage for animation
configurations = [initial_guess]

# Nonlinear Least-Square Gauss-Newton Optimization
delta_q = 10  # artificially superior to the tolerance criterion
current_q = initial_guess
loops = 0
while np.linalg.norm(delta_q) > 0.001:

    loops += 1 
    print(loops)
    
    delta_q = compute_pseudo_inverse(current_q) @ compute_residual(current_q, marker_locations)
    current_q = current_q + delta_q
    
    configurations.append(current_q.copy())


# Animation function
def animate(i):
    plt.gca().cla()  # Clear the current axis

    plt.plot(marker_locations[0], marker_locations[1], 'bo', label='Target Position' if i == 0 else "")
    plt.plot(marker_locations[2], marker_locations[3], 'bo', label='Target Position' if i == 0 else "")
    plt.xlim([-0.5, 0.5])
    plt.ylim([-0.5, 0.5])
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.grid(True)
    plt.title('Progression of the Optimization')

    current_position = forward_kinematics_model(configurations[i])
    plt.plot([0, current_position[0,0]], [0, current_position[1,0]], '-', color=color_1, lw=6)
    plt.plot(current_position[0], current_position[1], 'ro')
    plt.plot(current_position[2], current_position[3], 'ro')
    
fig = plt.figure()
ani = FuncAnimation(fig, animate, frames=len(configurations), repeat=False, interval=500)
plt.legend()
plt.show()
    
