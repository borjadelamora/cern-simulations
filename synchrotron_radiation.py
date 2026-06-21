import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, pi, h, m_e, e, epsilon_0, electron_volt


# Constants
MAGNETIC_FIELD_STRENGTH = 0.7  # in Tesla
INTERVALS = 200     # Graph Plot Intervals

def synchrotron_radiation(v, lorentz_factor):
    # E = lorentz_factor * m_e * c ** 2
    radius = (m_e * v) / (MAGNETIC_FIELD_STRENGTH * e)
    energy = (3 * h * c * lorentz_factor ** 3) / (2 * radius)

    B = v / c
    power = ((e ** 2 * c) / (6 * pi * epsilon_0)) * (lorentz_factor ** 4) * ((B ** 4) / (radius ** 2))

    return energy, power


def intensity_energy(energy_gev, intensity):
    # Mark Points
    indices = np.linspace(0, INTERVALS - 1, 7, dtype=int)  # Get 10 evenly spaced indices
    plt.scatter(energy_gev[indices], intensity[indices], color='red', label='Key Points')

    for i in indices:
        plt.text(energy_gev[i], intensity[i], f'({energy_gev[i]:.2f}, {intensity[i]:.2f})', fontsize=8, ha='left',
                 va='bottom')

    plt.plot(energy_gev, intensity)
    plt.title('Power of an electron radiated vs Energy of beam')
    plt.xlabel('Energy of Beam (GeV)')
    plt.ylabel('Power of a photon (kW)')
    plt.show()


energy_gev = np.linspace(1, 4, INTERVALS)
energy_j = energy_gev * electron_volt * 10e9

v = c * (1 - ((m_e * c ** 2) / (energy_j + m_e * c ** 2)) ** 2) ** .5
lorentz_factor = 1 / (1 - (v / c) ** 2) ** .5
energy, power = synchrotron_radiation(v, lorentz_factor)
intensity_energy(energy_gev, power * 1e-3)
