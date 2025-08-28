import os
import bpy
import h5py
import numpy as np
import databpy

add_faces = False
add_lines = False
add_bhs = True

frames = []
with h5py.File(os.path.expanduser("~/dxl/gwave/isosurfaces.h5"), "r") as f:
    for i in range(1600):
        frames.append(f[f"/frame_{i:05d}"][:])
    faces = f["/faces"][:]

with h5py.File(os.path.expanduser("~/dxl/gwave/isosurface_values.h5"), "r") as f:
    values = np.log10(f["/values"][:])
    theta = f["/theta"][:]
    phi = f["/phi"][:]

with h5py.File(os.path.expanduser("~/dxl/gwave/blackholes.h5"), "r") as f:
    primary_pos = f["/primary_pos"][:]
    primary_r = f["/primary_r"][:]
    secondary_pos = f["/secondary_pos"][:]
    secondary_r = f["/secondary_r"][:]
    final_pos = f["/final_pos"][:]
    final_r = f["/final_r"][:]

if add_faces:
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

    values_attribute = new_mesh.attributes.new(name="SurfaceValue", type="FLOAT", domain="POINT")
    values_attribute.data.foreach_set("value", values)

    theta_attribute = new_mesh.attributes.new(name="theta", type="FLOAT", domain="POINT")
    theta_attribute.data.foreach_set("value", theta)
    
    phi_attribute = new_mesh.attributes.new(name="phi", type="FLOAT", domain="POINT")
    phi_attribute.data.foreach_set("value", phi)

if add_lines:
    ## Now we add our lines that dance along the surface...

    ## Prime the pump with the first two frames

    stream_mesh = bpy.data.meshes.new('StreamlinesMesh')
    f = np.hstack([frames[0], frames[0]]).ravel().reshape((-1,3))
    stream_mesh.from_pydata(f, np.arange(f.size // 3).reshape((-1, 2)), [])

    stream_obj = bpy.data.objects.new('StreamlineObject', stream_mesh)
    stream_obj.shape_key_add(name="Basis")
    stream_obj.data.shape_keys.use_relative = False

    for f1, f2 in zip(frames[:-1], frames[1:]):
        new_shape_key = stream_obj.shape_key_add(from_mix=False)
        v = np.hstack([f1, f2])
        new_shape_key.points.foreach_set("co", v.flatten())

    bpy.context.scene.collection.objects.link(stream_obj)

    values_attribute = stream_mesh.attributes.new(name="LocalValue", type="FLOAT", domain="POINT")
    values_attribute.data.foreach_set("value", np.hstack([values, values]).ravel())

if add_bhs:
    # We do these differently, because they're single objects.

    bhp = databpy.create_bob(primary_pos, name="Primary Black Hole")
    bhp.store_named_attribute(primary_r, "radius")

    bhs = databpy.create_bob(secondary_pos, name="Secondary Black Hole")
    bhs.store_named_attribute(secondary_r, "radius")

    bhf = databpy.create_bob(final_pos, name="Final Black Hole")
    bhf.store_named_attribute(final_r, "radius")
