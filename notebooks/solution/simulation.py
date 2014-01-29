#!/usr/bin/env python

from pydy_code_gen.code import numeric_right_hand_side
from numpy import array, linspace, deg2rad, ones
from scipy.integrate import odeint

from .equations_of_motion import *

# List the symbolic arguments
# ===========================

# Constants
# ---------

constants = [lower_leg_length,
             lower_leg_com_length,
             lower_leg_mass,
             lower_leg_inertia,
             upper_leg_length,
             upper_leg_com_length,
             upper_leg_mass,
             upper_leg_inertia,
             torso_com_length,
             torso_mass,
             torso_inertia,
             g]

# Time Varying
# ------------

coordinates = [theta1, theta2, theta3]

speeds = [omega1, omega2, omega3]

specified = [ankle_torque, knee_torque, hip_torque]

# Generate RHS Function
# =====================

right_hand_side = numeric_right_hand_side(mass_matrix, forcing_vector,
                                          constants, coordinates, speeds,
                                          specified)

# Specify Numerical Quantities
# ============================

x0 = deg2rad(2.0) * ones(len(coordinates) + len(speeds))

# taken from male1.txt in yeadon (maybe I should use the values in Winters).
numerical_constants = array([0.387,  # lower_leg_length [m]
                             0.611,  # lower_leg_com_length [m]
                             6.769,  # lower_leg_mass [kg]
                             0.101,  # lower_leg_inertia [kg*m^2]
                             0.424,  # upper_leg_length [m]
                             0.193,  # upper_leg_com_length
                             17.01,  # upper_leg_mass [kg]
                             0.282,  # upper_leg_inertia [kg*m^2]
                             0.305,  # torso_com_length [m]
                             32.44,  # torso_mass [kg]
                             1.485,  # torso_inertia [kg*m^2]
                             9.81],  # acceleration due to gravity [m/s^2]
                           )

args = {'constants': numerical_constants,
        'specified': array([0.0, 0.0, 0.0])}

# Simulate
# ========

frames_per_sec = 60

t = linspace(0.0, 10.0, 10 * frames_per_sec)

y = odeint(right_hand_side, x0, t, args=(args,))
