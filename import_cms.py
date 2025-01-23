import bpy
import matplotlib.pyplot as plt
import numpy as np
import cmyt

vals = np.mgrid[0.0:1.0:256j]

arr = np.zeros((256, 64, 4), dtype="f4")


for cmap_name in cmyt._utils.cmyt_cmaps:
    if f"cmyt_{cmap_name}" not in bpy.data.images:
        img = bpy.data.images.new(
            f"cmyt_{cmap_name}", 64, 256, alpha=False, float_buffer=True
        )
    else:
        img = bpy.data.images[f"cmyt_{cmap_name}"]
    cmap = plt.cm.ScalarMappable(cmap=plt.get_cmap(f"cmyt.{cmap_name}"))
    cmap.set_clim(0.0, 1.0)
    arr[:] = cmap.to_rgba(vals).astype("f4")[:, None, :]
    img.pixels.foreach_set(arr.ravel(order="C"))
