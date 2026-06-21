# CERN Simulations

A set of Python simulations modelling the radiation a high-energy electron beam
produces when it strikes a target, written for a Beamline for Schools proposal
to CERN. The proposal was titled *Testing the Imaging Properties of Synchrotron
Radiation and Bremsstrahlung with a Self-Designed X-Ray Camera*, and these
scripts predict the patterns we expected to measure.

A full write-up of the physics, with the equations and example figures, is on my
website: https://borjadelamora.com/cern-simulations

## What each script does

| Script | Description |
| --- | --- |
| `synchrotron_radiation.py` | Plots the power radiated by an electron as a function of beam energy, for a fixed magnetic field. |
| `bremsstrahlung.py` | Estimates the power emitted per unit frequency when a single electron is deflected by a lead target, integrating over the impact parameter. |
| `xray_camera.py` | Models a Gaussian electron beam passing through the detector stages (target, photocathode, scintillator, phosphor screen) and shows the resulting intensity map. |

The `experiments/` folder holds earlier, rougher scripts kept for reference:
`bremsstrahlung_3d.py`, `deflection.py`, `frequency.py` and `photocathode.py`.

## Running

```bash
pip install -r requirements.txt
python synchrotron_radiation.py
```

Each script is run on its own and opens its plots in a window. `xray_camera.py`
and `bremsstrahlung.py` use Tkinter, which ships with most Python installations.

## Physics references

The bremsstrahlung treatment follows Chapter 7 of the MIT OpenCourseWare notes on
[Electromagnetic Interactions](https://ocw.mit.edu/courses/22-105-electromagnetic-interactions-fall-2005/).

## Licence

Released under the MIT Licence. See [LICENSE](LICENSE).
