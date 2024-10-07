import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs


@ns.tree("Outward Sphere")
def outward_facing_sphere():
    sphere = gs.uv_sphere(radius=100.0, segments=1024, rings=1024)
    points = gs.distribute_points_on_faces(mesh=sphere.mesh, density=0.01)
    line = gs.mesh_line()
    rotation = gs.align_rotation_to_vector(vector=gs.position())
    return gs.instance_on_points(points=points.points, instance=line, rotation=rotation)
