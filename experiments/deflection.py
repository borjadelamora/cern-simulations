import numpy as np
import matplotlib.pyplot as plt

def lorentz_force(q, v, B):
    # Lorentz force equation
    return q * np.cross(v, B)

def simulate_deflection(charge, initial_velocity, magnetic_field, time_step, num_steps):
    angles = np.zeros(num_steps)
    velocities = np.zeros((num_steps, 3))

    velocities[0] = initial_velocity

    for i in range(1, num_steps):
        # Calculate Lorentz force
        force = lorentz_force(charge, velocities[i-1], magnetic_field)

        # Update velocity using F = ma (acceleration = force/mass)
        acceleration = force / charge  # Assuming mass = 1 for simplicity
        velocities[i] = velocities[i-1] + acceleration * time_step

        # Calculate angle of deflection
        angles[i] = np.arctan2(np.linalg.norm(np.cross(initial_velocity, velocities[i])), np.dot(initial_velocity, velocities[i]))

    return angles * (180 / np.pi)  # Convert angles to degrees

# Simulation parameters
charge_positive = 1.0
initial_velocity = np.array([1, 1, 1])
magnetic_field = np.array([0, 0, 1])
time_step = 0.01
num_steps = 1000

# Simulate deflection for positive and negative particles
angles_positive = simulate_deflection(charge_positive, initial_velocity, magnetic_field, time_step, num_steps)
angles_negative = simulate_deflection(-charge_positive, initial_velocity, magnetic_field, time_step, num_steps)

# Plot the angle of deflection
plt.plot(angles_positive, label='Positive Particle')
plt.plot(angles_negative, label='Negative Particle')
plt.xlabel('Time Step')
plt.ylabel('Angle of Deflection (degrees)')
plt.legend()
plt.show()
