import struct
import os
import glob
import numpy as np

import bpy
import databpy


bgeo_header = (
    ("version", "i"),
    ("npoints", "i"),
    ("nprims", "i"),
    ("npointgroups", "i"),
    ("nprimgroups", "i"),
    ("npointattrib", "i"),
    ("nvertexattrib", "i"),
    ("nprimattrib", "i"),
    ("nattrib", "i"),
)


def read_struct_format(f, fmt):
    fmt = f">{fmt}"  # Ensure big-endian format
    size = struct.calcsize(fmt)
    data = f.read(size)
    if len(data) != size:
        raise ValueError("Unexpected end of file while reading struct")
    return struct.unpack(fmt, data)


dtype_map = {0: "float32", 1: "int32", 3: "3*float32"}


def read_attribute_header(f):
    name_length = read_struct_format(f, "h")[0]
    name = f.read(name_length).decode("ascii")
    size = read_struct_format(f, "h")[0]
    attr_type = read_struct_format(f, "i")[0]
    f.read(4 * size)  # Skip default values
    return name, dtype_map[attr_type]


def read_particles(fn: str):
    header = {}
    with open(fn, "rb") as f:
        magic_format = "5c"
        data = f.read(struct.calcsize(magic_format))
        magic = struct.unpack(magic_format, data)
        assert magic == (b"B", b"g", b"e", b"o", b"V"), "Not a valid BGEO file"
        attributes = []
        for name, dtype in bgeo_header:
            (header[name],) = read_struct_format(f, dtype)
        for i in range(header["npointattrib"]):
            attributes.append(read_attribute_header(f))
        new_dtype = np.dtype(
            [
                ("particle_position_x", "f4"),
                ("particle_position_y", "f4"),
                ("particle_position_z", "f4"),
                ("unknown", "f4"),
            ]
            + attributes
        )
        points = np.fromfile(f, dtype=new_dtype, count=header["npoints"]).byteswap()
    return points


if 0 and __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python read_load_bgeo.py <path_to_bgeo_file>")
        sys.exit(1)

    bgeo_file_path = sys.argv[1]
    arr = read_particles(bgeo_file_path)
    print(f"Successfully read BGEO file: {bgeo_file_path}")


cluster_path = os.path.expanduser("~/cluster/")
fns = glob.glob(f"{cluster_path}/nobh6-18d.*.bgeo")
fns = sorted([_ for _ in fns if "orbit" not in _])

arrs = []

for fn in fns:
    arrs.append(read_particles(fn))

arrs = np.array(arrs)

new_objs = []
for i in range(100):
    x = arrs[:, i]["particle_position_x"]
    y = arrs[:, i]["particle_position_y"]
    z = arrs[:, i]["particle_position_z"]
    obj = databpy.create_object(np.array([x, y, z]).T, name=f"Particles_{i:03d}")
    new_objs.append(obj)
