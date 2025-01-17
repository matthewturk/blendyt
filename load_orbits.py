import bpy
import csv_importer.csv
import glob
import os

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

for obj in new_objs:
    orbits.objects.link(obj)
    if obj.name in bpy.data.collections["Collection"].objects:
        bpy.data.collections["Collection"].objects.unlink(obj)
