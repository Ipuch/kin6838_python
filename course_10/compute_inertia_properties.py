"""
(selon Dumas et al.,2007) 
Adjustments to McConville et al. and Young et al. body segment inertial parameters
"""

# Constants and lengths
length_arm = 0.30  # m - Length from shoulder to elbow
length_forearm = 0.35  # m - Length from elbow to wrist
length_hand = 0.10  # m - Length from wrist to middle of metacarpals 2 and 5

# Total mass of the subject
m_tot = 80  # kg - Total mass of the subject

# Mass of the glass and drink, not zero if the arm carry a drink with something in it.
m_glass = 0  # kg - Mass of the glass
m_drink = 0  # kg - Mass of the drink

# Mass calculations based on total mass (according to Dumas et al., 2007)
m_arm = 0.024 * m_tot  # kg
m_forearm = 0.017 * m_tot  # kg
m_hand = 0.006 * m_tot  # kg

# Upper arm specifications
specs = {}
specs['l1'] = length_arm  # m
specs['m1'] = m_arm  # kg
specs['c1'] = specs['l1'] * 0.5502  # m - Position of the center of mass of segment 1
specs['I1'] = (0.33 * length_arm) ** 2 * m_arm  # kg.m2 - Moment of inertia of the arm

# Forearm + hand + glass specifications
I_Forearm = (0.27 * length_forearm) ** 2 * m_forearm  # kg.m2
I_Hand = (0.56 * length_hand) ** 2 * m_hand  # kg.m2

# Glass and drink inertia
Rext_glass = 0.04  # m
Rint_glass = 0.035  # m
I_glass = 0.5 * m_glass * (Rint_glass ** 2 + Rext_glass ** 2)  # kg.m2
I_drink = 0.5 * m_drink * Rint_glass ** 2  # kg.m2

# Forearm + hand + glass + drink specifications
specs['m2'] = m_forearm + m_hand + m_glass
specs['l2'] = length_forearm + length_hand  # m
specs['c2'] = (m_forearm * length_forearm * 0.5726 +
               m_hand * (length_forearm + length_hand * 0.6309) +
               (m_glass + m_drink) * (length_forearm + length_hand * 0.6309)) / (m_forearm + m_hand + m_glass + m_drink)

# Moment of inertia for the forearm + hand + glass + drink
specs['I2'] = (I_Forearm + m_forearm * (specs['c2'] - length_forearm * 0.5726) ** 2 +
               I_Hand + m_hand * (specs['c2'] - (length_forearm + length_hand * 0.6309)) ** 2 +
               I_glass + m_glass * (specs['c2'] - (length_forearm + length_hand * 0.6309)) ** 2 +
               I_drink + m_drink * (specs['c2'] - (length_forearm + length_hand * 0.6309)) ** 2)

print(specs)