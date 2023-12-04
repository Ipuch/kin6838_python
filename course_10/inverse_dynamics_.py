"""
Most simple inverse_dynamics example

"""
import numpy as np
import matplotlib.pyplot as plt


# model_parameters
m = 1  # kg
lc = 0.5  # meters
g = 9.81  # m/s2 
Izz = 4 * m * lc ** 2 / 3  # kg.m2

# Angles from inverse kineamtics
nb_point = 101
t = np.linspace(0.1, np.pi/2, num=nb_point)
q = np.cos(t) * 2  # angles articulaires (joint angles)

time = np.linspace(start=0, stop=1, num=nb_point)
dt = time[1]

def inverse_dynamics(q, qdot, qddot):
    #
    # 
    # return ...

def first_central_finite_difference(x_i_minus_1, x_i_plus_1, dt):
    # ...
    # return ...


# compute qdot with central finite difference
qdot = np.zeros(nb_point)
# ...  
# compute qddot with central finite difference
qddot = np.zeros(nb_point)
# ...


# inverse dynamics
tau = np.zeros(nb_point)
# ...

# uncomment to see the result
# # Plotting q, qdot, and qddot
# plt.figure(figsize=(12, 8))

# # Plotting q
# plt.subplot(3, 1, 1)
# plt.plot(time, q, label='q (Position)', color='blue')
# plt.title('Position, Velocity, and Acceleration over Time')
# plt.ylabel('Position (rad)')
# plt.grid(True)
# plt.legend()

# # Plotting qdot
# plt.subplot(3, 1, 2)
# plt.plot(time, qdot, label='qdot (Velocity)', color='green')
# plt.ylabel('Velocity (rad/s)')
# plt.grid(True)
# plt.legend()

# # Plotting qddot
# plt.subplot(3, 1, 3)
# plt.plot(time, qddot, label='qddot (Acceleration)', color='red')
# plt.xlabel('Time (s)')
# plt.ylabel('Acceleration (rad/s²)')
# plt.grid(True)
# plt.legend()

# # Emphasizing time discrepancies
# # Note: The first and last values of qdot and qddot are zero due to the finite difference method used for their calculation.
# plt.annotate('Nan due to boundary conditions', 
#              xy=(0, 0), 
#              xytext=(0.1, 0.5), 
#              arrowprops=dict(facecolor='black', shrink=0.05),
#              horizontalalignment='left',
#              verticalalignment='top')

# plt.annotate('Nan due to boundary conditions', 
#              xy=(1, 0), 
#              xytext=(0.9, -0.5), 
#              arrowprops=dict(facecolor='black', shrink=0.05),
#              horizontalalignment='right',
#              verticalalignment='bottom')

# plt.tight_layout()
# plt.show()

# # Plotting the results
# plt.figure(figsize=(10, 6))
# plt.plot(time, tau, label='Torque (Nm)')
# plt.title('Inverse Dynamics over Time')
# plt.xlabel('Time (s)')
# plt.ylabel('Torque (Nm)')
# plt.legend()
# plt.grid(True)
# plt.show()
