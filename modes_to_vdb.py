import numpy as np
import openvdb as vdb
import h5py

with h5py.File("modes.h5") as f:
    data = np.abs((f["/70.00"][:]).imag)
    print(f"Data shape: {data.shape}, min: {data.min()}, max: {data.max()}")
    # data = np.log10(data)
    mi = data.min()  # axis=(0, 1))
    ma = data.max()  # axis=(0, 1))
    data = (data - mi) / (ma - mi)
    print(f"Data shape: {data.shape}, min: {data.min()}, max: {data.max()}")
    # print(data.min(axis=(0, 1)), data.max(axis=(0, 1)))
    g_vdb = vdb.FloatGrid()
    g_vdb.name = "70.00"
    # g_vdb.transform = vdb.createLinearTransform(
    #    voxelSize=(1.0 / np.pi, 2.0 / np.pi, 1.0)
    # )
    g_vdb.copyFromArray(np.abs(data), ijk=(0, 0, 0))
vdb.write("modes.vdb", [g_vdb])
