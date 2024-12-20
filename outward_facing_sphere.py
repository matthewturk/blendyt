import nodetree_script as ns
import nodetree_script.api.dynamic.geometry as gs
import nodetree_script.api.dynamic.shader as ss

# https://i.sstatic.net/8tkSm.png
# https://blender.stackexchange.com/questions/271014/how-do-i-set-a-very-specific-number-of-instances-to-distribute-within-a-randomiz


@ns.tree("Outward Sphere")
def outward_facing_sphere(size: ns.Float, density: ns.Float):
    sphere = gs.uv_sphere(radius=size, segments=1024, rings=1024)
    points = gs.distribute_points_on_faces(mesh=sphere.mesh, density=density)
    line = gs.mesh_line()
    rotation = gs.align_rotation_to_vector(vector=gs.position())
    return {
        "Geometry": gs.instance_on_points(
            points=points.points,
            instance=line,
            rotation=rotation,
        ),
        "Points": points.points,
        "BasicGeometry": sphere.mesh,
    }


@ns.tree("Sphere To Curves")
def sphere_to_curves(sphere: ns.Geometry):
    # sphere1 = gs.uv_sphere(radius=100.0, segments=1024, rings=1024)
    sphere1 = sphere
    sphere2 = gs.uv_sphere(radius=1.0, segments=32, rings=32)
    target_volume = gs.volume_cube(min=(-210, -210, -10), max=(-190, -190, 10))
    points1 = gs.distribute_points_on_faces(mesh=sphere1, density=0.01)
    points2 = gs.distribute_points_in_volume(volume=target_volume, density=0.01)
    g1 = gs.instance_on_points(points=points1.points, instance=sphere2.mesh)
    g2 = gs.instance_on_points(points=points2, instance=sphere2.mesh)
    return gs.join_geometry(geometry=[g1, g2])


@ns.tree("Max Points")
def max_points(geometry: ns.Geometry):
    return


@ns.shadertree("Color Spheres")
def shader(color: ns.Color):
    pbsdf = ss.principled_bsdf(base_color=color)
    return {"Shader": pbsdf}
