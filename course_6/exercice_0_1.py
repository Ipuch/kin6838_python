import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Lengths of the links  - MODIFY THE SIZE OF THE LINKS
L1 = 0.30
L2 = 0.29

# Colors for the links
color_1 = (1, 0.45, 0.1)
color_2 = (0.294118, 0, 0.509804)

# Define the forward kinematics model
def forward_kinematics_model(q1, q2):
    # position of O1
    x1 = L1 * np.cos(q1)
    y1 = L1 * np.sin(q1)
    # position of M
    # EQUATION OF THE FORWARD KINEMATICS MODEL HERE
    # x2 = ...
    # y2 = ...
    
    return x1, y1, x2, y2

# Create a plotting function
def setup_plot():
    fig, axs = plt.subplots(1, 2, figsize=(16, 8))
    
    # Setup for the arm animation plot
    axs[0].set_xlim(-L1 - L2 - 0.1, L1 + L2 + 0.1)
    axs[0].set_ylim(-L1 - L2 - 0.1, L1 + L2 + 0.1)
    axs[0].set_aspect('equal', 'box')
    axs[0].grid(True)
    axs[0].set_title("Upper Arm Animation")
    
    # Setup for the time series plot
    axs[1].set_xlim(0, 360)  # Assuming 360 frames for the animation
    axs[1].set_ylim(-L1 - L2 - 0.1, L1 + L2 + 0.1)
    axs[1].set_xlabel('Time (frames)')
    axs[1].set_ylabel('Coordinates')
    axs[1].grid(True)
    axs[1].set_title("Marker (x, y) Over Time")
    
    return fig, axs

# Initialize the figure and axis for plotting
fig, axs = setup_plot()

# Plot the initial state of the arm on the first axis
line1, = axs[0].plot([], [], lw=6, color=color_1, label='Segment 1 - Humerus')
line2, = axs[0].plot([], [], lw=6, color=color_2, label='Segment 2 - Forearm')
point, = axs[0].plot([], [], 'bo', label='Marker')

# Plot for the time series on the second axis
line_x, = axs[1].plot([], [], 'b-', label='x-coordinate')
line_y, = axs[1].plot([], [], 'r-', label='y-coordinate')
time_data, x_data, y_data = [], [], []

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    point.set_data([], [])
    return line1, line2, point

def animate(i):
    q1 = np.deg2rad(i % 360)  # Joint angle q1 rotates 360 degrees
    q2 = np.deg2rad(45)      # Fixed joint angle q2 for simplicity
    
    x1, y1, x2, y2 = forward_kinematics_model(q1, q2)
    
    line1.set_data([0, x1], [0, y1])
    line2.set_data([x1, x2], [y1, y2])
    point.set_data(x2, y2)
    
    # Append data for the time series
    time_data.append(i)
    x_data.append(x2)
    y_data.append(y2)
    
    line_x.set_data(time_data, x_data)
    line_y.set_data(time_data, y_data)
    
    return line1, line2, point, line_x, line_y

ani = FuncAnimation(fig, animate, frames=360, init_func=init, blit=True, repeat=True)
axs[0].legend()
axs[1].legend()
plt.tight_layout()
plt.show()