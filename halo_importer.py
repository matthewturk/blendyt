import bpy
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

start_frame = 0
frame_interval = 24  # Number of frames each shape key will be active
particle_obj = databpy.create_object(new_objs[0], name="Particles")
# for kb in particle_obj.data.shape_keys.key_blocks:
#    kb.keyframe_clear(data_path="value")

prev_shape_key = None
for i, obj in enumerate(new_objs):
    new_shape_key = particle_obj.shape_key_add(from_mix=False)
    new_shape_key.data.foreach_set("co", obj.flatten())
    # --- Animate the shape key ---
    current_frame = start_frame + (i * frame_interval)

    # Set initial state (all shape keys off)
    # The current shape key starts influencing at `current_frame`
    # and reaches full influence at `current_frame + frame_interval`
    if prev_shape_key is not None:
        prev_shape_key.value = 1.0  # Ensure previous is full at current_frame - 1
        prev_shape_key.keyframe_insert(data_path="value", frame=current_frame - 1)

        new_shape_key.value = 0.0
        new_shape_key.keyframe_insert(
            data_path="value", frame=current_frame
        )  # Start current shape key at 0

        # Animate previous shape key fading out
        prev_shape_key.value = 0.0
        prev_shape_key.keyframe_insert(
            data_path="value", frame=current_frame + frame_interval - 1
        )  # Fades out fully just before next one finishes

    # Current shape key fades in
    new_shape_key.value = 1.0
    new_shape_key.keyframe_insert(
        data_path="value", frame=current_frame + frame_interval
    )
    prev_shape_key = new_shape_key

# Set the end frame of the animation to accommodate all shape keys
bpy.context.scene.frame_end = (
    start_frame + (len(new_objs) * frame_interval) + frame_interval
)
