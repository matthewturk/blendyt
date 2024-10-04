import bpy
import yt

ds = yt.load_sample("IsolatedGalaxy")

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.wm.read_factory_settings(use_empty=True)

for grid in ds.index.grids[:100]:
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
    cube.keyframe_insert("location", frame=0)
    cube.keyframe_insert("scale", frame=0)
    cube.scale = (grid.RightEdge - grid.LeftEdge).in_units("code_length") * 20
    cube.location = (grid.LeftEdge + grid.RightEdge).in_units("code_length") * 10
    cube.keyframe_insert("scale", frame=30)
    cube.keyframe_insert("location", frame=60)

bpy.ops.wm.save_mainfile(filepath="isolated_galaxy.blend")
