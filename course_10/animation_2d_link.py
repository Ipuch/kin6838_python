import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def forward_kinematics_model(l1, l2, q):
    """Compute the forward kinematics for a given joint configuration."""
    x1 = l1 * np.cos(q[0])
    y1 = l1 * np.sin(q[0])
    x2 = x1 + l2 * np.cos(q[0] + q[1])
    y2 = y1 + l2 * np.sin(q[0] + q[1])
    return x1, y1, x2, y2

def animate2d_link(l1, l2, q):
    # Colors for the links
    color_1 = (1, 0.45, 0.1)
    color_2 = (0.294118, 0, 0.509804)

    # Animation function
    def animate(i):
        ax.clear()
        
        x1, y1, x2, y2 = forward_kinematics_model(l1, l2, q[:, i])
        ax.plot([0, x1], [0, y1], '-', color=color_1, lw=6)
        ax.plot([x1, x2], [y1, y2], '-', color=color_2, lw=6)
        ax.plot(x1, y1, 'ro')
        ax.plot(x2, y2, 'ro')

        ax.set_xlim([-l1-l2, l1+l2])
        ax.set_ylim([-l1-l2, l1+l2])
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.grid(True)
        ax.set_title('2D Link Animation')

    fig, ax = plt.subplots(figsize=(8, 8))
    ani = FuncAnimation(fig, animate, frames=q.shape[1], repeat=True, interval=10)

    # Return the animation object
    return ani

# Example usage
l1 = 0.3
l2 = 0.29
q = np.linspace([0, 0], [np.pi/2, np.pi/3], 100).T  # Generate a range of joint angles

# Store the animation object in a variable
anim = animate2d_link(l1, l2, q)
plt.show()  # Display the animation