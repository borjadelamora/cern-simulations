import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import LogNorm
import matplotlib.ticker as ticker
import tkinter as tk

# Constants
BEAM_DIAMETER = 0.02  # Diameter of the electron beam (m)
INTERVAL = 100  # Interval of graph plot
METAL_DENSITY_FACTOR = 1.0  # Fixed Metal density

# Unknown values
METAL_THICKNESS = 0.01  # in meters
PHOTON_ATTENUATION_FACTOR = 0.01  # Fraction of X-rays passing through metal plate
PHOTO_CATHODE_EFFICIENCY = 0.9  # Efficiency of the photo-cathode
THRESHOLD_INTENSITY = 0.01  # Threshold for photo-electron emission
SCINTILLATOR_EFFICIENCY = 0.8  # Efficiency of the scintillator
PHOSPHOR_SCREEN_EFFICIENCY = 0.7  # Efficiency of the phosphor screen


def xray_attenuation(thickness, density_factor):
    return np.exp(-thickness * density_factor * PHOTON_ATTENUATION_FACTOR)


def calculate_photo_cathode_efficiency(xray_intensity):
    return np.where(xray_intensity > THRESHOLD_INTENSITY, xray_intensity * PHOTO_CATHODE_EFFICIENCY, 0.0)


def calculate_scintillator_efficiency(photoelectrons):
    return photoelectrons * SCINTILLATOR_EFFICIENCY


def calculate_phosphor_screen_efficiency(uv_photons):
    return uv_photons * PHOSPHOR_SCREEN_EFFICIENCY


def gaussian_beam(x, y):
    return np.exp(-(x**2 + y**2) / (2 * (BEAM_DIAMETER / 2)**2))


def create_tkinter_window(detected_intensity_map, positions_x):
    root = tk.Tk()
    root.title('Simulated Images')

    fig_xy, ax_xy = plt.subplots(dpi=60)
    ax_xy.set_title('Detected Intensity Map')
    ax_xy.set_xlabel('X Position (m)')
    ax_xy.set_ylabel('Y Position (m)')

    ax_xy.xaxis.set_major_locator(ticker.MultipleLocator(0.005))
    ax_xy.yaxis.set_major_locator(ticker.MultipleLocator(0.005))

    im_xy = ax_xy.imshow(detected_intensity_map, cmap='viridis', extent=[0, BEAM_DIAMETER, 0, BEAM_DIAMETER],
                         norm=LogNorm(), origin='lower')
    fig_xy.colorbar(im_xy, ax=ax_xy, label='Detected Intensity')

    fig_intensity, ax_intensity = plt.subplots(dpi=60)
    ax_intensity.set_title('Intensity vs. Position')
    ax_intensity.set_xlabel('Position')
    ax_intensity.set_ylabel('Detected Intensity')

    intensity_profile = np.sum(detected_intensity_map, axis=0)  # Sum along the y-axis
    ax_intensity.plot(positions_x, intensity_profile, label='Intensity Profile', color='blue')

    canvas_xy = FigureCanvasTkAgg(fig_xy, master=root)
    canvas_xy.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)  # Display on the left
    canvas_xy.draw()

    canvas_intensity = FigureCanvasTkAgg(fig_intensity, master=root)
    canvas_intensity.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)  # Display on the right
    canvas_intensity.draw()

    tk.mainloop()


def simulate_image():
    positions_x = np.linspace(0, BEAM_DIAMETER, INTERVAL)
    positions_y = np.linspace(0, BEAM_DIAMETER, INTERVAL)
    x, y = np.meshgrid(positions_x, positions_y)

    detected_intensity_map = np.zeros((INTERVAL, INTERVAL))
    beam_distribution = gaussian_beam(x - BEAM_DIAMETER / 2, y - BEAM_DIAMETER / 2)

    for i, pos_x in enumerate(positions_x):
        for j, pos_y in enumerate(positions_y):
            beam_intensity = beam_distribution[i, j]
            transmitted_intensity = beam_intensity * xray_attenuation(METAL_THICKNESS, METAL_DENSITY_FACTOR)
            photo_cathode_efficiency = calculate_photo_cathode_efficiency(transmitted_intensity)
            photoelectrons = transmitted_intensity * photo_cathode_efficiency
            uv_photons = calculate_scintillator_efficiency(photoelectrons)
            visible_light = calculate_phosphor_screen_efficiency(uv_photons)
            detected_intensity = calculate_photo_cathode_efficiency(visible_light)
            detected_intensity_map[i, j] = detected_intensity

    return detected_intensity_map, positions_x


# Display Graphs
detected_intensity_map, positions_x = simulate_image()
create_tkinter_window(detected_intensity_map, positions_x)
