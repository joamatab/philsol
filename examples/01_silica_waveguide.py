"""Solve Ex, Ey fields for the fundamental mode of a square silica waveguide.
"""


import numpy as np
import scipy.constants as cst
import matplotlib.pyplot as plt
import philsol as ps


# first we need to build a refractive index profile
points = 60
n = np.ones((points, points, 3))
n[19:39, 19:39, :] = 1.22


# Now we do some scaling so the waveguide guides light at telecom frequecies.
lam = 1.55e-6
k = 2 * cst.pi / lam
neff = 1.04
beta_in = 2 * cst.pi * neff / lam

# we want structure to be scale of wavelength
dx = 1.0e-6 / 20
dy = 1.0e-6 / 20

x = np.array(range(points)) * dx
y = np.array(range(points)) * dy


# plot the index profile
plt.pcolor(x * 1.0e6, y * 1.0e6, n[:, :, 1])


# Assemble finite difference matrices

P, _ = ps.eigen_build(k, n, dx, dy)

beta, Ex, Ey = ps.solve.solve(P, beta_in)

# Recover 2D field profiles from each vector solution
Ex_fields = [np.reshape(E_vec, (points, points)) for E_vec in Ex]
Ey_fields = [np.reshape(E_vec, (points, points)) for E_vec in Ey]

# For each eigenmode, create a real field plot for x-polarised light
for i, E in enumerate(Ey_fields):
    plt.figure(figsize=(8, 4))
    plt.suptitle(f"Effective index: {neff}")

    neff = beta[i] * lam / (2.0 * cst.pi)

    plt.subplot(121, aspect="equal")
    plt.pcolor(x * 1.0e6, y * 1.0e6, np.real(Ex_fields[i]))
    plt.title("E_x")
    plt.xlabel("x (microns)")
    plt.ylabel("y (microns)")

    plt.subplot(122, aspect="equal")
    plt.pcolor(x * 1.0e6, y * 1.0e6, np.real(E))
    plt.title("E_y")
    plt.xlabel("x (microns)")

    plt.show()
