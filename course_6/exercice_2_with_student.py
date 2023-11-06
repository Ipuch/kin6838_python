import numpy as np
import matplotlib.pyplot as plt

# Define the given points
pt1 = [0.5, 1]
pt2 = [0.1, 0.9]
pt3 = [1.5, 1.2]

# Build the equation in matrix form
# The equation is represented as Ax = b
# where A is the matrix of x-coordinates and ones (for the constant term),
# x are the coefficients we want to find (for the line equation y = mx + c),
A = np.array([[pt1[0], 1],
              [pt2[0], 1],
              [pt3[0], 1]])

# b is the y-coordinates of the given points.
b =  np.array([pt1[1], pt2[1], pt3[1]])

# Calculate the pseudo-inverse of A
# This helps us find a solution even if A is not a square matrix
pseudo_inverse_A = np.linalg.inv(A.T @ A) @ A.T

# Compute x the coefficient of the affine transform  y = ax + b
coefficients = pseudo_inverse_A @ b

# Visualize the given points and the resulting line
x_values = np.linspace(min(pt1[0], pt2[0], pt3[0]) - 0.5, max(pt1[0], pt2[0], pt3[0]) + 0.5, 400)
y_values = coefficients[0] * x_values + coefficients[1]
plt.plot(x_values, y_values, color='blue', label=f'y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}')
plt.scatter([pt1[0], pt2[0], pt3[0]],
            [coefficients[0] * pt1[0] + coefficients[1],
             coefficients[0] *  pt2[0] + coefficients[1],
             coefficients[0] *  pt3[0] + coefficients[1],
             ], 
            color='blue', label='Model Points')
plt.scatter([pt1[0], pt2[0], pt3[0]], [pt1[1], pt2[1], pt3[1]], color='red', label='Given Points')
plt.legend()
plt.title('Affine Transformation Using Pseudo-Inverse')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()

print(f"Coefficients (a, b) of the affine transformation y = ax + b are: {coefficients}")
