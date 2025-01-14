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


@ns.tree("Select Vertex by Index")
def select_vertex_by_index(geometry: ns.Geometry, index: ns.Int):
    vindex = gs.index()
    comparison = gs.math(operation=gs.Math.Operation.COMPARE, value=(index, vindex))
    return gs.separate_geometry(geometry=geometry, selection=comparison).selection


@ns.tree("Spheres at Vertex Attributes")
def spheres_at_vertex_attributes(geometry: ns.Geometry):
    x = gs.named_attribute(name="x").attribute
    y = gs.named_attribute(name="y").attribute
    z = gs.named_attribute(name="z").attribute
    pos = gs.combine_xyz(x=x, y=y, z=z)
    points = gs.set_position(geometry=gs.mesh_to_points(mesh=geometry), position=pos)
    return gs.instance_on_points(points=points, instance=gs.uv_sphere().mesh)


@ns.tree("Animated Orbit")
def animated_orbit(geometry: ns.Geometry):
    scene_time = gs.scene_time()
    svbi = select_vertex_by_index(geometry=geometry, index=scene_time.frame)
    return spheres_at_vertex_attributes(geometry=svbi)


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
