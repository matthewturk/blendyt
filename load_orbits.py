import bpy
import csv_importer.csv
import glob
import os

orbit_path = os.path.expanduser("~/dxl/orbit-experiments")

fns = glob.glob(f"{orbit_path}/orbit_*.csv")

for fn in sorted(fns):
    obj = csv_importer.csv.load_csv(fn)
    modifier = obj.modifiers.new("GeometryNodes", "NODES")
    modifier.node_group = bpy.data.node_groups["Animated Orbit"]
