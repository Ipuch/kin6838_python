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
    # ...

def objective_min_square(F, Fmax):
    # Assuming that the objective function is the sum of the muscle forces
    # This could be changed to any other provided function of the forces
    # ...

# Constraints as provided in the optimization problem
def constraint_eq(F):
    # This is the constraint that the muscles must produce the desired net ankle moment
    # ...

# Maximal forces of gastrocnemius, soleus, tibial posterior
Fmax = np.array([4097, 6435, 3052])

# The bounds on the muscle forces, based on physiological ranges
# bounds = [(min, max), (min, max), ...]
# bounds = ...

# Initial guess for the muscle forces
# initial_guess = ...

# Define the constraints in a dictionary format for minimize function
cons = [{'type': 'eq', 'fun': constraint_eq}]

# Perform the optimization
objective = objective_sum
# objective = lambda F: objective_min_square(F, Fmax)
result = minimize(objective, 
                  initial_guess, 
                  method='SLSQP', 
                  bounds=bounds, 
                  constraints=cons,
                  )

result.x, result.success # Return the optimized muscle forces and the success flag

# Define a range of desired net ankle moments to analyze
ankle_moments = np.linspace(0, 400, 100)  # From 0 to 200 in 100 steps
# solve it for torques from 0 to 400 N...