import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs


class TerrainInputs(ns.InputGroup):
    width: ns.Float
    height: ns.Float
    resolution: ns.Int
    scale: ns.Float
    w: ns.Float


@ns.tree("Experiment")
def do_something(inputs: TerrainInputs):
    return gs.cube(size=(1.0, 1.0, 1.0)).mesh


@ns.tree("Load AMR Grids")
def my_thing():
    points = gs.volume_cube(
        resolution_x=32,
        resolution_y=32,
        resolution_z=32,
        min=(0, 0, 0),
        max=(1, 1, 1),
    ).distribute_points_in_volume(
        mode=gs.DistributePointsInVolume.Mode.DENSITY_GRID, spacing=(0.25, 0.25, 0.25)
    )
    return gs.instance_on_points(
        points=points, instance=gs.cube(size=(0.1, 0.1, 0.1)).mesh
    )
