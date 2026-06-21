import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.special import k1
from scipy.constants import c, pi, h, hbar, m_e, e, electron_volt
from scipy.integrate import quad
import tkinter as tk


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
    for i in range(1, num_regions):
        end = b_min + quadratic_factor * i ** DISTRIBUTION_POWER
        regions.append([start, end])
        start = end

    # last region
    regions.append([start, np.inf])

    return regions


def integrand(b, w, v, lorentz_factor):
    energy_per_frequency = ((8 * Z ** 2 * e ** 6) / (
            3 * pi * b ** 2 * m_e ** 2 * c ** 3 * v ** 2)) * ((b * w) / ((lorentz_factor ** 2) * v)) ** 2 * (
                                       (k1((b * w) / ((lorentz_factor ** 2) * v))) ** 2)

    return energy_per_frequency * b


def bremsstrahlung_radiation(energy, v, lorentz_factor):
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


def intensity_energy(root, energy, power_per_frequency):
    fig_xy, ax_xy = plt.subplots(dpi=80)
    ax_xy.set_title('Energy of Beam against Emitted power per unit frequency of the single electron', fontsize=8)
    ax_xy.set_xlabel('Energy of Beam (GeV)')
    ax_xy.set_ylabel('Emitted power per unit frequency of the single electron')
    ax_xy.plot(energy, power_per_frequency)

    # Mark Points
    indices = np.linspace(0, INTERVALS - 1, 7, dtype=int)  # Get 10 evenly spaced indices
    ax_xy.scatter(energy[indices], power_per_frequency[indices], color='red', label='Key Points')

    for i in indices:
        ax_xy.text(energy[i], power_per_frequency[i], f'({energy[i]:.2f}, {power_per_frequency[i] * 1e51:.2f})',
                   fontsize=8, ha='left',
                   va='bottom')
    # Embed the Matplotlib plots in Tkinter window
    canvas_xy = FigureCanvasTkAgg(fig_xy, master=root)
    canvas_xy.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)  # Display on the left
    canvas_xy.draw()


def alternate_graph(root, energy, power_per_frequency, b):
    fig_xy, ax_xy = plt.subplots(dpi=80)
    ax_xy.set_title('Emitted power per unit frequency of the single electron for different b values', fontsize=8)
    ax_xy.set_xlabel('b (Impact Parameter)')
    ax_xy.set_ylabel('Emitted power per unit frequency of the single electron')

    # Plot the x-y graph
    scatter = ax_xy.scatter(b, power_per_frequency, s=10 * energy, c=energy, cmap='viridis', alpha=0.7)
    fig_xy.colorbar(scatter, ax=ax_xy, label='Energy (GeV)')

    # Embed the Matplotlib plots in Tkinter window
    canvas_xy = FigureCanvasTkAgg(fig_xy, master=root)
    canvas_xy.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)  # Display on the left
    canvas_xy.draw()


energy_gev = np.linspace(1, 4, INTERVALS)
energy_j = energy_gev * electron_volt * 10e9


v = c * (1 - ((m_e * c ** 2) / (energy_j + m_e * c ** 2)) ** 2) ** .5
lorentz_factor = 1 / (1 - (v / c) ** 2) ** .5

regions = np.array([])
energies = np.array([])
sliced_power_per_frequency = np.array([])
power_per_frequency = np.zeros_like(energy_gev)

for index, val in enumerate(energy_j):
    region, power_per_frequency_val = bremsstrahlung_radiation(val, v[index], lorentz_factor[index])
    sliced_power_per_frequency = np.concatenate((sliced_power_per_frequency, power_per_frequency_val))
    power_per_frequency[index] = np.sum(power_per_frequency_val)

    regions = np.concatenate((regions, region))
    energies = np.concatenate((energies, np.array([energy_gev[index] for i in range(REGIONS)])))


# Display Graphs
root = tk.Tk()
root.title('Bremsstrahlung Graphs')
intensity_energy(root, energy_gev, power_per_frequency)
alternate_graph(root, energies, sliced_power_per_frequency, regions)
tk.mainloop()
