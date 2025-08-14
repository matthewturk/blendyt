import os
import bpy
import h5py

frames = []

with h5py.File(os.path.expanduser("~/dxl/gwave/isosurfaces.h5"), "r") as f:
    for i in range(1600):
        frames.append(f[f"/frame_{i:05d}"][:])
    faces = f["/faces"][:]

new_mesh = bpy.data.meshes.new('IsosurfaceMesh')
new_mesh.from_pydata(frames[0], [], faces)
new_mesh.update()
surf_obj = bpy.data.objects.new('IsosurfaceObject', new_mesh)

surf_obj.shape_key_add(name="Basis")
surf_obj.data.shape_keys.use_relative = False

for obj in frames[1:]:
    new_shape_key = surf_obj.shape_key_add(from_mix=False)
    new_shape_key.points.foreach_set("co", obj.flatten())

bpy.context.scene.collection.objects.link(surf_obj)
