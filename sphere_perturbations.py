import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs
import nodetree_script.api.dynamic.shader as ss

@ss.materialtree("Experimental Material")
def experimental_material():
    base_color = (0.5,0.5,1,1)
    time_value = ns.scripted_expression("frame / 250")
    time_value = ss.pingpong(time_value)
    noise_color = ss.texture_coordinate().generated.noise_texture(noise_dimensions=ss.NoiseTexture.NoiseDimensions._4D, w=time_value).color
    norm =  ss.bump(normal=noise_color,distance=0.1)
    shader = ss.glass_bsdf(normal=norm,color=base_color,roughness=0.25)
    return shader


@ns.tree("Spherical Coordinates")
def spherical_coordinates(positions: ns.Vector):
    r = gs.length(positions)
    pos = gs.position()
    theta = gs.math(operation=gs.Math.Operation.ARCCOSINE, value=pos.z / r)
    phi = gs.math(operation=gs.Math.Operation.ARCTANGENT, value=pos.y / pos.x)
    return gs.combine_xyz(x=r, y=theta, z=phi)


@ns.tree("Time Varying Radially Perturbed Sphere")
def time_varying_radially_perturbed_sphere(
    geometry: ns.Geometry, magnitude: ns.Float = 0.1
):
    ts = gs.scene_time().seconds
    factor = (ts % 2) / 2.0
    index = gs.math(operation=gs.Math.Operation.FLOOR, value=(ts / 2))
    r1 = gs.random_value(
        data_type=gs.RandomValue.DataType.FLOAT,
        min=1.0,
        max=1.0 + magnitude,
        seed=index,
    )
    r2 = gs.random_value(
        data_type=gs.RandomValue.DataType.FLOAT,
        min=1.0,
        max=1.0 + magnitude,
        seed=index + 1,
    )
    new_positions = gs.vector_math(
        operation=gs.VectorMath.Operation.SCALE,
        vector=gs.vector_math(
            operation=gs.VectorMath.Operation.NORMALIZE, vector=gs.position()
        ),
        scale=gs.mix(data_type=gs.Mix.DataType.VECTOR, factor=factor, a=r1, b=r2),
    )
    rtp = spherical_coordinates(positions=new_positions)
    sphere = (
        gs.subdivide_mesh(mesh=geometry, level=4).set_position(position=new_positions)
    ).store_named_attribute(
        data_type=gs.StoreNamedAttribute.DataType.FLOAT_VECTOR,
        name="spherical_coordinates",
        value=rtp,
    )
    return sphere


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
    # sphere = gs.uv_sphere().mesh
    instances = gs.instance_on_points(points=points, instance=geometry)
    return gs.scale_instances(
        instances=instances, scale=(ts * 1.0 / 10) * (gs.index()), selection=selection
    )
