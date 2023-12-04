import numpy as np
import matplotlib.pyplot as plt

# Define the equations as a function
def muscle_dynamics(a, u):
    """
    Muscle dynamics equations to be integrated
    a: activation
    u: excitation
    """
    # Activation and deactivation constants
    tau_a = 0.01
    tau_d = 0.04 
    
    # The given image is not clearly readable, using placeholder dynamics
    if u > a:
        dadt = (u - a) / (tau_a * (0.5 + 1.5 * a))
    else:
        dadt = (u - a) / (tau_d / (0.5 + 1.5 * a))

    return dadt

# Control input function
def u(t):
    # u(t) equal to one over 250 ms and then 0
    return 1 if t <= 0.250 else 0

# Time parameters for integration
t_start = 0
t_end = 1  # Assume 1 second for demonstration
dt = 0.001  # Time step for Forward Euler integration

# Initialize state variables
a_0 = 0.0  # Assuming initial activation is zero

# Time vector
time = np.arange(t_start, t_end, dt)

# To store the results
activations = []
excitations = []

# Forward Euler integration
for t in time:
    # Store the current activation
    activations.append(a_0)
    # Compute the state derivatives
    excitation = u(t)
    excitations.append(excitation)
    
    adot = muscle_dynamics(a_0, excitation)
    # Update the state: Forward Euler integration step
    a_0 += adot * dt

# Plotting the results
plt.plot(time, activations, label="activation")
plt.plot(time, excitations, label="excitation", linestyle='--')
plt.xlabel('Time (s)')
plt.ylabel('Activation/Excitation')
plt.title('Muscle Activation and Excitation Over Time')
plt.legend()
plt.grid(True)
plt.show()