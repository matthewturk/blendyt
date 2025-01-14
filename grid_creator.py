import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs
import nodetree_script.api.dynamic.shader as ss
import numpy as np


class GridSpecification(ns.InputGroup):
    left_edge: ns.Vector
    right_edge: ns.Vector
    nx: ns.Int
    ny: ns.Int
    nz: ns.Int


@ns.tree("Positions from CSV")
def positions_from_csv(geometry: ns.Geometry, animation_scale: ns.Float):
    x = gs.named_attribute(name="x").attribute
    y = gs.named_attribute(name="y").attribute
    z = gs.named_attribute(name="z").attribute
    pos = gs.combine_xyz(x=x, y=y, z=z)
    points = gs.set_position(geometry=gs.mesh_to_points(mesh=geometry), position=pos)
    curves = gs.points_to_curves(points=points)
    mapped_range = gs.map_range(
        value=gs.scene_time().seconds,
        from_min=0,
        from_max=animation_scale,
        to_min=0,
        to_max=1,
    )
    return gs.sample_curve(curves=curves, factor=mapped_range).position


@ns.tree("Animated Orbit")
def animated_orbit(geometry: ns.Geometry, radius: ns.Float):
    positions = positions_from_csv(geometry=geometry, animation_scale=10.0)
    return gs.transform_geometry(geometry=gs.uv_sphere().mesh, translation=positions)


@ns.tree("Grid as Points")
def grid_as_points(spec: GridSpecification):
    cube = gs.cube(size=spec.right_edge - spec.left_edge)
    curves = gs.store_named_attribute(
        geometry=gs.mesh_to_curve(mesh=cube.mesh), name="curve_index", value=gs.index()
    )
    points = gs.curve_to_points(curve=curves)
    return {"points": points.points, "curves": curves}


class GravityInput(ns.InputGroup):
    magnitude: ns.Float
    source_position: ns.Vector
    geometry: ns.Geometry


@ns.tree("Apply Gravity")
def apply_gravity(inputs: GravityInput):
    pos = gs.position()
    value = inputs.magnitude / (
        gs.vector_math(
            operation=gs.VectorMath.Operation.DISTANCE,
            vector=(inputs.source_position, pos),
        )
        ** 0.5
    )
    direction = gs.vector_math(operation=gs.VectorMath.Operation.NORMALIZE, vector=pos)
    return gs.set_position(geometry=inputs.geometry, position=pos - direction * value)
