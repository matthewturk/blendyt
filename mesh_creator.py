## https://stackoverflow.com/questions/68297161/creating-a-blender-mesh-directly-from-numpy-data

import numpy as np
import bpy
import numpy

# the numpy array must be in this form
vertices = numpy.array(
    [
        1,
        1,
        1,  # vertex 0
        -1,
        1,
        -1,  # vertex 1
        -1,
        -1,
        1,  # vertex 2
        1,
        -1,
        -1,  # vertex 3
    ],
    dtype=numpy.float32,
)

# vertices for each polygon
vertex_index = numpy.array(
    [
        0,
        1,
        2,  #  first polygon starting at 0
        0,
        2,
        3,  # second polygon starting at 3
        0,
        3,
        1,  #  third polygon starting at 6
        2,
        1,
        3,  #  forth polygon starting at 9
    ],
    dtype=numpy.int32,
)


# every polygon start at a specific index in vertex_index array
loop_start = numpy.array(
    [
        0,  # polygon start at 0 --> 0, 1, 2
        3,  # polygon start at 3 --> 0, 2, 3
        6,  # polygon start at 6 --> 0, 3, 1
        9,  # polygon start at 9 --> 2, 1, 3
    ],
    dtype=numpy.int32,
)

# lenght of the loop
num_loops = loop_start.shape[0]


# Length of each polygon in number of vertices
loop_total = numpy.array([3, 3, 3, 3], dtype=numpy.int32)


# Create mesh object based on the arrays above
mesh = bpy.data.meshes.new(name="created mesh")

# Number of vertices in vertices array (12 // 3)
num_vertices = vertices.shape[0] // 3

# add the amount of vertices, in this case 4.
mesh.vertices.add(num_vertices)

# use the vertices numpy array
mesh.vertices.foreach_set("co", vertices)

# total indexes in vertex_index
num_vertex_indices = vertex_index.shape[0]

# add the amount of the vertex_index array, in this case 12
mesh.loops.add(num_vertex_indices)

# set the vertx_index
mesh.loops.foreach_set("vertex_index", vertex_index)

# add the length of loop_start array
mesh.polygons.add(num_loops)

# generate the polygons
mesh.polygons.foreach_set("loop_start", loop_start)
mesh.polygons.foreach_set("loop_total", loop_total)


class ndarray_pydata(np.ndarray):
    def __bool__(self) -> bool:
        return len(self) > 0


vertices = np.array(
    [
        (1, 1, 1),
        (-1, 1, -1),
        (-1, -1, 1),
        (1, -1, -1),
    ],
    dtype=np.float32,
)

faces = np.array([[0, 1, 2], [0, 2, 3], [0, 3, 1], [2, 1, 3]], dtype=int)

mesh = bpy.data.meshes.new(name="created mesh")
vertices = vertices.view(ndarray_pydata)
faces = faces.view(ndarray_pydata)
mesh.from_pydata(vertices, [], faces)
