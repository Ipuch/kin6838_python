from sympy import symbols, cos, sin, diff, Matrix

L1 = 0.3

# Define the symbolic variables
q1 = symbols('q1')

# Define the forward kinematics equations
xm = L1 * cos(q1)
ym = L1 * sin(q1)

# Compute the Jacobian matrix
J = Matrix([[diff(xm, q1)],
            [diff(ym, q1)]])

print(J)


