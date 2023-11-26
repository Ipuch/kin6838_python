"""
Most simple inverse_dynamics example

"""
import numpy as np
import matplotlib.pyplot as plt
from animation_2d_link import animate2d_link

# from Dumas et al. 2007 for a male see script
m1 = 1.92
m2 = 1.84
l1 = 0.3
l2 = 0.44999999999999996
lc1 = 0.16506
lc2 = 0.2558917391304347
I1 = 0.018817920000000002
I2 = 0.44999999999999996

# model_parameters
m = 1  # kg
lc = 0.5  # meters
g = 9.81  # m/s2 
I = 4 * m * lc ** 2 / 3  # kg.m2

# Angles
nb_point = 101
t = np.linspace(0.1, np.pi/2, num=nb_point)

# writing some random joint angles
q1 = np.cos(t) * 2
q2 = np.cos(t*2) + 1
q = np.vstack([q1, q2])

# visualisation
# animate2d_link(l1,l2, q)
# plt.show()  # Display the motion

time = np.linspace(start=0, stop=1, num=nb_point)
dt = time[1]

def inverse_dynamics(q, qdot, qddot):
    tau_1 = ((I1 + m1 * lc1**2 + m2 * (l1**2 + lc2**2 + 2 * l1 * lc2 * np.cos(q[1]))) * qddot[0]
             + (I2 + m2 * lc2**2 + m2 * l1 * lc2 * np.cos(q[1])) * qddot[1]
             - m2 * l1 * lc2 * np.sin(q[1]) * qdot[1]**2
             - 2 * m2 * l1 * lc2 * np.sin(q[1]) * qdot[0] * qdot[1]
             + m1 * g * lc1 * np.cos(q[0])
             + m2 * g * (l1 * np.cos(q[0]) + lc2 * np.cos(q[0] + q[1])))
    
    tau_2 = ((I2 + m2 * lc2**2) * qddot[1]
             + (I2 + m2 * l1 * lc2 * np.cos(q[1])) * qddot[0]
             + m2 * l1 * lc2 * np.sin(q[1]) * qdot[0]**2
             + m2 * g * lc2 * np.cos(q[0] + q[1]))

    return np.hstack([tau_1, tau_2])

def first_central_finite_difference(x_i_minus_1, x_i_plus_1, dt):
    return (x_i_plus_1 - x_i_minus_1)/ (2 * dt)


# compute qdot with central finite difference
qdot = np.zeros((2, nb_point))
for i in range(1, nb_point-1):
    qdot[:, i] = first_central_finite_difference(q[:,i-1], q[:,i+1], dt=dt)
    
# compute qddot with central finite difference
qddot =  np.zeros((2, nb_point))
for i in range(2, nb_point-2):
    qddot[:, i] = first_central_finite_difference(qdot[:,i-1], qdot[:,i+1], dt=dt)

# inverse dynamics
tau =  np.zeros((2, nb_point))
tau[:, 0:2] = np.nan
tau[:, -2:-1] = np.nan
for i in range(2, nb_point-2):
    tau[:, i] = inverse_dynamics(q[:,i], qdot[:,i], qddot[:,i])


# Plotting q, qdot, qddot, and tau
plt.figure(figsize=(12, 18))

# Plotting q
plt.subplot(4, 1, 1)
plt.plot(time, q[0, :], label='q1 (Position)', color='blue')
plt.plot(time, q[1, :], label='q2 (Position)', color='cyan')
plt.title('Position, Velocity, Acceleration, and Torque over Time')
plt.ylabel('Position (rad)')
plt.grid(True)
plt.legend()

# Plotting qdot
plt.subplot(4, 1, 2)
plt.plot(time, qdot[0, :], label='qdot1 (Velocity)', color='green')
plt.plot(time, qdot[1, :], label='qdot2 (Velocity)', color='olive')
plt.ylabel('Velocity (rad/s)')
plt.grid(True)
plt.legend()

# Plotting qddot
plt.subplot(4, 1, 3)
plt.plot(time, qddot[0, :], label='qddot1 (Acceleration)', color='red')
plt.plot(time, qddot[1, :], label='qddot2 (Acceleration)', color='maroon')
plt.ylabel('Acceleration (rad/s²)')
plt.grid(True)
plt.legend()

# Plotting torque
plt.subplot(4, 1, 4)
plt.plot(time, tau[0, :], label='tau1 (Torque)', color='blue')
plt.plot(time, tau[1, :], label='tau2 (Torque)', color='cyan')
plt.xlabel('Time (s)')
plt.ylabel('Torque (Nm)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
