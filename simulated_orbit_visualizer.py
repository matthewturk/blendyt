import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs
import nodetree_script.api.dynamic.shader as ss
import numpy as np
import bpy
import csv_importer.csv
import glob
import os


class GridSpecification(ns.InputGroup):
    left_edge: ns.Vector
    right_edge: ns.Vector
    nx: ns.Int
    ny: ns.Int
    nz: ns.Int


@ns.tree("Positions from CSV")
def positions_from_csv(geometry: ns.Geometry, animation_scale: ns.Float):
    x = gs.named_attribute(name="x").attribute
    y = gs.named_attribute(name="y").attribute
    z = gs.named_attribute(name="z").attribute
    pos = gs.combine_xyz(x=x, y=y, z=z)
    points = gs.set_position(geometry=gs.mesh_to_points(mesh=geometry), position=pos)
    curves = gs.points_to_curves(points=points)
    mapped_range = gs.map_range(
        value=gs.scene_time().seconds,
        from_min=0,
        from_max=animation_scale,
        to_min=0,
        to_max=1,
    )
    return gs.sample_curve(curves=curves, factor=mapped_range).position


@ns.tree("Animated Orbit")
def animated_orbit(geometry: ns.Geometry, radius: ns.Float):
    positions = positions_from_csv(geometry=geometry, animation_scale=10.0)
    return gs.transform_geometry(geometry=gs.uv_sphere().mesh, translation=positions)


orbit_path = os.path.expanduser("~/dxl/orbit-experiments")

fns = glob.glob(f"{orbit_path}/orbit_*.csv")

for obj in bpy.data.objects:
    if obj.name.startswith("CSV_orbit"):
        bpy.data.objects.remove(obj)

new_objs = []

for fn in sorted(fns):
    obj = csv_importer.csv.load_csv(fn)
    modifier = obj.modifiers.new("GeometryNodes", "NODES")
    modifier.node_group = bpy.data.node_groups["Animated Orbit"]
    new_objs.append(obj)

# Now we create the collection "Orbits" if it doesn't exist
if "Orbits" not in bpy.data.collections:
    orbits = bpy.data.collections.new("Orbits")
else:
    orbits = bpy.data.collections["Orbits"]

bpy.context.scene.collection.children.link(orbits)

for obj in new_objs:
    orbits.objects.link(obj)
    if obj.name in bpy.data.collections["Collection"].objects:
        bpy.data.collections["Collection"].objects.unlink(obj)
