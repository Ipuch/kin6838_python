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
        [L1 * np.cos(q[0,0])], 
        [L1 * np.sin(q[0,0])],
    ])
    
def compute_jacobian(q):
    """Compute the Jacobian for a given joint configuration."""
    return np.array([
        [-L1 * np.sin(q[0,0])],
        [L1 * np.cos(q[0,0])]
    ])

def compute_residual(q, m):
    """Compute the residual between the current position and target position."""
    return forward_kinematics_model(q) - m
                    
def compute_pseudo_inverse(q):
    """Compute the pseudo-inverse of the Jacobian."""
    J = compute_jacobian(q)
    return - np.linalg.inv(J.T @ J) @ J.T


marker_location = np.array([[0.4],[0.1]])
initial_guess = np.array([[3]])  # q at the initialization of the optimization
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
    
    delta_q = compute_pseudo_inverse(current_q) @ compute_residual(current_q, marker_location)
    current_q = current_q + delta_q
    
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
ani = FuncAnimation(fig, animate, frames=len(configurations), repeat=True, interval=500)
plt.legend()
plt.show()
    
