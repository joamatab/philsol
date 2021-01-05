"""Solve Ex, Ey fields for the fundamental mode of a rectangular silicon waveguide.
"""

import numpy as np
import matplotlib.pyplot as plt
import philsol as ps


# first we need to build a refractive index profile
n_background = 1.44
n_core = 3.45
xmargin = 2e-6
ymargin = 2e-6
wg_width = 0.5e-6
wg_thickness = 0.22e-6
dx = 10e-9
dy = 10e-9
nx = int((wg_width + 2 * xmargin) / dx)
ny = int((wg_thickness + 2 * ymargin) / dy)

x = np.array(range(nx)) * dx
y = np.array(range(ny)) * dy
n = np.ones((nx, ny, 3)) * n_background
n[
    nx // 2 - int(wg_width / dx / 2) : nx // 2 + int(wg_width / dx / 2),
    ny // 2 - int(wg_thickness / dy / 2) : ny // 2 + int(wg_thickness / dy / 2),
    :,
] = n_core


# Now we do some scaling so the waveguide guides light at telecom frequecies.
wl = 1.55e-6
k = 2 * np.pi / wl
neff = 2.45
beta_in = 2 * np.pi * neff / wl


# plot the index profile
plt.pcolor(x * 1e6, y * 1e6, n[:, :, 1].T)
plt.colorbar()
# plt.show()


# Assemble finite difference matrices
P, _ = ps.eigen_build(k, n, dx, dy)
beta, Ex, Ey = ps.solve.solve(P, beta_in)

# Recover 2D field profiles from each vector solution
Ex_fields = [np.reshape(E_vec, (nx, ny)) for E_vec in Ex]
Ey_fields = [np.reshape(E_vec, (nx, ny)) for E_vec in Ey]

# For each eigenmode, create a real field plot for x-polarised light
for i, E in enumerate(Ey_fields):
    plt.figure(figsize=(8, 4))
    plt.suptitle(f"Effective index: {neff}")

    neff = beta[i] * wl / (2.0 * np.pi)
    plt.subplot(121, aspect="equal")
    plt.pcolor(x * 1.0e6, y * 1.0e6, np.real(Ex_fields[i].T))
    plt.title("E_x")
    plt.xlabel("x (microns)")
    plt.ylabel("y (microns)")

    plt.subplot(122, aspect="equal")
    plt.pcolor(x * 1.0e6, y * 1.0e6, np.real(E.T))
    plt.title("E_y")
    plt.xlabel("x (microns)")

    plt.show()
