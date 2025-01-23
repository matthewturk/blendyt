import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs
import nodetree_script.api.dynamic.shader as ss
import numpy as np
import bpy
import csv_importer.csv
import glob
import os
import healpy as hp
import matplotlib.pyplot as plt
from scipy.special import sph_harm

# Create new array

width = 1024
height = 640

if "Example Image" not in bpy.data.images:
    img = bpy.data.images.new(
        "Example Image", height, width, alpha=False, float_buffer=True
    )
else:
    img = bpy.data.images["Example Image"]

arr = np.zeros((width, height, 4), dtype="f4")

x, y = np.mgrid[0.0 : 1.0 : width * 1j, 0.0 : 1.0 : height * 1j]


arr[:, :, 0] = x
arr[:, :, 1] = 0.0
arr[:, :, 2] = y
arr[:, :, 3] = 1.0

img.pixels.foreach_set(arr.ravel(order="C"))

# https://scipython.com/blog/visualizing-the-real-forms-of-the-spherical-harmonics/
width = 1024
height = 1024

if "Spherical Harmonics" not in bpy.data.images:
    img = bpy.data.images.new(
        "Spherical Harmonics", height, width, alpha=False, float_buffer=True
    )
else:
    img = bpy.data.images["Spherical Harmonics"]

theta, phi = np.mgrid[0 : np.pi : height * 1j, 0 : 2 * np.pi : width * 1j]

l = 3
m = 1

vals = sph_harm(abs(m), l, phi, theta).real

arr = np.zeros((width, height, 4), dtype="f4")
cmap = plt.cm.ScalarMappable(cmap=plt.get_cmap("viridis"))
cmap.set_clim(-0.5, 0.5)

color_vals = cmap.to_rgba(vals)
arr[:] = color_vals

img.pixels.foreach_set(arr.ravel(order="C"))
