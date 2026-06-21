import numpy as np
import matplotlib.pyplot as plt

# Constants
Z = 82  # Atomic number of the lead nucleus
ELEMENTARY_CHARGE = 1.602176634e-19  # Elementary charge in C
ELECTRON_MASS = 9.10938356e-31  # Electron mass in kg
SPEED_OF_LIGHT = 299792458  # Speed of light in m/s
NUM_ELECTRONS = 1e6
TARGET_DENSITY = 7.87  # g/cm^3, density of the material
ATOMIC_MASS = 55.845  # g/mol, atomic mass of the material
RADIATION_LENGTH = 1  # in cm, radiation length of the material
FINE_STRUCTURE_CONSTANT = 7.2973525693e-3  # Fine-structure constant
CLASSICAL_ELECTRON_RADIUS = 2.8179403227e-13  # cm, classical electron radius
INITIAL_VELOCITY = 2e7  # make sure this is correct


# Function to calculate bremsstrahlung intensity for a given beam energy
def bremsstrahlung_intensity(energy):
    intensity = Z**2 * ELEMENTARY_CHARGE**6 * (1 / (ATOMIC_MASS * SPEED_OF_LIGHT ** 2)) * (NUM_ELECTRONS / energy)
    initial_ke = .5 * ELECTRON_MASS * INITIAL_VELOCITY ** 2
    final_ke = 100
    energy_max = (4 * initial_ke * final_ke) / (ELECTRON_MASS * SPEED_OF_LIGHT ** 2)
    K, sigma = 0, 0 # Constants specific to the beam
    characteristic_energy = (K * (Z - sigma)) ** 2
    return intensity

# Function to calculate Bremsstrahlung intensity for a range of beam energies

# Function to plot the Bremsstrahlung intensity versus beam energy
def plot_intensity_vs_energy(beam_energy_range, intensities):
    plt.plot(beam_energy_range, intensities)
    plt.title('Bremsstrahlung Intensity vs Beam Energy')
    plt.xlabel('Beam Energy (eV)')
    plt.ylabel('Intensity')
    plt.grid()
    plt.show()

# Define the range of beam energies
beam_energy_range = np.linspace(1e-15, 1e-14, 100)  # eV
# Calculate Bremsstrahlung intensity for the range of beam energies
intensities = bremsstrahlung_intensity(beam_energy_range)

print(intensities)

# Plot Bremsstrahlung intensity versus beam energy
plot_intensity_vs_energy(beam_energy_range, intensities)
