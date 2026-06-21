import numpy as np
import matplotlib.pyplot as plt
from scipy.special import k1
from scipy.constants import c, pi, h, hbar, m_e, e, electron_volt
from scipy.integrate import quad
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D



# Constants
Z = 82  # Atomic number of lead
REGIONS = 100   # Regions during integration
DISTRIBUTION_POWER = 50    # The x^n at which the regions are distributed
INTERVALS = 200     # Graph Plot Intervals


def create_regions(b_min, b_max, num_regions):
    regions = []
    d = b_max - b_min
    quadratic_factor = d / (num_regions ** DISTRIBUTION_POWER)
    start = b_min
    for i in range(1, num_regions + 1):
        end = b_min + quadratic_factor * i ** DISTRIBUTION_POWER
        regions.append([start, end])
        start = end

    # last region
    # regions.append([start, np.inf])
    return regions


def integrand(b, w, v, lorentz_factor):
    energy_per_frequency = ((8 * Z ** 2 * e ** 6) / (
                3 * pi * b ** 2 * m_e ** 2 * c ** 3 * v ** 2)) * ((b * w) / ((lorentz_factor ** 2) * v)) ** 2 * ((k1((b * w) / ((lorentz_factor ** 2) * v))) ** 2)
    return energy_per_frequency * b


def relation():
    b = np.linspace(1e-11, 1e-9, 1000)  # x axis
    E = np.linspace(1.602e-10, 1.602e-10 * 4, 1000)
    frequency = E / h
    w = 2 * pi * frequency
    z = integrand(b, w)    # dW/dw

    # Create a figure and a 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot a 3D line
    ax.plot(b, E, z)

    # Set labels and title
    ax.set_xlabel("Impact Parameter")
    ax.set_ylabel("Energy")
    ax.set_zlabel("dW/dw")
    ax.set_title('3D Line Plot')

    # Show plot
    plt.show()


def bremsstrahlung_radiation(energy, v, lorentz_factor):
    n_pb = 2.89e30
    frequency = energy / h
    w = 2 * pi * frequency
    b_min = hbar / (m_e * v)
    b_max = (2 * v ** 2) / (w * m_e)  # approximation

    regions = create_regions(b_min, b_max, REGIONS)

    integral = 0
    for i in regions:
        val = quad(integrand, i[0], i[1], args=(w, v, lorentz_factor), epsabs=1.49e-8, epsrel=1.49e-8)[0]
        integral += val

    power_per_frequency = 2 * pi * c * n_pb * integral

    return power_per_frequency


def intensity_energy(energy, power):
    # Mark Points
    indices = np.linspace(0, INTERVALS - 1, 7, dtype=int)  # Get 10 evenly spaced indices
    plt.scatter(energy[indices], power[indices], color='red', label='Key Points')

    for i in indices:
        plt.text(energy[i], power[i], f'({energy[i]:.2f}, {power[i] * 1e51:.2f})', fontsize=8, ha='left',
                 va='bottom')

    plt.plot(energy, power)
    plt.xlabel("Energy of Beam (GeV)")
    plt.ylabel("Emitted power per unit frequency of the single electron")
    plt.show()



def alternate_calc(energy, v, lorentz_factor):
    n_pb = 2.89e30
    frequency = energy / h
    w = 2 * pi * frequency
    b_min = hbar / (m_e * v)
    b_max = (2 * v ** 2) / (w * m_e)  # approximation

    regions = create_regions(b_min, b_max, REGIONS)
    regions_median = []
    power_per_frequency = []

    for i in regions:
        regions_median.append((i[0] + i[1]) / 2)
        integral = quad(integrand, i[0], i[1], args=(w, v, lorentz_factor), epsabs=1.49e-8, epsrel=1.49e-8)[0]
        power_per_frequency.append(2 * pi * c * n_pb * integral)

    return regions_median, power_per_frequency


def alternate_graph(energy, power, b):
    # Convert lists to numpy arrays
    b = np.array(b)
    power = np.array(power)
    energy = np.array(energy)

    # Create scatter plot
    plt.figure()

    # Plot the surface
    plt.scatter(b, power, s=10 * energy, c=energy, cmap='viridis', alpha=0.7)
    # Add colorbar
    plt.colorbar(label='Energy (GeV)')




    # Set labels and title
    plt.ylabel("Emitted power per unit frequency of the single electron")
    plt.xlabel("b")
    plt.title('Emitted power per unit frequency of the single electron for different b values', fontsize=10)

    plt.show()


energy_gev = np.linspace(1, 4, INTERVALS)
energy_j = energy_gev * electron_volt * 10e9


v = c * (1 - ((m_e * c ** 2) / (energy_j + m_e * c ** 2)) ** 2) ** .5
lorentz_factor = 1 / (1 - (v / c) ** 2) ** .5

powers = []
regions = []
energies = []

for index, val in enumerate(energy_j):
    region, power = alternate_calc(val, v[index], lorentz_factor[index])
    powers.extend(power)
    regions.extend(region)
    for i in range(REGIONS):
        energies.append(energy_gev[index])


alternate_graph(energies, powers, regions)
