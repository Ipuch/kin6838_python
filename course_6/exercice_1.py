import numpy as np
import matplotlib.pyplot as plt

L1 = 0.3
L2 = 0.29

def inverse_kinematics_2d(L1, L2, xm, ym):
        """
        Inverse kinematics with elbow down solution.
        Parameters
        ----------
        l1:
            The length of the arm
        l2:
            The length of the forearm
        xp:
            Coordinate on x of the marker of the knee in the arm's frame
        yp:
            Coordinate on y of the marker of the knee in the arm's frame

        Returns
        -------
        theta:
            The dependent joint
        """

        # q2 = ...
        
        # fill the equation with np.arctan2 (...)
        # to handle all the quadrant of the trigonometric circle
        
        # q1 = ...
        return q1, q2


# Define colors
color_1 = (1, 0.45, 0.1)
color_2 = (0.294118, 0, 0.509804)

# Define the forward kinematics function to visualize the arm's position
def forward_kinematics_2d(q1, q2, L1, L2):
    x1 = L1 * np.cos(q1)
    y1 = L1 * np.sin(q1)
    x2 = x1 + L2 * np.cos(q1 + q2)
    y2 = y1 + L2 * np.sin(q1 + q2)
    return x1, y1, x2, y2


# Set up the initial plot
fig, ax = plt.subplots()
ax.set_xlim(-L1 - L2 - 0.1, L1 + L2 + 0.1)
ax.set_ylim(-L1 - L2 - 0.1, L1 + L2 + 0.1)
ax.set_aspect('equal', 'box')
ax.set_title("Click anywhere to find q1 and q2 of the robot")
ax.grid(True)

# Initial state of the arm
line1, = ax.plot([], [], lw=6, color=color_1, label='Segment 1 - Humerus')
line2, = ax.plot([], [], lw=6, color=color_2, label='Segment 2 - Forearm ')
point, = ax.plot([], [], 'bo', label='Marker')

max_circle = plt.Circle((0, 0), L1 + L2, color='g', fill=False, linestyle='--', label='Max Reach')
ax.add_artist(max_circle)

# Event handler for click event
def onclick(event):
    xm, ym = event.xdata, event.ydata
    q1, q2 = inverse_kinematics_2d(L1, L2, xm, ym)
    
    x1, y1, x2, y2 = forward_kinematics_2d(q1, q2, L1, L2)
    line1.set_data([0, x1], [0, y1])
    line2.set_data([x1, x2], [y1, y2])
    point.set_data(x2, y2)
    ax.set_title("Click anywhere to find q1 and q2 of the robot \n"
                 # f"q1 = {np.round(q1,3)} rad, q2 = {np.round(q2,3)} rad \n"
                 f"q1 = {np.round(np.rad2deg(q1),1)} deg, q2 = {np.round(np.rad2deg(q2),1)} deg \n")
    ax.legend()
    fig.canvas.draw()

# Connect the click event to the event handler
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()