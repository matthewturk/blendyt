import glob
import os
import databpy
import polars as pr


halo_path = os.path.expanduser("~/temp/halos/")

fns = glob.glob(f"{halo_path}/*.csv")

new_objs = []
nframes = len(fns) * 24

for i, fn in enumerate(sorted(fns)):
    arr = (
        pr.read_csv(fn)
        .sort(by="particle_index")[
            ["particle_position_x", "particle_position_y", "particle_position_z"]
        ]
        .to_numpy()
    )
    new_objs.append(arr)

particle_obj = databpy.create_object(new_objs[0], name="Particles")
particle_obj.shape_key_add(name="Basis")
particle_obj.data.shape_keys.use_relative = False

for obj in new_objs[1:]:
    new_shape_key = particle_obj.shape_key_add(from_mix=False)
    new_shape_key.points.foreach_set("co", obj.flatten())

# The evaluation time needs a driver, like `#frame * 2` or something.
