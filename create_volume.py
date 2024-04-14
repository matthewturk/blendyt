# import bpy
import yt
import pyopenvdb as vdb

# bpy.ops.wm.read_factory_settings(use_empty=True)


# Looks like by default the volume has a left edge at location - scale and a right edge at location + scale.  Scale is with respect to 2?
# bpy.ops.object.volume_add(align="WORLD", location=(0, 0, 0), scale=(1, 1, 1))

# I think it's highly likely that the vertex / cell-centering issue will raise its head.

ds = yt.load_sample("IsolatedGalaxy")

g_vdbs = []
for g in ds.index.grids:
    if g.Level == 0:
        continue
    g_dens = vdb.FloatGrid()
    g_dens.copyFromArray(
        g["density"].in_units("code_density").d,
        ijk=g.get_global_startindex(),
    )
    g_dens.transform = vdb.createLinearTransform(voxelSize=g.dds[0].d)
    g_dens.name = str(g)
    g_vdbs.append(g_dens)

vdb.write("galaxy.vdb", g_vdbs)
