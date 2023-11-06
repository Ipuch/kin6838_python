import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L10 = 0.3
# Let's add another marker on the first segment
L11 = 0.25
# Let's add another marker on a second segment !!
L2 = 0.29  

# Colors for the links
color_1 = (1, 0.45, 0.1)
color_2 = (0.294118, 0, 0.509804)

def forward_kinematics_model(q):
    """Compute the forward kinematics for a given joint configuration."""
    return np.array([
        [L10 * np.cos(q[0,0])], 
        [L10 * np.sin(q[0,0])],
        [L11 * np.cos(q[0,0])], 
        [L11 * np.sin(q[0,0])],
        [L10 * np.cos(q[0,0]) + L2 * np.cos(q[0,0] + q[1,0])], 
        [L10 * np.sin(q[0,0]) + L2 * np.sin(q[0,0] + q[1,0]) ], 
    ])
    
def compute_jacobian(q):
    """Compute the Jacobian for a given joint configuration."""
    return np.array([
        [-L10 * np.sin(q[0,0]), 0 ],
        [L10 * np.cos(q[0,0]), 0 ],
        [-L11 * np.sin(q[0,0]), 0],
        [L11 * np.cos(q[0,0]), 0 ],
        [-L10 * np.sin(q[0,0]) - L2 * np.sin(q[0,0] + q[1,0]), -L2 * np.sin(q[0,0] + q[1,0])],
        [L10 * np.cos(q[0,0]) + L2 * np.cos(q[0,0] + q[1,0]), L2 * np.cos(q[0,0] + q[1,0])]
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
    [0.2],
    [0.15],
    [0.45],
    [0.4]
    ])
initial_guess = np.array([[2.54],[200]])  # q at the initialization of the optimization
convergence_tolerance = 0.001

# Storage for animation
configurations = [initial_guess]

# Nonlinear Least-Square Gauss-Newton Optimization
delta_q = 10  # artificially superior to the tolerance criterion
current_q = initial_guess
loops = 0
while np.linalg.norm(delta_q) > 0.001 and loops < 100:

    loops += 1 
    print("Loop: ", loops)
    
    delta_q = compute_pseudo_inverse(current_q) @ compute_residual(current_q, marker_locations)
    current_q = current_q + delta_q
    
    configurations.append(current_q.copy())


# Animation function
def animate(i):
    ax1.clear()
    ax2.clear()
    
    # Visualization for robot's position
    ax1.plot(marker_locations[0], marker_locations[1], 'bo', label='Target Position' if i == 0 else "")
    ax1.plot(marker_locations[2], marker_locations[3], 'bo', label='Target Position' if i == 0 else "")
    ax1.plot(marker_locations[4], marker_locations[5], 'bo', label='Target Position' if i == 0 else "")
    ax1.axis("equal")
    ax1.set_xlim([-0.7, 0.7])
    ax1.set_ylim([-0.7, 0.7])
    ax1.set_xlabel('X Position')
    ax1.set_ylabel('Y Position')
    ax1.grid(True)
    ax1.set_title('Progression of the Optimization')

    current_position = forward_kinematics_model(configurations[i])
    ax1.plot([0, current_position[0,0]], [0, current_position[1,0]], '-', color=color_1, lw=6)
    ax1.plot([current_position[0,0], current_position[4,0]], [current_position[1,0], current_position[5,0]], '-', color=color_2, lw=6)
    ax1.plot(current_position[0], current_position[1], 'ro')
    ax1.plot(current_position[2], current_position[3], 'ro')
    ax1.plot(current_position[4], current_position[5], 'ro')
    
    # Visualization for the residual
    computed_residuals = [np.linalg.norm(compute_residual(config, marker_locations)) for config in configurations[:i+1]]
    ax2.plot(computed_residuals, 'g-')
    ax2.set_title("Evolution of the Total Residual")
    ax2.set_xlabel('Iterations')
    ax2.set_ylabel('Residual norm')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
ani = FuncAnimation(fig, animate, frames=len(configurations), repeat=False, interval=500)
plt.tight_layout()
plt.show()
    
