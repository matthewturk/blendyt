import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs
import nodetree_script.api.dynamic.shader as ss


@ns.materialtree("Experimental Material")
def experimental_material():
    base_color = (0.5, 0.5, 1, 1)
    time_value = ns.scripted_expression("frame / 250")
    time_value = ss.pingpong(time_value)
    noise_color = (
        ss.texture_coordinate()
        .generated.noise_texture(
            noise_dimensions=ss.NoiseTexture.NoiseDimensions._4D, w=time_value
        )
        .color
    )
    norm = ss.bump(normal=noise_color, distance=0.1)
    shader = ss.glass_bsdf(normal=norm, color=base_color, roughness=0.25)
    return shader


@ns.tree("Spherical Coordinates")
def spherical_coordinates(positions: ns.Vector):
    r = gs.length(positions)
    pos = gs.position()
    theta = gs.math(operation=gs.Math.Operation.ARCCOSINE, value=pos.z / r)
    phi = gs.math(operation=gs.Math.Operation.ARCTAN2, value=(pos.y, pos.x))
    return gs.combine_xyz(x=r, y=theta, z=phi)


@ns.tree("Time Varying Radially Perturbed Sphere")
def time_varying_radially_perturbed_sphere(
    geometry: ns.Geometry, magnitude: ns.Float = 0.1, ts: ns.Float = 0
):
    factor = (ts % 20) / 20.0
    index = gs.math(operation=gs.Math.Operation.FLOOR, value=(ts / 20))
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
def time_varying_perturbed_sphere(
    geometry: ns.Geometry, magnitude: ns.Float = 0.1, ts: ns.Float = 0
):
    factor = (ts % 20) / 20.0
    index = gs.math(operation=gs.Math.Operation.FLOOR, value=(ts / 20.0))
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


@ns.tree("Emitted Scale")
def emitted_scale(frame_delta: ns.Int, index_attribute: ns.String):
    ts = gs.scene_time().frame
    index = gs.named_attribute(
        data_type=gs.NamedAttribute.DataType.INT,
        name=index_attribute,
    ).attribute
    scale = gs.clamp(
        clamp_type=gs.Clamp.ClampType.MINMAX,
        value=(ts - index * frame_delta) / frame_delta,
        min=1.0,
        max=100.0,
    )
    return scale
