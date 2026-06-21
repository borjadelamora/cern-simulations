import numpy as np
import matplotlib.pyplot as plt

# Generate X-ray energies
x_ray_energies = np.linspace(10, 100, 100)  # X-ray energies in keV

# Constants
area_of_photocathode = 0.01  # Example area in square units (modify as needed)
quantum_efficiency = 0.8    # Example quantum efficiency (modify as needed)

# Calculate the expected photoelectron current using the formula
photoelectron_current = area_of_photocathode * quantum_efficiency / x_ray_energies

# Create a plot
plt.plot(x_ray_energies, photoelectron_current, color='blue', label='Photoelectron Current')

# Add labels and legend
plt.xlabel('Energy of Incident X-rays (keV)')
plt.ylabel('Photoelectron Current')
plt.title('Simulation of Photoelectron Current from Photocathode')
plt.legend()

# Show the plot
plt.show()
