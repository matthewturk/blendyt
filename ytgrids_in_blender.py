import databpy
import bpy
import numpy as np
import yt

ds = yt.load_sample("IsolatedGalaxy")

LE = ds.index.grid_left_edge
RE = ds.index.grid_right_edge
grid_centers = ((LE + RE) / 2.0).in_units("unitary").d
grid_half_widths = (RE - LE).in_units("unitary").d

if "Grid Hierarchy" in bpy.data.objects:
    obj = databpy.BlenderObject(bpy.data.objects["Grid Hierarchy"])
else:
    obj = databpy.create_bob(grid_centers, name="Grid Hierarchy")

obj.store_named_attribute(name="grid_width", data=grid_half_widths)

obj.store_named_attribute(name="grid_level", data=ds.index.grid_levels)


if "slice" not in bpy.data.images:
    img = bpy.data.imges.new("slice", 512, 512, alpha=False, float_buffer=True)
else:
    img = bpy.data.images["slice"]

s = ds.r[:, :, 0.5].to_frb((1.0, "unitary"), (512, 512))

r = np.log10(s["density"].d)
g = s["temperature"].d
b = np.log10(s["velocity_magnitude"].d)

ytimg = np.zeros((512, 512, 4), dtype="f4")
ytimg[:, :, 0] = (r - r.min()) / (r.max() - r.min())
ytimg[:, :, 1] = (g - g.min()) / (g.max() - g.min())
ytimg[:, :, 2] = (b - b.min()) / (b.max() - b.min())

img.pixels.foreach_set(ytimg.ravel(order="C"))
