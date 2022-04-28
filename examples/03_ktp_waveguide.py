"""Solve Ex, Ey fields for the fundamental mode of a rectangular KTP waveguide.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as cst
from PIL import Image, ImageDraw


def refractive(lam):
    n_square = [
        3.0065 + 0.03901 / (lam ** 2 - 0.04251) - 0.01327 * lam ** 2,
        3.0333 + 0.04154 / (lam ** 2 - 0.04547) - 0.01408 * lam ** 2,
        3.0065 + 0.05694 / (lam ** 2 - 0.05658) - 0.01682 * lam ** 2,
    ]

    return [ns ** 0.5 for ns in n_square]


# We define the size of the simulation window (note there is automatically
# a conductive boundry layer).
simulation_width = 10.0
simulation_height = 9.0

# Number of pixels/fd grid points.
num_x = 81
num_y = 101
dx = simulation_width / float(num_x - 1)
dy = simulation_height / float(num_y - 1)

# Wavelength of end point
lam = 0.3
k = 2 * cst.pi / lam

# We deffine some parameters of the waveguide(refer to the plot if confused!)
air_height = 1.0
WG_height = 6.0
WG_width = 4.0


def n_build(lam):
    # we start with a KTP slab
    n_ax = refractive(lam)
    n_ax = [n_ax[1], n_ax[2], n_ax[0]]
    geom = [Image.new("F", (num_x, num_y), n_ax[i]) for i in range(3)]
    geom_draw = [ImageDraw.Draw(axis) for axis in geom]

    # now we need some air
    air_index = int(round((simulation_height - air_height) / dy))
    [axis.rectangle([0, air_index, num_x - 1, num_y - 1], 1.0) for axis in geom_draw]

    # Now we draw the waveguide with a slightly larger intex
    x0_ind = int(round((simulation_width - WG_width) / (2.0 * dx)))
    x1_ind = int(round((simulation_width + WG_width) / (2.0 * dx)))
    y0_ind = int(round((simulation_height - air_height - WG_height) / dy))
    y1_ind = air_index - 1

    [
        geom_draw[i].rectangle([x0_ind, y0_ind, x1_ind, y1_ind], n_ax[i] + 0.01)
        for i in range(3)
    ]

    return np.dstack(
        [
            np.asarray(axis.getdata(), dtype=np.float64).reshape(
                (num_y, num_x)
            )
            for axis in geom
        ]
    )


x = np.linspace(-simulation_width / 2.0, simulation_width / 2.0, num_x)
y = np.linspace(air_height - simulation_height, air_height, num_y)
n = n_build(lam)

plt.pcolor(x, y, n[:, :, 1])
plt.clim([2.1, 2.2])
# plt.colorbar()
plt.show()
