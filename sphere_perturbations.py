import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs
import nodetree_script.api.dynamic.shader as ss


@ns.tree("Time Varying Perturbed Sphere")
def time_varying_perturbed_sphere(geometry: ns.Geometry, magnitude: ns.Float = 0.1):
    ts = gs.scene_time().seconds
    factor = (ts % 2) / 2.0
    index = gs.math(operation=gs.Math.Operation.FLOOR, value=(ts / 2))
    r1 = gs.random_value(
        data_type=gs.RandomValue.DataType.FLOAT_VECTOR,
        max=magnitude,
        seed=index,
    )
    r2 = gs.random_value(
        data_type=gs.RandomValue.DataType.FLOAT_VECTOR,
        max=magnitude,
        seed=index + 1,
    )
    sphere = gs.subdivide_mesh(mesh=geometry, level=4).set_position(
        position=gs.vector_math(
            operation=gs.VectorMath.Operation.NORMALIZE, vector=gs.position()
        )
        + gs.mix(data_type=gs.Mix.DataType.VECTOR, factor=factor, a=r1, b=r2),
    )
    return gs.set_position(
        geometry=sphere,
    )


@ns.tree("Emitting Spheres")
def emitting_spheres(geometry: ns.Geometry):
    ts = gs.scene_time().frame
    selection = gs.math(
        operation=gs.Math.Operation.LESS_THAN, value=(1 + gs.index(), ts / 10)
    )
    points = gs.points(count=60)
    sphere = gs.uv_sphere().mesh
    instances = gs.instance_on_points(points=points, instance=sphere)
    return gs.scale_instances(
        instances=instances, scale=(ts * 1.0 / 10) * (gs.index()), selection=selection
    )
