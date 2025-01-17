import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs
import nodetree_script.api.dynamic.shader as ss


@ns.tree("Time Varying Perturbed Sphere")
def time_varying_perturbed_sphere(geometry: ns.Geometry, time: ns.Float):
    ts = gs.scene_time().seconds
    pos = gs.position()
    r1 = gs.random_value(
        data_type=gs.RandomValue.DataType.FLOAT_VECTOR, min=-0.1, max=0.1, seed=0
    )
    r2 = gs.random_value(
        data_type=gs.RandomValue.DataType.FLOAT_VECTOR, min=-0.1, max=0.1, seed=1
    )
    posi = r1 + pos
    posf = r2 + pos
    factor = (ts % 2) / 5
    return gs.set_position(
        geometry=geometry,
        position=gs.mix(
            data_type=gs.Mix.DataType.VECTOR, factor=factor, a=posi, b=posf
        ),
    )


@ns.tree("Emitting Spheres")
def emitting_spheres(geometry: ns.Geometry):
    ts = gs.scene_time().frame
    selection = gs.math(
        operation=gs.Math.Operation.LESS_THAN, value=(gs.index(), ts / 10)
    )
    points = gs.points(count=60)
    sphere = gs.uv_sphere().mesh
    instances = gs.instance_on_points(points=points, instance=sphere)
    return gs.scale_instances(
        instances=instances, scale=gs.index(), selection=selection
    )
