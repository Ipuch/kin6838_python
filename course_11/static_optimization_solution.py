#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 01:14:06 2023

@author: puchaud
"""

from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt

# Define the objective function J(F)
def objective_sum(F):
    # Assuming that the objective function is the sum of the muscle forces
    # This could be changed to any other provided function of the forces
    return np.sum(F)

def objective_min_square(F, Fmax):
    # Assuming that the objective function is the sum of the muscle forces
    # This could be changed to any other provided function of the forces
    return np.sum((F/Fmax)**2)

# Constraints as provided in the optimization problem
def constraint_eq(F):
    # This is the constraint that the muscles must produce the desired net ankle moment
    return 0.039*F[0] + 0.036*F[1] + 0.008*F[2] - 100

# Maximal forces of gastrocnemius, soleus, tibial posterior
Fmax = np.array([4097, 6435, 3052])

# The bounds on the muscle forces, based on physiological ranges
bounds = [(0, Fmax[0]), (0, Fmax[1]), (0, Fmax[2])]

# Initial guess for the muscle forces
initial_guess = [.1, 250, .1]

# Define the constraints in a dictionary format for minimize function
cons = [{'type': 'eq', 'fun': constraint_eq}]

# Perform the optimization
objective = objective_sum
# objective = lambda F: objective_min_square(F, Fmax)
result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=cons)

result.x, result.success # Return the optimized muscle forces and the success flag

# Define a range of desired net ankle moments to analyze
ankle_moments = np.linspace(0, 400, 100)  # From 0 to 200 in 100 steps

# Store optimized forces for each desired moment
optimized_forces = np.zeros((len(ankle_moments), 3))

# Update the constraint equation to take into account different moments
def constraint_eq_varying_moment(F, moment):
    return 0.039*F[0] + 0.036*F[1] + 0.008*F[2] - moment

# Loop over the desired ankle moments to solve the optimization problem for each
for i, moment in enumerate(ankle_moments):
    # Update the constraints for the current moment
    cons = [{'type': 'eq', 'fun': constraint_eq_varying_moment, 'args': (moment,)}]
    
    # Solve the optimization problem
    result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=cons)
    
    # Store the optimized forces
    optimized_forces[i, :] = result.x

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(ankle_moments, optimized_forces[:, 0], label='F_GAS')
plt.plot(ankle_moments, optimized_forces[:, 1], label='F_SOL')
plt.plot(ankle_moments, optimized_forces[:, 2], label='F_TP')
plt.xlabel('Desired Net Ankle Moment (Nm)')
plt.ylabel('Muscle Force (N)')
plt.title('Optimized Muscle Forces vs. Ankle Joint Torque')
plt.legend()
plt.grid(True)
plt.show()