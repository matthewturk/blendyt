import bpy


class ndarray_pydata(np.ndarray):
    def __bool__(self) -> bool:
        return len(self) > 0


mesh = bpy.meshes.new(name="created mesh")
edges = edges_np.view(ndarray_pydata)
faces = faces_np.view(ndarray_pydata)
mesh.from_pydata(vertices, edges, faces)
