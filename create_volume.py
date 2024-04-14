# import bpy
import yt
import pyopenvdb as vdb

# bpy.ops.wm.read_factory_settings(use_empty=True)


# Looks like by default the volume has a left edge at location - scale and a right edge at location + scale.  Scale is with respect to 2?
# bpy.ops.object.volume_add(align="WORLD", location=(0, 0, 0), scale=(1, 1, 1))

# I think it's highly likely that the vertex / cell-centering issue will raise its head.

ds = yt.load_sample("IsolatedGalaxy")

g_vdbs = {_: vdb.FloatGrid() for _ in range(ds.index.max_level + 1)}
for i in g_vdbs:
    g_vdbs[i].name = f"Level {i}"
    g_vdbs[i].transform = vdb.createLinearTransform(
        voxelSize=ds.index.select_grids(i)[0].dds[0].d
    )

for g in ds.index.grids:
    g_dens = g_vdbs[g.Level]
    g_dens.copyFromArray(
        g["density"].in_units("code_density").d * g.child_mask,
        ijk=g.get_global_startindex(),
    )
    # print(g_dens.activeVoxelCount(), g.child_mask.sum())

vdb.write("galaxy.vdb", list(g_vdbs.values()))
